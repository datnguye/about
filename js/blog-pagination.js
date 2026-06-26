// Blog pagination functionality
document.addEventListener('DOMContentLoaded', function() {
    const postsPerPage = 6; // Match the paginate_by value in _index.md
    const articles = Array.from(document.querySelectorAll('.grid > article'));
    const totalPosts = articles.length;
    const totalPages = Math.ceil(totalPosts / postsPerPage);
    
    // Get current page from URL parameter
    const urlParams = new URLSearchParams(window.location.search);
    const currentPage = parseInt(urlParams.get('page')) || 1;
    
    // Hide all articles first
    articles.forEach(article => {
        article.style.display = 'none';
    });
    
    // Show only articles for current page
    const startIndex = (currentPage - 1) * postsPerPage;
    const endIndex = startIndex + postsPerPage;
    
    articles.slice(startIndex, endIndex).forEach(article => {
        article.style.display = '';
    });
    
    // Create pagination controls
    if (totalPages > 1) {
        const nav = document.createElement('nav');
        nav.className = 'mt-12 flex justify-center items-center space-x-4';
        nav.id = 'pagination-controls';
        
        // Previous button
        const prevElement = currentPage > 1 ? 
            createLink(`/blog/${currentPage > 1 ? `?page=${currentPage - 1}` : ''}`, 'Previous', 'fa-chevron-left', true) :
            createDisabledButton('Previous', 'fa-chevron-left', true);
        nav.appendChild(prevElement);
        
        // Page numbers container
        const pageContainer = document.createElement('div');
        pageContainer.className = 'flex items-center space-x-2';
        
        for (let page = 1; page <= totalPages; page++) {
            if (page === currentPage) {
                const span = document.createElement('span');
                span.className = 'w-10 h-10 flex items-center justify-center bg-[var(--primary)] text-white rounded-lg font-semibold';
                span.textContent = page;
                pageContainer.appendChild(span);
            } else {
                const link = document.createElement('a');
                link.href = `/blog/${page > 1 ? `?page=${page}` : ''}`;
                link.className = 'w-10 h-10 flex items-center justify-center bg-[var(--card)] hover:bg-[var(--primary)] hover:text-white rounded-lg transition-colors';
                link.textContent = page;
                pageContainer.appendChild(link);
            }
        }
        nav.appendChild(pageContainer);
        
        // Next button
        const nextElement = currentPage < totalPages ?
            createLink(`/blog/?page=${currentPage + 1}`, 'Next', 'fa-chevron-right', false) :
            createDisabledButton('Next', 'fa-chevron-right', false);
        nav.appendChild(nextElement);
        
        // Insert pagination controls after the grid
        const grid = document.querySelector('.grid');
        if (grid && !document.getElementById('pagination-controls')) {
            grid.insertAdjacentElement('afterend', nav);
        }
    }
    
    // Update page info display
    if (totalPages > 1 && currentPage > 1) {
        const pageInfo = document.querySelector('header h1');
        if (pageInfo) {
            pageInfo.textContent += ` - Page ${currentPage}`;
        }
    }
});

// Helper function to create a link button
function createLink(href, text, iconClass, iconBefore) {
    const link = document.createElement('a');
    link.href = href;
    link.className = 'px-4 py-2 bg-[var(--card)] rounded-lg hover:bg-[var(--primary)] hover:text-white transition-colors';
    
    const icon = document.createElement('i');
    icon.className = `fas ${iconClass} ${iconBefore ? 'mr-2' : 'ml-2'}`;
    
    if (iconBefore) {
        link.appendChild(icon);
        link.appendChild(document.createTextNode(text));
    } else {
        link.appendChild(document.createTextNode(text));
        link.appendChild(icon);
    }
    
    return link;
}

// Helper function to create a disabled button
function createDisabledButton(text, iconClass, iconBefore) {
    const span = document.createElement('span');
    span.className = 'px-4 py-2 bg-[var(--card)] rounded-lg opacity-50 cursor-not-allowed';
    
    const icon = document.createElement('i');
    icon.className = `fas ${iconClass} ${iconBefore ? 'mr-2' : 'ml-2'}`;
    
    if (iconBefore) {
        span.appendChild(icon);
        span.appendChild(document.createTextNode(text));
    } else {
        span.appendChild(document.createTextNode(text));
        span.appendChild(icon);
    }
    
    return span;
}