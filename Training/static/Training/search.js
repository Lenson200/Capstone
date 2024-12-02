document.addEventListener('DOMContentLoaded', function () {
    const searchForm = document.querySelector('#search-form');
    const resultsContainer = document.querySelector('.results');
    
    if (!searchForm) {
        return;
    }
    const searchUrl = searchForm.getAttribute('action');
    const searchInput = searchForm.querySelector('input[name="q"]');
    searchInput.addEventListener('input', () => {
        const query = searchInput.value.trim();
        if (!searchInput) {return;
        }
        if (query === '') {
            return;
        }
    });

    searchForm.addEventListener('submit', (event) => {
        event.preventDefault(); 
        const query = searchInput.value.trim();

        // Hide results by default
        resultsContainer.classList.remove('active');
        resultsContainer.innerHTML = '';

        if (!query) {
            return;
        }

        fetch(`${searchUrl}?q=${encodeURIComponent(query)}`, {
            headers: { 'X-Requested-With': 'XMLHttpRequest' }
        })
        .then(response => {
            if (!response.ok) throw new Error('Network response was not ok');
            return response.json();
        })
        .then(data => {
            if (data.results.length > 0) {
                resultsContainer.classList.add('active'); // Show results
                data.results.forEach(result => {
                    const item = document.createElement('div');
                    item.className = 'result-item';
                    item.innerHTML = `
                        <a href="${result.url}">
                            <strong>${result.type}:</strong> ${result.name} - ${result.description}
                        </a>`;
                    resultsContainer.appendChild(item);
                    
                });
                
            } else {
                resultsContainer.classList.add('active'); // Show message
                resultsContainer.innerHTML = '<p>No results found.</p>';
            }
        })
        .catch(error => {
            console.error('Error:', error);
            resultsContainer.classList.add('active'); // Show error message
            resultsContainer.innerHTML = '<p>Error processing your request. Please try again.</p>';
        });
    });
});