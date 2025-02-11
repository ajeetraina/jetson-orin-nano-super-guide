// Add copy button to code blocks
document.querySelectorAll('pre code').forEach((block) => {
    // Create copy button
    const button = document.createElement('button');
    button.className = 'md-clipboard md-icon';
    button.title = 'Copy to clipboard';
    
    // Add click handler
    button.addEventListener('click', () => {
        navigator.clipboard.writeText(block.textContent).then(() => {
            button.title = 'Copied!';
            setTimeout(() => {
                button.title = 'Copy to clipboard';
            }, 2000);
        });
    });
    
    block.parentNode.insertBefore(button, block);
});

// Add version selector
const versions = document.querySelector('.md-version-select');
if (versions) {
    versions.addEventListener('change', (e) => {
        window.location.href = e.target.value;
    });
}

// Add search highlighting
document.addEventListener('DOMContentLoaded', () => {
    const params = new URLSearchParams(window.location.search);
    const query = params.get('q');
    if (query) {
        const regex = new RegExp(query, 'gi');
        document.querySelectorAll('.md-content article').forEach((article) => {
            article.innerHTML = article.innerHTML.replace(
                regex,
                '<mark>$&</mark>'
            );
        });
    }
});
