// AI Dictionary JavaScript functionality

document.addEventListener('DOMContentLoaded', function() {
    const searchForm = document.getElementById('searchForm');
    const wordInput = document.getElementById('wordInput');
    const searchBtn = document.getElementById('searchBtn');
    const loadingCard = document.getElementById('loadingCard');
    const welcomeCard = document.getElementById('welcomeCard');
    const resultsCard = document.getElementById('resultsCard');

    // Focus on input when page loads
    if (wordInput) {
        wordInput.focus();
    }

    // Handle form submission with loading state
    if (searchForm) {
        searchForm.addEventListener('submit', function(e) {
            const word = wordInput.value.trim();
            
            // Basic client-side validation
            if (!word) {
                e.preventDefault();
                showAlert('Please enter a word to search for.', 'warning');
                wordInput.focus();
                return;
            }

            if (word.length > 50) {
                e.preventDefault();
                showAlert('Word is too long. Please enter a shorter word.', 'warning');
                wordInput.focus();
                return;
            }

            // Check for valid characters (letters, hyphens, apostrophes)
            if (!/^[a-zA-Z\-']+$/.test(word)) {
                e.preventDefault();
                showAlert('Please enter a valid word (letters, hyphens, and apostrophes only).', 'warning');
                wordInput.focus();
                return;
            }

            // Show loading state
            showLoadingState();
        });
    }

    // Auto-focus on input when "Search Another Word" is clicked
    const searchAnotherBtn = document.querySelector('button[onclick*="wordInput"]');
    if (searchAnotherBtn) {
        searchAnotherBtn.addEventListener('click', function() {
            if (wordInput) {
                wordInput.select();
            }
        });
    }

    // Handle enter key in input
    if (wordInput) {
        wordInput.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                e.preventDefault();
                searchForm.dispatchEvent(new Event('submit', { cancelable: true }));
            }
        });

        // Clear any previous error styling on input
        wordInput.addEventListener('input', function() {
            this.classList.remove('is-invalid');
        });
    }

    // Auto-dismiss alerts after 5 seconds
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(alert => {
        if (!alert.querySelector('.btn-close')) return;
        
        setTimeout(() => {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        }, 5000);
    });

    // Function to show loading state
    function showLoadingState() {
        if (loadingCard && welcomeCard) {
            welcomeCard.classList.add('d-none');
            loadingCard.classList.remove('d-none');
        }
        
        if (resultsCard) {
            resultsCard.style.opacity = '0.5';
        }

        // Disable form during loading
        if (searchBtn) {
            searchBtn.disabled = true;
            searchBtn.innerHTML = '<i class="fas fa-spinner fa-spin me-2"></i>Searching...';
        }
        
        if (wordInput) {
            wordInput.disabled = true;
        }
    }

    // Function to show alert messages
    function showAlert(message, type = 'info') {
        const alertContainer = document.querySelector('.container > .alert');
        if (alertContainer) {
            alertContainer.remove();
        }

        const alertDiv = document.createElement('div');
        alertDiv.className = `alert alert-${type === 'error' ? 'danger' : type} alert-dismissible fade show`;
        alertDiv.setAttribute('role', 'alert');
        
        const iconClass = type === 'error' ? 'exclamation-triangle' : 
                         type === 'warning' ? 'exclamation-circle' : 'info-circle';
        
        alertDiv.innerHTML = `
            <i class="fas fa-${iconClass} me-2"></i>
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
        `;

        const container = document.querySelector('.container');
        const firstChild = container.firstElementChild;
        container.insertBefore(alertDiv, firstChild);

        // Auto-dismiss after 5 seconds
        setTimeout(() => {
            const bsAlert = new bootstrap.Alert(alertDiv);
            bsAlert.close();
        }, 5000);
    }

    // Smooth scroll to results when they appear
    if (resultsCard && !resultsCard.classList.contains('d-none')) {
        setTimeout(() => {
            resultsCard.scrollIntoView({ 
                behavior: 'smooth', 
                block: 'start' 
            });
        }, 100);
    }

    // Add keyboard shortcuts
    document.addEventListener('keydown', function(e) {
        // Ctrl/Cmd + K to focus search
        if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
            e.preventDefault();
            if (wordInput) {
                wordInput.focus();
                wordInput.select();
            }
        }
        
        // Escape to clear input
        if (e.key === 'Escape' && document.activeElement === wordInput) {
            wordInput.value = '';
        }
    });

    // Add search suggestions (simple implementation)
    if (wordInput) {
        let timeout;
        wordInput.addEventListener('input', function() {
            clearTimeout(timeout);
            const value = this.value.trim();
            
            // Remove invalid characters as user types
            this.value = value.replace(/[^a-zA-Z\-']/g, '');
        });
    }

    // Preload common words or provide quick access
    const commonWords = ['serendipity', 'ephemeral', 'ubiquitous', 'eloquent', 'meticulous'];
    
    // Add quick search suggestions (optional enhancement)
    function addQuickSuggestions() {
        if (!welcomeCard || resultsCard) return;
        
        const suggestionsDiv = document.createElement('div');
        suggestionsDiv.className = 'mt-4';
        suggestionsDiv.innerHTML = `
            <h6 class="text-muted mb-3">Try these words:</h6>
            <div class="d-flex flex-wrap gap-2">
                ${commonWords.map(word => 
                    `<button class="btn btn-outline-secondary btn-sm quick-search" data-word="${word}">${word}</button>`
                ).join('')}
            </div>
        `;
        
        welcomeCard.querySelector('.card-body').appendChild(suggestionsDiv);
        
        // Add click handlers for quick search
        suggestionsDiv.querySelectorAll('.quick-search').forEach(btn => {
            btn.addEventListener('click', function() {
                const word = this.getAttribute('data-word');
                if (wordInput) {
                    wordInput.value = word;
                    searchForm.dispatchEvent(new Event('submit', { cancelable: true }));
                }
            });
        });
    }

    // Add quick suggestions if we're on the welcome screen
    if (welcomeCard && !welcomeCard.classList.contains('d-none')) {
        addQuickSuggestions();
    }
});

// Utility function to copy text to clipboard
function copyToClipboard(text) {
    navigator.clipboard.writeText(text).then(function() {
        showAlert('Text copied to clipboard!', 'success');
    }).catch(function() {
        showAlert('Failed to copy text to clipboard.', 'error');
    });
}

// Add copy functionality to definitions (enhancement)
document.addEventListener('DOMContentLoaded', function() {
    const definitionElements = document.querySelectorAll('.fs-5');
    definitionElements.forEach(el => {
        el.style.cursor = 'pointer';
        el.title = 'Click to copy definition';
        el.addEventListener('click', function() {
            copyToClipboard(this.textContent);
        });
    });
});
