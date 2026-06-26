(function () {
    const config = window.ROAST_CONFIG || {};
    const workerUrl = config.workerUrl;
    const bmcUrl = config.bmcUrl;

    const form = document.getElementById("roast-form");
    const urlInput = document.getElementById("url-input");
    const urlError = document.getElementById("url-error");
    const roastBtn = document.getElementById("roast-btn");
    const loadingSection = document.getElementById("loading-section");
    const resultSection = document.getElementById("result-section");
    const roastText = document.getElementById("roast-text");
    const typingCursor = document.getElementById("typing-cursor");
    const targetUrlEl = document.getElementById("target-url");
    const siteFavicon = document.getElementById("site-favicon");
    const siteTitle = document.getElementById("site-title");
    const actionButtons = document.getElementById("action-buttons");
    const copyBtn = document.getElementById("copy-btn");
    const anotherBtn = document.getElementById("another-btn");
    const bmcModal = document.getElementById("bmc-modal");
    const bmcClose = document.getElementById("bmc-close");
    const bmcLink = document.getElementById("bmc-link");

    if (bmcUrl && bmcLink) {
        bmcLink.href = bmcUrl;
    }

    let rawRoastText = "";
    let roastInProgress = false;
    let abortController = null;
    const REQUEST_TIMEOUT_MS = 30000;

    form.addEventListener("submit", function (e) {
        e.preventDefault();
        if (roastInProgress) return;
        startRoast();
    });

    copyBtn.addEventListener("click", copyRoast);
    anotherBtn.addEventListener("click", resetForm);
    bmcClose.addEventListener("click", closeBmcModal);
    bmcModal.addEventListener("click", function (e) {
        if (e.target === bmcModal) closeBmcModal();
    });

    function isValidUrl(str) {
        try {
            var url = new URL(str);
            return url.protocol === "http:" || url.protocol === "https:";
        } catch (_) {
            return false;
        }
    }

    function showError(msg) {
        urlError.textContent = msg;
        urlError.classList.remove("hidden");
    }

    function hideError() {
        urlError.classList.add("hidden");
    }

    function setState(state) {
        var heroInputs = form;
        loadingSection.classList.add("hidden");
        resultSection.classList.add("hidden");
        actionButtons.classList.add("hidden");
        typingCursor.classList.add("hidden");

        if (state === "input") {
            heroInputs.classList.remove("hidden");
            roastBtn.disabled = false;
            roastBtn.innerHTML = '<i class="fas fa-fire"></i> Destroy It';
        } else if (state === "loading") {
            roastBtn.disabled = true;
            roastBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Destroying...';
            loadingSection.classList.remove("hidden");
        } else if (state === "streaming") {
            roastBtn.disabled = true;
            loadingSection.classList.add("hidden");
            resultSection.classList.remove("hidden");
            typingCursor.classList.remove("hidden");
        } else if (state === "done") {
            roastBtn.disabled = false;
            roastBtn.innerHTML = '<i class="fas fa-fire"></i> Destroy It';
            resultSection.classList.remove("hidden");
            typingCursor.classList.add("hidden");
            actionButtons.classList.remove("hidden");
            actionButtons.style.display = "flex";
        }
    }

    async function startRoast() {
        hideError();
        var url = urlInput.value.trim();

        if (!url) {
            showError("Please enter a URL.");
            return;
        }

        if (!url.startsWith("http://") && !url.startsWith("https://")) {
            url = "https://" + url;
            urlInput.value = url;
        }

        if (!isValidUrl(url)) {
            showError("Please enter a valid URL (e.g. https://example.com).");
            return;
        }

        rawRoastText = "";
        roastText.innerHTML = "";
        targetUrlEl.textContent = url;

        // Set fallback title from hostname until worker sends real metadata
        try {
            siteTitle.textContent = new URL(url).hostname;
        } catch (_) {
            siteTitle.textContent = url;
        }
        siteFavicon.src = "";
        siteFavicon.classList.add("hidden");

        setState("loading");
        roastInProgress = true;
        abortController = new AbortController();
        var timeoutId = setTimeout(function () {
            abortController.abort();
        }, REQUEST_TIMEOUT_MS);

        try {
            var response = await fetch(workerUrl, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ url: url }),
                signal: abortController.signal,
            });

            clearTimeout(timeoutId);

            if (response.status === 402) {
                setState("input");
                showBmcModal();
                return;
            }

            if (response.status === 429) {
                setState("input");
                showError("Slow down! Too many roasts. Wait a minute and try again.");
                return;
            }

            if (!response.ok) {
                var errBody = await response.json().catch(function () {
                    return { error: "Something went wrong. Try again." };
                });
                setState("input");
                showError(errBody.error || "Something went wrong. Try again.");
                return;
            }

            setState("streaming");
            await readStream(response);
            setState("done");
        } catch (err) {
            clearTimeout(timeoutId);
            setState("input");
            if (err.name === "AbortError") {
                showError("Request timed out. The site might be too slow or unreachable.");
            } else {
                showError("Network error. Check your connection and try again.");
            }
        } finally {
            roastInProgress = false;
            abortController = null;
        }
    }

    async function readStream(response) {
        var reader = response.body.getReader();
        var decoder = new TextDecoder();
        var buffer = "";

        while (true) {
            var result = await reader.read();
            if (result.done) break;

            buffer += decoder.decode(result.value, { stream: true });
            var lines = buffer.split("\n");
            buffer = lines.pop();

            for (var i = 0; i < lines.length; i++) {
                var line = lines[i].trim();
                if (!line.startsWith("data: ")) continue;
                var data = line.slice(6);
                if (data === "[DONE]") return;

                try {
                    var parsed = JSON.parse(data);

                    // Handle site metadata event
                    if (parsed.site_meta) {
                        if (parsed.site_meta.favicon) {
                            siteFavicon.src = parsed.site_meta.favicon;
                            siteFavicon.classList.remove("hidden");
                            siteFavicon.onerror = function () {
                                siteFavicon.classList.add("hidden");
                            };
                        }
                        if (parsed.site_meta.title) {
                            siteTitle.textContent = parsed.site_meta.title;
                        }
                        continue;
                    }

                    var delta = parsed.choices && parsed.choices[0] && parsed.choices[0].delta;
                    var content = delta && delta.content;
                    if (content) {
                        rawRoastText += content;
                        renderMarkdown(rawRoastText);
                    }
                } catch (_) {
                    // skip malformed chunks
                }
            }
        }
    }

    function escapeHtml(str) {
        return str
            .replace(/&/g, "&amp;")
            .replace(/</g, "&lt;")
            .replace(/>/g, "&gt;")
            .replace(/"/g, "&quot;")
            .replace(/'/g, "&#039;");
    }

    function renderMarkdown(text) {
        var html = escapeHtml(text)
            .replace(/\*\*(.+?)\*\*/g, "<strong>$1</strong>")
            .replace(/\*(.+?)\*/g, "<em>$1</em>")
            .replace(/^[-*] (.+)$/gm, "<li>$1</li>")
            .replace(/\n/g, "<br>");

        html = html.replace(/((?:<li>.*?<\/li><br>?)+)/g, function (match) {
            return "<ul>" + match.replace(/<br>/g, "") + "</ul>";
        });

        roastText.innerHTML = html;
    }

    function copyRoast() {
        navigator.clipboard.writeText(rawRoastText).then(function () {
            copyBtn.innerHTML = '<i class="fas fa-check"></i> Copied!';
            setTimeout(function () {
                copyBtn.innerHTML = '<i class="fas fa-copy"></i> Copy';
            }, 2000);
        });
    }



    function resetForm() {
        urlInput.value = "";
        rawRoastText = "";
        roastText.innerHTML = "";
        targetUrlEl.textContent = "";
        siteFavicon.src = "";
        siteFavicon.classList.add("hidden");
        siteTitle.textContent = "";
        setState("input");
        hideError();
        urlInput.focus();
    }

    function showBmcModal() {
        bmcModal.classList.remove("hidden");
        bmcModal.style.display = "flex";
    }

    function closeBmcModal() {
        bmcModal.classList.add("hidden");
        bmcModal.style.display = "";
    }
})();
