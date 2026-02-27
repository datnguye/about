const SYSTEM_PROMPT = `You are a brutally honest, hilariously savage website roaster — think Gordon Ramsay reviewing restaurants, but for websites. You just visited a website and scraped its content. Now deliver a roast.

Rules:
- Be funny, sharp, and brutally honest — but NEVER personal or hateful
- Roast the design, copy, UX, tech choices, marketing speak, and overall vibe
- Use analogies, pop culture references, and dramatic flair
- Keep it around 250-350 words
- Use markdown formatting: bold for emphasis, bullet points for lists
- End with ONE backhanded compliment
- After the backhanded compliment, add a warm closing line like "No hard feelings — just love wrapped in fire 🤗🔥" or similar. Make it genuinely sweet and huggy to ease the burn
- Never mention that you scraped or received HTML/text — pretend you visited the site like a real user
- If the content is mostly empty or broken, roast that fact mercilessly`;

const RATE_LIMIT_MAX = 5;
const RATE_LIMIT_WINDOW_MS = 60_000;
const rateLimitMap = new Map();

function isRateLimited(ip) {
  const now = Date.now();
  const entry = rateLimitMap.get(ip);

  if (!entry || now - entry.windowStart >= RATE_LIMIT_WINDOW_MS) {
    rateLimitMap.set(ip, { windowStart: now, count: 1 });
    return false;
  }

  entry.count++;
  return entry.count > RATE_LIMIT_MAX;
}

function cleanupRateLimitMap() {
  const now = Date.now();
  for (const [ip, entry] of rateLimitMap) {
    if (now - entry.windowStart >= RATE_LIMIT_WINDOW_MS) {
      rateLimitMap.delete(ip);
    }
  }
}

export default {
  async fetch(request, env) {
    const origin = request.headers.get("Origin") || "";
    const allowedOrigins = (env.ALLOWED_ORIGINS || "https://about.datnguyen.de")
      .split(",")
      .map((o) => o.trim());
    const isAllowed = allowedOrigins.includes(origin);

    const corsHeaders = {
      "Access-Control-Allow-Origin": isAllowed ? origin : allowedOrigins[0],
      "Access-Control-Allow-Methods": "POST, OPTIONS",
      "Access-Control-Allow-Headers": "Content-Type",
    };

    if (request.method === "OPTIONS") {
      return new Response(null, { status: 204, headers: corsHeaders });
    }

    if (request.method !== "POST") {
      return new Response(JSON.stringify({ error: "Method not allowed" }), {
        status: 405,
        headers: { ...corsHeaders, "Content-Type": "application/json" },
      });
    }

    const clientIp = request.headers.get("CF-Connecting-IP") || "unknown";
    cleanupRateLimitMap();
    if (isRateLimited(clientIp)) {
      return new Response(JSON.stringify({ error: "Too many requests. Please wait a minute before trying again." }), {
        status: 429,
        headers: { ...corsHeaders, "Content-Type": "application/json", "Retry-After": "60" },
      });
    }

    try {
      const body = await request.json();
      const targetUrl = body.url;

      if (!targetUrl || !isValidUrl(targetUrl)) {
        return new Response(JSON.stringify({ error: "Invalid URL provided" }), {
          status: 422,
          headers: { ...corsHeaders, "Content-Type": "application/json" },
        });
      }

      let scrapeResult;
      try {
        scrapeResult = await scrapeUrl(targetUrl);
      } catch (err) {
        return new Response(JSON.stringify({ error: `Could not fetch that site: ${err.message}` }), {
          status: 422,
          headers: { ...corsHeaders, "Content-Type": "application/json" },
        });
      }

      let siteText = scrapeResult.text;
      const siteMeta = { title: scrapeResult.siteTitle, favicon: scrapeResult.faviconUrl };

      if (!siteText || siteText.trim().length < 20) {
        siteText = `[The website at ${targetUrl} returned almost no readable content — it's either blank, behind a login wall, or built entirely with JavaScript that blocks scraping.]`;
      }

      const models = [
        "meta-llama/llama-3.3-70b-instruct:free",
        "openai/gpt-oss-120b:free",
        "google/gemma-3-27b-it:free",
        "meta-llama/llama-3.3-70b-instruct",
      ];
      let openrouterResponse;

      for (const model of models) {
        openrouterResponse = await fetch("https://openrouter.ai/api/v1/chat/completions", {
          method: "POST",
          headers: {
            "Authorization": `Bearer ${env.OPENROUTER_API_KEY}`,
            "Content-Type": "application/json",
            "HTTP-Referer": allowedOrigins[0],
          },
          body: JSON.stringify({
            model,
            stream: true,
            messages: [
              { role: "system", content: SYSTEM_PROMPT },
              { role: "user", content: `Roast this website (${targetUrl}):\n\n${siteText}` },
            ],
            temperature: 0.9,
            max_tokens: 1024,
          }),
        });

        if (openrouterResponse.ok) break;

        const isFreeModel = model.endsWith(":free");
        const isRateLimit = openrouterResponse.status === 402 || openrouterResponse.status === 429;
        if (isFreeModel && (isRateLimit || !openrouterResponse.ok)) {
          console.log(`Free model ${model} failed (${openrouterResponse.status}), trying next...`);
          continue;
        }

        break;
      }

      if (openrouterResponse.status === 402 || openrouterResponse.status === 429) {
        return new Response(JSON.stringify({ error: "AI credits exhausted. Please try again later." }), {
          status: 402,
          headers: { ...corsHeaders, "Content-Type": "application/json" },
        });
      }

      if (!openrouterResponse.ok) {
        const errText = await openrouterResponse.text();
        console.error("OpenRouter error:", openrouterResponse.status, errText);
        return new Response(JSON.stringify({ error: "Upstream AI service error", detail: errText }), {
          status: 502,
          headers: { ...corsHeaders, "Content-Type": "application/json" },
        });
      }

      // Prepend site metadata event before the LLM stream
      const metaEvent = `data: ${JSON.stringify({ site_meta: siteMeta })}\n\n`;
      const metaStream = new ReadableStream({
        start(controller) {
          controller.enqueue(new TextEncoder().encode(metaEvent));
          const reader = openrouterResponse.body.getReader();
          function pump() {
            reader.read().then(({ done, value }) => {
              if (done) {
                controller.close();
                return;
              }
              controller.enqueue(value);
              pump();
            }).catch((err) => controller.error(err));
          }
          pump();
        },
      });

      return new Response(metaStream, {
        status: 200,
        headers: {
          ...corsHeaders,
          "Content-Type": "text/event-stream",
          "Cache-Control": "no-cache",
          "Connection": "keep-alive",
        },
      });
    } catch (err) {
      console.error("Worker error:", err.message, err.stack);
      return new Response(JSON.stringify({ error: "Internal server error", detail: err.message }), {
        status: 500,
        headers: { ...corsHeaders, "Content-Type": "application/json" },
      });
    }
  },
};

