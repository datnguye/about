// Article Ads Insertion Script
function insertArticleAds() {
    const content = document.getElementById('article-content');
    if (!content) return;
    
    const paragraphs = content.querySelectorAll('p');
    
    // Calculate ad positions - after every 3-4 paragraphs
    const totalParagraphs = paragraphs.length;
    const adInterval = 3; // Insert ad every 3 paragraphs
    const maxAds = 1; // Maximum number of in-article ads
    
    let adsInserted = 0;
    
    // Insert ads at calculated positions
    for (let i = adInterval; i < totalParagraphs && adsInserted < maxAds; i += adInterval + 1) {
        if (paragraphs[i]) {
            // Create ad container
            const adContainer = document.createElement('div');
            adContainer.className = 'my-8 mx-auto in-article-ad';
            adContainer.innerHTML = `
                <ins class="adsbygoogle"
                     style="display:block; text-align:center;"
                     data-ad-layout="in-article"
                     data-ad-format="fluid"
                     data-ad-client="ca-pub-9818368894527523"
                     data-ad-slot="2619000802"></ins>
            `;
            
            // Insert ad after the paragraph
            paragraphs[i].parentNode.insertBefore(adContainer, paragraphs[i].nextSibling);
            
            // Push ad to adsbygoogle
            (adsbygoogle = window.adsbygoogle || []).push({});
            adsInserted++;
        }
    }
    
    // Also insert ads between long sections
    const headings = content.querySelectorAll('h2, h3');
    
    headings.forEach((heading) => {
        // Count content length between headings
        let element = heading.nextElementSibling;
        let sectionLength = 0;
        
        while (element && !['H2', 'H3'].includes(element.tagName)) {
            if (element.tagName === 'P') {
                sectionLength += element.textContent.length;
            }
            element = element.nextElementSibling;
        }
        
        // If section is long (>1000 chars), insert an ad in the middle
        if (sectionLength > 1000 && adsInserted < maxAds + 2) {
            let midElement = heading.nextElementSibling;
            let currentLength = 0;
            
            while (midElement && currentLength < sectionLength / 2) {
                if (midElement.tagName === 'P') {
                    currentLength += midElement.textContent.length;
                }
                if (currentLength >= sectionLength / 2 && midElement.nextElementSibling) {
                    // Create ad container
                    const adContainer = document.createElement('div');
                    adContainer.className = 'my-8 mx-auto in-article-ad';
                    adContainer.innerHTML = `
                        <ins class="adsbygoogle"
                             style="display:block; text-align:center;"
                             data-ad-layout="in-article"
                             data-ad-format="fluid"
                             data-ad-client="ca-pub-9818368894527523"
                             data-ad-slot="2619000802"></ins>
                    `;
                    
                    midElement.parentNode.insertBefore(adContainer, midElement.nextSibling);
                    (adsbygoogle = window.adsbygoogle || []).push({});
                    adsInserted++;
                    break;
                }
                midElement = midElement.nextElementSibling;
            }
        }
    });
}

// Run when DOM is loaded
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', insertArticleAds);
} else {
    insertArticleAds();
}