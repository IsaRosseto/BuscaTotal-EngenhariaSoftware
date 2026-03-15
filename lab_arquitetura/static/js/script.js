document.addEventListener('DOMContentLoaded', () => {
    const searchForm = document.getElementById('searchForm');
    const searchInput = document.getElementById('searchInput');
    const clearBtn = document.getElementById('clearBtn');
    const searchButton = document.querySelector('.search-button');
    const resultsGrid = document.getElementById('resultsGrid');
    const statsContainer = document.getElementById('statsContainer');
    const statsText = document.getElementById('statsText');

    // States elements
    const loadingState = document.getElementById('loadingState');
    const errorState = document.getElementById('errorState');
    const errorMessage = document.getElementById('errorMessage');
    const emptyState = document.getElementById('emptyState');

    // Show/Hide Clear Button
    searchInput.addEventListener('input', () => {
        if (searchInput.value.trim().length > 0) {
            clearBtn.classList.add('visible');
        } else {
            clearBtn.classList.remove('visible');
        }
    });

    // Clear Input
    clearBtn.addEventListener('click', () => {
        searchInput.value = '';
        searchInput.focus();
        clearBtn.classList.remove('visible');
    });

    // Helper functions for UI States
    const hideAllStates = () => {
        resultsGrid.innerHTML = '';
        loadingState.classList.add('hidden');
        errorState.classList.add('hidden');
        emptyState.classList.add('hidden');
        statsContainer.classList.add('hidden');
    };

    const showLoading = () => {
        hideAllStates();
        searchButton.classList.add('loading');
        searchButton.disabled = true;
        searchInput.disabled = true;
        loadingState.classList.remove('hidden');
    };

    const stopLoading = () => {
        searchButton.classList.remove('loading');
        searchButton.disabled = false;
        searchInput.disabled = false;
    };

    const showError = (msg) => {
        hideAllStates();
        stopLoading();
        errorMessage.textContent = msg;
        errorState.classList.remove('hidden');
    };

    const showEmpty = () => {
        hideAllStates();
        stopLoading();
        emptyState.classList.remove('hidden');
    };

    // Card UI Generator
    const createProductCard = (product) => {
        const formatter = new Intl.NumberFormat('pt-BR', {
            style: 'currency',
            currency: product.currency
        });

        const priceFormatted = formatter.format(product.price);
        const conditionText = product.condition === 'new' ? 'Novo' : 'Usado';

        return `
            <a href="${product.permalink}" target="_blank" rel="noopener noreferrer" class="product-card">
                <div class="card-image-wrapper">
                    <span class="condition-badge">${conditionText}</span>
                    <img src="${product.thumbnail}" alt="${product.title}" class="card-image" loading="lazy">
                </div>
                <div class="card-content">
                    <h3 class="card-title" title="${product.title}">${product.title}</h3>
                    <div class="card-price">${priceFormatted}</div>
                    
                    <div class="card-footer">
                        <span class="store-name">📦 Mercado Livre</span>
                        <span class="buy-btn-text">Ver Oferta ➜</span>
                    </div>
                </div>
            </a>
        `;
    };

    const handleSearch = async (query) => {
        if (!query.trim()) return;

        showLoading();

        try {
            // Chamando a API do Flask que injeta as dependências e consome o ML
            const response = await fetch(`/api/search?q=${encodeURIComponent(query)}`);

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.error || 'Erro na comunicação com o backend.');
            }

            const data = await response.json();
            stopLoading();
            hideAllStates();

            if (data.results.length === 0) {
                showEmpty();
                return;
            }

            // Exibir estatísticas
            statsText.innerHTML = `O <b>IntelligenceProcessor</b> filtrou os dados impuros e encontrou <b>${data.count}</b> ofertas fidedignas para "${data.query}".`;
            statsContainer.classList.remove('hidden');

            // Renderizar Grid
            const cardsHtml = data.results.map(prod => createProductCard(prod)).join('');
            resultsGrid.innerHTML = cardsHtml;

        } catch (error) {
            console.error('Busca Error:', error);
            showError(`Falha ao realizar busca: ${error.message}`);
        }
    };

    // Form Submission
    searchForm.addEventListener('submit', (e) => {
        e.preventDefault();
        handleSearch(searchInput.value);
    });
});
