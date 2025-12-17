/*
 * JavaScript pour l'interactivité de l'application - Version Élégante & Moderne
 * Animations avancées, effets visuels et interactions fluides
 */

// Animations au chargement de la page
document.addEventListener('DOMContentLoaded', function() {
    // Animation fade-in pour tous les éléments
    const fadeElements = document.querySelectorAll('.card, .stat-card, .product-card');
    fadeElements.forEach((el, index) => {
        el.style.opacity = '0';
        el.style.transform = 'translateY(30px)';
        setTimeout(() => {
            el.style.transition = 'all 0.6s cubic-bezier(0.4, 0, 0.2, 1)';
            el.style.opacity = '1';
            el.style.transform = 'translateY(0)';
        }, index * 100);
    });

    // Effet de particules sur le fond
    createParticles();
    
    // Animation smooth scroll
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
});

// Fonction utilitaire pour les requêtes AJAX
async function apiRequest(url, method = 'GET', data = null) {
    const options = {
        method: method,
        headers: {
            'Content-Type': 'application/json',
        }
    };
    
    if (data) {
        options.body = JSON.stringify(data);
    }
    
    try {
        const response = await fetch(url, options);
        const result = await response.json();
        return result;
    } catch (error) {
        console.error('Erreur API:', error);
        throw error;
    }
}

// Fonction pour créer des particules en arrière-plan
function createParticles() {
    const particleCount = 30;
    const body = document.body;
    
    for (let i = 0; i < particleCount; i++) {
        const particle = document.createElement('div');
        particle.style.position = 'fixed';
        particle.style.width = Math.random() * 5 + 2 + 'px';
        particle.style.height = particle.style.width;
        particle.style.background = 'rgba(255, 255, 255, 0.5)';
        particle.style.borderRadius = '50%';
        particle.style.left = Math.random() * 100 + '%';
        particle.style.top = Math.random() * 100 + '%';
        particle.style.pointerEvents = 'none';
        particle.style.zIndex = '0';
        particle.style.animation = `float ${Math.random() * 10 + 10}s ease-in-out infinite`;
        particle.style.animationDelay = Math.random() * 5 + 's';
        body.appendChild(particle);
    }
}

// Animation CSS pour les particules
const style = document.createElement('style');
style.textContent = `
    @keyframes float {
        0%, 100% {
            transform: translate(0, 0) scale(1);
            opacity: 0.5;
        }
        50% {
            transform: translate(${Math.random() * 100 - 50}px, ${Math.random() * 100 - 50}px) scale(1.2);
            opacity: 0.8;
        }
    }
`;
document.head.appendChild(style);

// Gestion du drag & drop pour l'upload
document.addEventListener('DOMContentLoaded', function() {
    const uploadZone = document.querySelector('.upload-zone');
    
    if (uploadZone) {
        ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
            uploadZone.addEventListener(eventName, preventDefaults, false);
        });
        
        function preventDefaults(e) {
            e.preventDefault();
            e.stopPropagation();
        }
        
        ['dragenter', 'dragover'].forEach(eventName => {
            uploadZone.addEventListener(eventName, () => {
                uploadZone.classList.add('dragging');
            }, false);
        });
        
        ['dragleave', 'drop'].forEach(eventName => {
            uploadZone.addEventListener(eventName, () => {
                uploadZone.classList.remove('dragging');
            }, false);
        });
        
        uploadZone.addEventListener('drop', handleDrop, false);
        
        function handleDrop(e) {
            const dt = e.dataTransfer;
            const files = dt.files;
            handleFiles(files);
        }
        
        function handleFiles(files) {
            const fileInput = document.getElementById('file');
            if (fileInput) {
                fileInput.files = files;
                const event = new Event('change', { bubbles: true });
                fileInput.dispatchEvent(event);
            }
        }
    }
    
    // Afficher le nom du fichier sélectionné
    const fileInput = document.getElementById('file');
    if (fileInput) {
        fileInput.addEventListener('change', function(e) {
            const fileName = e.target.files[0]?.name || 'Aucun fichier sélectionné';
            const label = document.querySelector('.upload-zone p');
            if (label) {
                label.textContent = `Fichier: ${fileName}`;
            }
        });
    }
});

// Confirmation avant suppression
function confirmDelete(message = 'Êtes-vous sûr de vouloir supprimer cet élément ?') {
    return confirm(message);
}

// Auto-fermeture des alerts après 5 secondes
document.addEventListener('DOMContentLoaded', function() {
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(alert => {
        setTimeout(() => {
            alert.style.opacity = '0';
            setTimeout(() => alert.remove(), 300);
        }, 5000);
    });
});

// Validation des formulaires côté client
function validateForm(formId) {
    const form = document.getElementById(formId);
    if (!form) return true;
    
    const inputs = form.querySelectorAll('input[required], textarea[required], select[required]');
    let isValid = true;
    
    inputs.forEach(input => {
        if (!input.value.trim()) {
            input.classList.add('is-invalid');
            isValid = false;
        } else {
            input.classList.remove('is-invalid');
        }
    });
    
    return isValid;
}

// Chargement des statistiques du dashboard (AJAX)
async function loadDashboardStats() {
    try {
        const data = await apiRequest('/api/stats/dashboard');
        if (data.success) {
            updateDashboardUI(data.stats);
        }
    } catch (error) {
        console.error('Erreur lors du chargement des statistiques:', error);
    }
}

function updateDashboardUI(stats) {
    // Mise à jour des compteurs
    if (document.getElementById('total-users')) {
        document.getElementById('total-users').textContent = stats.total_users;
    }
    if (document.getElementById('total-products')) {
        document.getElementById('total-products').textContent = stats.total_products;
    }
    if (document.getElementById('total-uploads')) {
        document.getElementById('total-uploads').textContent = stats.total_uploads;
    }
    if (document.getElementById('total-activities')) {
        document.getElementById('total-activities').textContent = stats.total_activities;
    }
}

// Recherche en temps réel pour les produits
let searchTimeout;
function searchProducts(query) {
    clearTimeout(searchTimeout);
    searchTimeout = setTimeout(async () => {
        try {
            const data = await apiRequest(`/api/products?search=${encodeURIComponent(query)}`);
            if (data.success) {
                displayProducts(data.products);
            }
        } catch (error) {
            console.error('Erreur de recherche:', error);
        }
    }, 300);
}

function displayProducts(products) {
    const container = document.getElementById('products-container');
    if (!container) return;
    
    if (products.length === 0) {
        container.innerHTML = '<p class="text-center">Aucun produit trouvé</p>';
        return;
    }
    
    container.innerHTML = products.map(product => `
        <div class="product-card">
            <img src="${product.image_url || '/static/images/placeholder.png'}" 
                 alt="${product.name}" class="product-image">
            <div class="product-body">
                <h3 class="product-title">${product.name}</h3>
                <p class="product-price">${product.price.toFixed(2)} €</p>
                <p>${product.description || ''}</p>
                <div class="product-actions">
                    <a href="/products/${product.id}" class="btn btn-primary btn-sm">Voir</a>
                    <a href="/products/${product.id}/edit" class="btn btn-secondary btn-sm">Modifier</a>
                </div>
            </div>
        </div>
    `).join('');
}

// Animation smooth scroll
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({
                behavior: 'smooth'
            });
        }
    });
});

// Chargement initial du dashboard si on est sur la page
if (window.location.pathname.includes('dashboard')) {
    loadDashboardStats();
    // Rafraîchir toutes les 30 secondes
    setInterval(loadDashboardStats, 30000);
}
