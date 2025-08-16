document.addEventListener('DOMContentLoaded',()=>{
  // Animate progress bars on scroll
  const observer=new IntersectionObserver((entries)=>{
    entries.forEach(entry=>{
      if(entry.isIntersecting){
        const progressBars=entry.target.querySelectorAll('.progress');
        progressBars.forEach(bar=>{
          const width=bar.style.width;
          bar.style.width='0';
          setTimeout(()=>{
            bar.style.width=width
          },100)
        })
      }
    })
  },{threshold:0.1});
  
  document.querySelectorAll('.resume-section').forEach(section=>{
    observer.observe(section)
  });

  // Add copy-to-clipboard functionality for header anchors (h2-h6)
  function addAnchorCopyButtons() {
    const headers = document.querySelectorAll('.article-content h2, .article-content h3, .article-content h4, .article-content h5, .article-content h6');
    
    headers.forEach(header => {
      if (header.id) {
        // Create anchor copy button
        const copyButton = document.createElement('button');
        copyButton.className = 'header-anchor-copy';
        copyButton.innerHTML = '<i class="fas fa-link"></i>';
        copyButton.title = 'Copy link to section';
        copyButton.setAttribute('aria-label', 'Copy link to this section');
        
        // Position button relative to header
        header.style.position = 'relative';
        header.appendChild(copyButton);
        
        // Add click event to copy URL with hash
        copyButton.addEventListener('click', async (e) => {
          e.preventDefault();
          const url = window.location.origin + window.location.pathname + '#' + header.id;
          
          try {
            await navigator.clipboard.writeText(url);
            
            // Visual feedback - success
            const originalIcon = copyButton.innerHTML;
            copyButton.innerHTML = '<i class="fas fa-check"></i>';
            copyButton.style.color = '#10b981'; // green color
            
            setTimeout(() => {
              copyButton.innerHTML = originalIcon;
              copyButton.style.color = '';
            }, 2000);
            
          } catch (err) {
            console.warn('Could not copy to clipboard:', err);
            
            // Visual feedback - error
            const originalIcon = copyButton.innerHTML;
            copyButton.innerHTML = '<i class="fas fa-exclamation"></i>';
            copyButton.style.color = '#ef4444'; // red color
            
            setTimeout(() => {
              copyButton.innerHTML = originalIcon;
              copyButton.style.color = '';
            }, 2000);
          }
        });
      }
    });
  }
  
  // Initialize anchor copy buttons
  addAnchorCopyButtons();

  // Show NEW badge for articles published within 7 days
  function initNewBadges() {
    const badgeElements = document.querySelectorAll('.new-badge-check');
    if (!badgeElements.length) return;

    const now = Date.now();
    const sevenDays = 7 * 24 * 60 * 60 * 1000;
    
    badgeElements.forEach(el => {
      const dateStr = el.dataset.postDate;
      if (!dateStr) return;
      
      const postTime = dateStr.length === 10 && dateStr.includes('-') 
        ? new Date(dateStr + 'T00:00:00').getTime()
        : new Date(dateStr).getTime();
      
      if (postTime >= (now - sevenDays) && postTime <= now) {
        el.className = 'new-badge';
        el.hidden = false;
      }
    });
  }

  initNewBadges();
})