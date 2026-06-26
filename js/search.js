// Search functionality
let searchData = [];

// Initialize search data with site content
async function initializeSearchData() {
    // Clear existing data
    searchData = [];
    
    // Fetch and parse blog posts from the blog page
    try {
        const response = await fetch('/blog/');
        const html = await response.text();
        const parser = new DOMParser();
        const doc = parser.parseFromString(html, 'text/html');
        
        // Add blog index page
        const blogTitle = doc.querySelector('h1')?.textContent;
        const blogDesc = doc.querySelector('header p')?.textContent;
        if (blogTitle) {
            searchData.push({
                url: '/blog/',
                title: blogTitle,
                body: blogDesc || '',
                type: 'page'
            });
        }
        
        // Extract blog posts from the blog page
        const articles = doc.querySelectorAll('article');
        articles.forEach(article => {
            const titleEl = article.querySelector('h2 a');
            const descEl = article.querySelector('p');
            const tagsEls = article.querySelectorAll('span[class*="bg-"][class*="primary"]');
            
            if (titleEl && descEl) {
                const tags = Array.from(tagsEls).map(el => el.textContent.replace('#', '').trim());
                const url = titleEl.href || titleEl.getAttribute('href');
                const absoluteUrl = url.startsWith('http') ? url : new URL(url, window.location.origin).href;
                
                searchData.push({
                    url: absoluteUrl,
                    title: titleEl.textContent.trim(),
                    body: descEl.textContent.trim() + ' ' + tags.join(' '),
                    type: 'blog'
                });
            }
        });
    } catch (error) {
        console.log('Could not fetch blog posts:', error);
    }
    
    // Fetch and parse resume/home page
    try {
        const response = await fetch('/');
        const html = await response.text();
        const parser = new DOMParser();
        const doc = parser.parseFromString(html, 'text/html');
        
        // Extract resume content
        const nameEl = doc.querySelector('h1');
        const titleEl = doc.querySelector('h2');
        const bioEl = doc.querySelector('.text-base.opacity-90');
        
        // Get skills from the page
        const skillElements = doc.querySelectorAll('.bg-\\[var\\(--primary\\)\\].bg-opacity-10.px-3.py-1.rounded-full.text-xs');
        const skills = Array.from(skillElements).map(el => el.textContent.trim());
        
        // Get experience titles
        const experienceElements = doc.querySelectorAll('.timeline-item h3');
        const experiences = Array.from(experienceElements).map(el => el.textContent.trim());
        
        const resumeBody = [
            nameEl ? nameEl.textContent : '',
            titleEl ? titleEl.textContent : '',
            bioEl ? bioEl.textContent : '',
            ...skills,
            ...experiences
        ].filter(text => text).join(' ');
        
        if (doc.title) {
            searchData.push({
                url: '/',
                title: doc.title,
                body: resumeBody,
                type: 'page'
            });
        }
    } catch (error) {
        console.log('Could not fetch resume page:', error);
    }
}

// Perform search
function performSearch(query) {
    if (!query.trim() || searchData.length === 0) {
        return [];
    }
    
    const lowerQuery = query.toLowerCase();
    const results = [];
    
    // Simple search implementation
    searchData.forEach(doc => {
        const titleMatch = doc.title.toLowerCase().includes(lowerQuery);
        const bodyMatch = doc.body.toLowerCase().includes(lowerQuery);
        
        if (titleMatch || bodyMatch) {
            let score = 0;
            if (titleMatch) score += 2;
            if (bodyMatch) score += 1;
            
            results.push({
                ...doc,
                score: score
            });
        }
    });
    
    // Sort by score
    return results.sort((a, b) => b.score - a.score);
}

// Display search results
function displaySearchResults(results, query) {
    const resultsContainer = document.getElementById('search-results-content');
    const searchResultsDiv = document.getElementById('search-results');
    
    if (results.length === 0) {
        resultsContainer.innerHTML = `<p class="text-sm opacity-60">No results found for "${query}"</p>`;
    } else {
        resultsContainer.innerHTML = results.map(result => {
            // Highlight matching text
            const highlightedTitle = highlightText(result.title, query);
            const snippet = createSnippet(result.body, query, 150);
            const highlightedSnippet = highlightText(snippet, query);
            
            // Check if it's an external link
            const isExternal = result.url.startsWith('http');
            const iconClass = isExternal ? 'fa-external-link-alt' : 'fa-arrow-right';
            
            return `
                <a href="${result.url}" ${isExternal ? 'target="_blank" rel="noopener noreferrer"' : ''} 
                   class="block p-3 rounded-lg hover:bg-[var(--background)] transition-colors">
                    <h4 class="font-semibold text-sm mb-1">${highlightedTitle}</h4>
                    <p class="text-xs opacity-70">${highlightedSnippet}</p>
                    <span class="text-xs text-[var(--primary)] mt-1 inline-flex items-center gap-1">
                        <i class="fas ${iconClass} text-xs"></i>
                    </span>
                </a>
            `;
        }).join('');
    }
    
    // Show results
    searchResultsDiv.classList.remove('hidden');
}

// Create snippet around search term
function createSnippet(text, query, maxLength) {
    const lowerText = text.toLowerCase();
    const lowerQuery = query.toLowerCase();
    const index = lowerText.indexOf(lowerQuery);
    
    if (index === -1) {
        return text.substring(0, maxLength) + '...';
    }
    
    const start = Math.max(0, index - 50);
    const end = Math.min(text.length, index + query.length + 100);
    
    let snippet = text.substring(start, end);
    if (start > 0) snippet = '...' + snippet;
    if (end < text.length) snippet = snippet + '...';
    
    return snippet;
}

// Highlight matching text
function highlightText(text, query) {
    const regex = new RegExp(`(${query})`, 'gi');
    return text.replace(regex, '<mark class="bg-[var(--primary)] bg-opacity-30 px-1 rounded">$1</mark>');
}

// Initialize search when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    // Initialize search data asynchronously
    initializeSearchData();
    
    const searchInput = document.getElementById('search-input');
    const searchButton = document.getElementById('search-button');
    const searchResults = document.getElementById('search-results');
    const closeSearch = document.getElementById('close-search');
    
    if (!searchInput || !searchButton) return;
    
    // Search on input
    let searchTimeout;
    searchInput.addEventListener('input', function(e) {
        clearTimeout(searchTimeout);
        const query = e.target.value;
        
        if (query.length < 2) {
            searchResults.classList.add('hidden');
            return;
        }
        
        searchTimeout = setTimeout(() => {
            const results = performSearch(query);
            displaySearchResults(results, query);
        }, 300);
    });
    
    // Search on button click
    searchButton.addEventListener('click', function() {
        const query = searchInput.value;
        if (query.length >= 2) {
            const results = performSearch(query);
            displaySearchResults(results, query);
        }
    });
    
    // Close search results
    if (closeSearch) {
        closeSearch.addEventListener('click', function() {
            searchResults.classList.add('hidden');
            searchInput.value = '';
        });
    }
    
    // Close on outside click
    document.addEventListener('click', function(e) {
        if (!searchResults.contains(e.target) && !searchInput.contains(e.target) && !searchButton.contains(e.target)) {
            searchResults.classList.add('hidden');
        }
    });
    
    // Handle Enter key
    searchInput.addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            e.preventDefault();
            const query = searchInput.value;
            if (query.length >= 2) {
                const results = performSearch(query);
                displaySearchResults(results, query);
            }
        }
    });
});