function isValidUrl(str) {
  try {
    const url = new URL(str);
    return url.protocol === "http:" || url.protocol === "https:";
  } catch {
    return false;
  }
}

function decodeHtmlEntities(str) {
  return str
    .replace(/&#(\d+);/g, (_, code) => String.fromCharCode(code))
    .replace(/&#x([0-9a-fA-F]+);/g, (_, code) => String.fromCharCode(parseInt(code, 16)))
    .replace(/&amp;/g, "&")
    .replace(/&lt;/g, "<")
    .replace(/&gt;/g, ">")
    .replace(/&quot;/g, '"')
    .replace(/&#039;/g, "'")
    .replace(/&apos;/g, "'")
    .replace(/&nbsp;/g, " ");
}

async function scrapeUrl(targetUrl) {
  const response = await fetch(targetUrl, {
    headers: {
      "User-Agent": "Mozilla/5.0 (compatible; RoastBot/1.0)",
      "Accept": "text/html,application/xhtml+xml",
    },
    redirect: "follow",
    cf: { cacheTtl: 300 },
  });

  if (!response.ok) {
    throw new Error(`HTTP ${response.status}`);
  }

  const html = await response.text();

  // Extract site title and decode HTML entities
  const titleMatch = html.match(/<title[^>]*>([\s\S]*?)<\/title>/i);
  const siteTitle = titleMatch
    ? decodeHtmlEntities(titleMatch[1].replace(/\s+/g, " ").trim())
    : "";

  // Extract favicon URL
  const parsedUrl = new URL(targetUrl);
  const baseUrl = `${parsedUrl.protocol}//${parsedUrl.host}`;
  let faviconUrl = `${baseUrl}/favicon.ico`;

  const iconMatch = html.match(/<link[^>]*rel=["'](?:icon|shortcut icon)["'][^>]*href=["']([^"']+)["'][^>]*>/i)
    || html.match(/<link[^>]*href=["']([^"']+)["'][^>]*rel=["'](?:icon|shortcut icon)["'][^>]*>/i);
  if (iconMatch) {
    const href = iconMatch[1];
    if (href.startsWith("http")) {
      faviconUrl = href;
    } else if (href.startsWith("//")) {
      faviconUrl = `${parsedUrl.protocol}${href}`;
    } else if (href.startsWith("/")) {
      faviconUrl = `${baseUrl}${href}`;
    } else {
      faviconUrl = `${baseUrl}/${href}`;
    }
  }

  const stripped = html
    .replace(/<script[^>]*>[\s\S]*?<\/script>/gi, "")
    .replace(/<style[^>]*>[\s\S]*?<\/style>/gi, "")
    .replace(/<nav[^>]*>[\s\S]*?<\/nav>/gi, "")
    .replace(/<footer[^>]*>[\s\S]*?<\/footer>/gi, "")
    .replace(/<header[^>]*>[\s\S]*?<\/header>/gi, "")
    .replace(/<[^>]+>/g, " ")
    .replace(/\s+/g, " ")
    .trim();

  const decoded = decodeHtmlEntities(stripped);

  return { text: decoded.slice(0, 4000), siteTitle, faviconUrl };
}
