function initGiscusComments() {
    const commentsSection = document.getElementById('comments-section');
    if (!commentsSection) return;
    
    // Clear the loading message
    commentsSection.innerHTML = '';
    
    // Check if discussions are likely enabled (this is a fallback UI)
    const checkDiscussions = () => {
        setTimeout(() => {
            const giscusFrame = document.querySelector('iframe.giscus-frame');
            if (!giscusFrame) {
                commentsSection.innerHTML = `
                    <div style="background: rgba(255, 165, 0, 0.1); border: 2px solid rgba(255, 165, 0, 0.3); border-radius: 8px; padding: 2rem; text-align: center;">
                        <h3 style="color: #FFA500; margin-bottom: 1rem;">📝 Enable GitHub Discussions</h3>
                        <p style="margin-bottom: 1.5rem;">Comments require GitHub Discussions to be enabled:</p>
                        <ol style="text-align: left; display: inline-block; margin-bottom: 1.5rem; line-height: 1.8;">
                            <li>Go to your <a href="https://github.com/datnguye/about/settings" target="_blank" style="color: var(--primary);">repository settings</a></li>
                            <li>Scroll to "Features" section</li>
                            <li>Check ✅ <strong>Discussions</strong></li>
                            <li>Refresh this page</li>
                        </ol>
                        <p style="margin-top: 1.5rem; font-size: 0.9rem; opacity: 0.8;">
                            Or connect directly: 
                            <a href="https://github.com/datnguye" target="_blank" style="color: var(--primary); margin: 0 0.5rem;">GitHub</a> | 
                            <a href="https://www.linkedin.com/in/datnguye/" target="_blank" style="color: var(--primary); margin: 0 0.5rem;">LinkedIn</a>
                        </p>
                    </div>
                `;
            }
        }, 3000);
    };
    
    const script = document.createElement('script');
    script.src = 'https://giscus.app/client.js';
    script.setAttribute('data-repo', 'datnguye/about');
    script.setAttribute('data-repo-id', 'R_kgDOPUfCtQ');
    script.setAttribute('data-category', 'Blogpost');
    script.setAttribute('data-category-id', 'DIC_kwDOPUfCtc4Ct2JY');
    script.setAttribute('data-mapping', 'pathname');
    script.setAttribute('data-strict', '1');
    script.setAttribute('data-reactions-enabled', '1');
    script.setAttribute('data-emit-metadata', '0');
    script.setAttribute('data-input-position', 'bottom');
    script.setAttribute('data-theme', 'dark');
    script.setAttribute('data-lang', 'en');
    script.crossOrigin = 'anonymous';
    script.async = true;
    
    commentsSection.appendChild(script);
    checkDiscussions();
}

function getGiscusTheme() {
    return 'dark';  // Always use dark theme
}

document.addEventListener('DOMContentLoaded', () => {
    initGiscusComments();
});