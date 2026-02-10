const backToTopButton = document.getElementById('backToTop');

window.addEventListener('scroll', () => {
    if (window.pageYOffset > 300) {
        backToTopButton.style.display = 'block';
    } else {
        backToTopButton.style.display = 'none';
    }
});

backToTopButton.addEventListener('click', () => {
    window.scrollTo({
        top: 0,
        behavior: 'smooth'
    });
});

// Gestion du formulaire newsletter
const newsletterForm = document.getElementById('newsletter-form');
if (newsletterForm) {
    newsletterForm.addEventListener('submit', function(e) {
        e.preventDefault();
        const email = this.querySelector('input[type="email"]').value;
        
        // Ici, normalement on enverrait les données à un serveur
        // Pour l'exemple, on simule un envoi réussi
        alert(`Merci de vous être inscrit avec l'adresse: ${email}\nVous recevrez bientôt nos actualités.`);
        this.reset();
    });
}

// Animation au défilement
function isElementInViewport(el) {
    const rect = el.getBoundingClientRect();
    return (
        rect.top <= (window.innerHeight || document.documentElement.clientHeight) * 0.8
    );
}

function handleScrollAnimation() {
    const elements = document.querySelectorAll('.service-card, .news-card, .info-box');
    
    elements.forEach(element => {
        if (isElementInViewport(element)) {
            element.classList.add('animated');
        }
    });
}

// Initialiser l'animation au chargement
document.addEventListener('DOMContentLoaded', function() {
    // Ajouter une classe pour déclencher les animations CSS
    setTimeout(() => {
        document.body.classList.add('loaded');
    }, 100);
    
    // Gérer l'animation au défilement
    window.addEventListener('scroll', handleScrollAnimation);
    handleScrollAnimation(); // Vérifier au chargement initial
    
    // Menu actif basé sur la page courante
    const currentPage = window.location.pathname.split('/').pop() || 'index.html';
    const navLinks = document.querySelectorAll('.nav-link');
    
    navLinks.forEach(link => {
        const linkPage = link.getAttribute('href');
        if (currentPage === linkPage || 
            (currentPage === '' && linkPage === 'index.html') ||
            (currentPage.includes(linkPage.replace('.html', '')) && linkPage !== 'index.html')) {
            link.classList.add('active');
        } else {
            link.classList.remove('active');
        }
    });
    
    // Initialiser les tooltips Bootstrap
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
});

// Données des lieux touristiques
const touristPlaces = [
    {
        id: 1,
        name: "Basilique Notre-Dame de la Paix",
        category: "culture",
        image: "images/basilique.jpg",
        description: "La plus grande basilique au monde, chef-d'œuvre architectural.",
        rating: 4.8,
        icon: "fas fa-church",
        features: ["Architecture unique", "Vue panoramique", "Visites guidées"]
    },
    {
        id: 2,
        name: "Le Plateau",
        category: "culture",
        image: "images/plateau.jpg",
        description: "Centre administratif et historique avec son architecture coloniale.",
        rating: 4.5,
        icon: "fas fa-building",
        features: ["Architecture coloniale", "Musées", "Restaurants"]
    },
    {
        id: 3,
        name: "Parc National du Banco",
        category: "nature",
        image: "images/banco.jpg",
        description: "Forêt tropicale préservée au cœur de la ville.",
        rating: 4.7,
        icon: "fas fa-tree",
        features: ["Randonnée", "Observation oiseaux", "Pique-nique"]
    },
    {
        id: 4,
        name: "Marché de Yamoussoukro",
        category: "shopping",
        image: "images/yams-market.jpg",
        description: "Marché traditionnel coloré pour l'artisanat local.",
        rating: 4.3,
        icon: "fas fa-shopping-bag",
        features: ["Artisanat", "Textiles", "Épices"]
    },
    {
        id: 5,
        name: "Lagune Ébrié",
        category: "nature",
        image: "images/lagune.jpg",
        description: "Croisière sur la magnifique lagune d'Abidjan.",
        rating: 4.6,
        icon: "fas fa-ship",
        features: ["Croisière", "Pêche", "Coucher de soleil"]
    },
    {
        id: 6,
        name: "Musée des Civilisations",
        category: "culture",
        image: "images/musee.jpg",
        description: "Découvrez l'histoire riche de la Côte d'Ivoire.",
        rating: 4.4,
        icon: "fas fa-landmark",
        features: ["Art africain", "Histoire", "Expositions"]
    },
    {
        id: 7,
        name: "Marché de Cocody",
        category: "gastronomie",
        image: "images/marche-cocody.jpg",
        description: "Dégustez les spécialités culinaires ivoiriennes.",
        rating: 4.2,
        icon: "fas fa-utensils",
        features: ["Street food", "Fruits tropicaux", "Plats locaux"]
    },
    {
        id: 8,
        name: "Jardin Botanique",
        category: "nature",
        image: "images/jardin.jpg",
        description: "Collection exceptionnelle de plantes tropicales.",
        rating: 4.5,
        icon: "fas fa-leaf",
        features: ["Plantes rares", "Jardins thématiques", "Visites"]
    }
];

// Générer la galerie des lieux
function generatePlacesGallery(filter = 'all') {
    const gallery = document.getElementById('places-gallery');
    if (!gallery) return;
    
    gallery.innerHTML = '';
    
    const filteredPlaces = filter === 'all' 
        ? touristPlaces 
        : touristPlaces.filter(place => place.category === filter);
    
    filteredPlaces.forEach(place => {
        const col = document.createElement('div');
        col.className = 'col-lg-3 col-md-6';
        
        col.innerHTML = `
            <div class="place-card" data-category="${place.category}">
                <div class="place-card-img">
                    <img src="${place.image}" alt="${place.name}"
                         onerror="this.src='https://via.placeholder.com/400x300/4a7c59/ffffff?text=${encodeURIComponent(place.name)}'">
                    <span class="place-category">
                        <i class="${place.icon} me-1"></i>
                        ${place.category.charAt(0).toUpperCase() + place.category.slice(1)}
                    </span>
                    <div class="place-rating">
                        <i class="fas fa-star text-warning"></i> ${place.rating}
                    </div>
                </div>
                <div class="card-body p-4">
                    <h5 class="card-title">${place.name}</h5>
                    <p class="card-text text-muted">${place.description}</p>
                    <div class="mt-3">
                        ${place.features.map(feature => 
                            `<span class="badge bg-light text-dark me-1 mb-1">${feature}</span>`
                        ).join('')}
                    </div>
                    <div class="mt-3 d-flex justify-content-between align-items-center">
                        <button class="btn btn-sm btn-outline-primary explore-btn" data-place="${place.id}">
                            <i class="fas fa-eye me-1"></i> Explorer
                        </button>
                        <button class="btn btn-sm btn-outline-success map-btn" data-place="${place.id}">
                            <i class="fas fa-map-marker-alt me-1"></i> Itinéraire
                        </button>
                    </div>
                </div>
            </div>
        `;
        
        gallery.appendChild(col);
    });
}

// Gestion des filtres
document.addEventListener('DOMContentLoaded', function() {
    // Générer la galerie initiale
    generatePlacesGallery();
    
    // Gestion des filtres
    const filterButtons = document.querySelectorAll('#category-filters button');
    filterButtons.forEach(button => {
        button.addEventListener('click', function() {
            // Retirer la classe active de tous les boutons
            filterButtons.forEach(btn => btn.classList.remove('active'));
            // Ajouter la classe active au bouton cliqué
            this.classList.add('active');
            // Appliquer le filtre
            const filter = this.getAttribute('data-filter');
            generatePlacesGallery(filter);
        });
    });
    
    // Points interactifs sur la carte
    const mapPoints = document.querySelectorAll('.map-point');
    mapPoints.forEach(point => {
        point.addEventListener('click', function() {
            const target = this.getAttribute('data-target');
            // Animation de clic
            this.style.transform = 'translate(-50%, -50%) scale(1.5)';
            setTimeout(() => {
                this.style.transform = 'translate(-50%, -50%) scale(1)';
            }, 300);
            
            // Filtrer la galerie selon le point cliqué
            let filter = 'all';
            switch(target) {
                case 'basilique': filter = 'culture'; break;
                case 'plateau': filter = 'culture'; break;
                case 'banco': filter = 'nature'; break;
                case 'yams': filter = 'shopping'; break;
            }
            
            // Mettre à jour les filtres et la galerie
            filterButtons.forEach(btn => {
                btn.classList.remove('active');
                if(btn.getAttribute('data-filter') === filter) {
                    btn.classList.add('active');
                }
            });
            generatePlacesGallery(filter);
            
            // Scroll vers la galerie
            document.getElementById('places-gallery').scrollIntoView({ 
                behavior: 'smooth',
                block: 'start'
            });
        });
    });
    
    // Gestion des boutons "Explorer"
    document.addEventListener('click', function(e) {
        if(e.target.closest('.explore-btn')) {
            const placeId = e.target.closest('.explore-btn').getAttribute('data-place');
            const place = touristPlaces.find(p => p.id == placeId);
            if(place) {
                // Afficher une modal avec les détails
                alert(`Exploration de : ${place.name}\n\n${place.description}\n\nCatégorie : ${place.category}\nNote : ${place.rating}/5`);
            }
        }
        
        if(e.target.closest('.map-btn')) {
            const placeId = e.target.closest('.map-btn').getAttribute('data-place');
            const place = touristPlaces.find(p => p.id == placeId);
            if(place) {
                // Ouvrir Google Maps (simulation)
                window.open(`https://www.google.com/maps/search/${encodeURIComponent(place.name)}+Abidjan`, '_blank');
            }
        }
    });
    
    // Animation au scroll
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };
    
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('animate-in');
            }
        });
    }, observerOptions);
    
    // Observer les cartes de lieux
    document.querySelectorAll('.place-card').forEach(card => {
        observer.observe(card);
    });
});




document.addEventListener('DOMContentLoaded', function() {
    // Animation au survol
    const placeItems = document.querySelectorAll('.place-item');
    
    placeItems.forEach(item => {
        const imgWrapper = item.querySelector('.place-img-wrapper');
        const img = item.querySelector('.place-img');
        
        // Effet zoom au survol
        item.addEventListener('mouseenter', function() {
            img.style.transform = 'scale(1.1)';
            imgWrapper.style.boxShadow = '0 15px 30px rgba(0,0,0,0.2)';
        });
        
        item.addEventListener('mouseleave', function() {
            img.style.transform = 'scale(1)';
            imgWrapper.style.boxShadow = '0 5px 15px rgba(0,0,0,0.1)';
        });
        
        // Effet clic
        item.addEventListener('mousedown', function() {
            this.style.transform = 'scale(0.98)';
        });
        
        item.addEventListener('mouseup', function() {
            this.style.transform = 'scale(1)';
        });
    });
    
    // Préchargement des modales
    const modalTriggers = document.querySelectorAll('[data-bs-toggle="modal"]');
    modalTriggers.forEach(trigger => {
        trigger.addEventListener('click', function() {
            const modalId = this.getAttribute('data-bs-target');
            console.log('Ouverture de :', modalId);
        });
    });
});

// Script simple pour les filtres (peut être amélioré)
    document.addEventListener('DOMContentLoaded', function() {
        const filterButtons = document.querySelectorAll('.btn-outline-primary, .btn-primary');
        
        filterButtons.forEach(button => {
            button.addEventListener('click', function() {
                // Retirer la classe active de tous les boutons
                filterButtons.forEach(btn => {
                    btn.classList.remove('active');
                    btn.classList.remove('btn-primary');
                    btn.classList.add('btn-outline-primary');
                });
                
                // Ajouter la classe active au bouton cliqué
                this.classList.remove('btn-outline-primary');
                this.classList.add('btn-primary', 'active');
                
                // Ici, vous pourriez ajouter la logique de filtrage
                // des actualités selon la catégorie sélectionnée
            });
        });
    });

    document.addEventListener('DOMContentLoaded', function() {
        // Animation des compteurs
        const counters = document.querySelectorAll('.counter');
        const speed = 200; // Plus bas = plus rapide
        
        const animateCounter = (counter) => {
            const target = +counter.getAttribute('data-target');
            const count = +counter.innerText;
            const increment = target / speed;
            
            if (count < target) {
                counter.innerText = Math.ceil(count + increment);
                setTimeout(() => animateCounter(counter), 10);
            } else {
                counter.innerText = target.toLocaleString();
            }
        };
        
        // Détecter quand les compteurs sont dans le viewport
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    animateCounter(entry.target);
                    observer.unobserve(entry.target);
                }
            });
        }, { threshold: 0.5 });
        
        counters.forEach(counter => {
            observer.observe(counter);
        });
        
        // Navigation par onglets
        const triggerTabList = document.querySelectorAll('#servicesTab button');
        triggerTabList.forEach(triggerEl => {
            const tabTrigger = new bootstrap.Tab(triggerEl);
            
            triggerEl.addEventListener('click', event => {
                event.preventDefault();
                tabTrigger.show();
            });
        });
        
        // Ajouter un effet au survol des cartes
        const serviceCards = document.querySelectorAll('.service-card, .urgent-service-card');
        serviceCards.forEach(card => {
            card.addEventListener('mouseenter', () => {
                card.style.transform = 'translateY(-10px) scale(1.02)';
            });
            
            card.addEventListener('mouseleave', () => {
                card.style.transform = 'translateY(-5px) scale(1)';
            });
        });
    });

    document.addEventListener('DOMContentLoaded', function() {
    // Ajouter des placeholders améliorés
    const inputs = document.querySelectorAll('.modern-form input, .modern-form textarea');
    
    inputs.forEach(input => {
        // Si le champ est vide, ajouter un effet
        if (!input.value) {
            input.style.borderColor = '#e0e6ed';
        }
        
        // Effet focus amélioré
        input.addEventListener('focus', function() {
            this.parentElement.style.transform = 'translateX(8px)';
            this.parentElement.style.boxShadow = '0 8px 20px rgba(0, 0, 0, 0.12)';
        });
        
        input.addEventListener('blur', function() {
            this.parentElement.style.transform = 'translateX(0)';
            this.parentElement.style.boxShadow = '0 4px 12px rgba(0, 0, 0, 0.05)';
        });
        
        // Validation en direct pour le téléphone
        if (input.type === 'tel') {
            input.addEventListener('input', function(e) {
                // Nettoyer le numéro
                this.value = this.value.replace(/[^\d+\-\s]/g, '');
                
                // Ajouter un style si le format semble bon
                if (this.value.length >= 10) {
                    this.style.borderColor = '#2ecc71';
                    this.style.background = 'linear-gradient(145deg, #f8fff9, #ffffff)';
                }
            });
        }
        
        // Validation pour l'email
        if (input.type === 'email') {
            input.addEventListener('blur', function() {
                const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
                if (this.value && !emailPattern.test(this.value)) {
                    this.style.borderColor = '#e74c3c';
                    this.style.animation = 'shake 0.5s ease';
                }
            });
        }
    });
    
    // Effet de soumission
    const form = document.querySelector('.modern-form');
    const submitBtn = document.querySelector('.submit-btn');
    
    if (form && submitBtn) {
        form.addEventListener('submit', function(e) {
            // Ajouter un effet de chargement
            submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin me-2"></i>Envoi en cours...';
            submitBtn.disabled = true;
            submitBtn.style.opacity = '0.8';
            
            // Valider tous les champs requis
            let valid = true;
            const requiredInputs = form.querySelectorAll('input[required], textarea[required]');
            
            requiredInputs.forEach(input => {
                if (!input.value.trim()) {
                    valid = false;
                    input.style.borderColor = '#e74c3c';
                    input.style.animation = 'shake 0.5s ease';
                    
                    // Réinitialiser l'animation après un délai
                    setTimeout(() => {
                        input.style.animation = '';
                    }, 500);
                }
            });
            
            if (!valid) {
                e.preventDefault();
                submitBtn.innerHTML = '<i class="fas fa-paper-plane me-2"></i>Envoyer le message';
                submitBtn.disabled = false;
                submitBtn.style.opacity = '1';
                
                // Afficher une alerte visuelle
                submitBtn.style.background = 'linear-gradient(135deg, #e74c3c, #c0392b)';
                setTimeout(() => {
                    submitBtn.style.background = 'linear-gradient(135deg, #3498db, #2980b9)';
                }, 1000);
            }
        });
    }
});

 // Gestion des demandes en ligne
    function envoyerDemandeNaissance() {
        const form = document.getElementById('formNaissance');
        const submitBtn = document.querySelector('#demandeNaissanceModal .btn-primary');
        
        if (form.checkValidity()) {
            // Simulation d'envoi
            const originalText = submitBtn.innerHTML;
            submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin me-2"></i>Envoi en cours...';
            submitBtn.disabled = true;
            
            setTimeout(() => {
                // Message de succès
                const successAlert = document.createElement('div');
                successAlert.className = 'alert alert-success alert-dismissible fade show';
                successAlert.innerHTML = `
                    <i class="fas fa-check-circle me-2"></i>
                    <strong>Demande envoyée !</strong> Votre demande d'acte de naissance a été enregistrée sous le numéro <strong>AN-${Date.now().toString().slice(-8)}</strong>. Vous recevrez un email de confirmation dans les 24h.
                    <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
                `;
                
                form.prepend(successAlert);
                
                // Réinitialiser après 3 secondes
                setTimeout(() => {
                    form.reset();
                    submitBtn.innerHTML = originalText;
                    submitBtn.disabled = false;
                    
                    // Fermer le modal après 2 secondes
                    setTimeout(() => {
                        const modal = bootstrap.Modal.getInstance(document.getElementById('demandeNaissanceModal'));
                        if (modal) modal.hide();
                        
                        // Afficher notification
                        showNotification('Votre demande a été envoyée avec succès !', 'success');
                    }, 2000);
                }, 3000);
            }, 1500);
        } else {
            form.reportValidity();
        }
    }
    
    // Fonction de notification
    function showNotification(message, type = 'success') {
        const notification = document.createElement('div');
        notification.className = `alert alert-${type} alert-dismissible fade show position-fixed`;
        notification.style.cssText = 'top: 20px; right: 20px; z-index: 9999; min-width: 300px;';
        notification.innerHTML = `
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        `;
        
        document.body.appendChild(notification);
        
        setTimeout(() => {
            notification.remove();
        }, 5000);
    }
    
    // Scroll vers sections
    document.addEventListener('DOMContentLoaded', function() {
        // Navigation rapide
        document.querySelectorAll('a[href^="#"]').forEach(anchor => {
            anchor.addEventListener('click', function(e) {
                const targetId = this.getAttribute('href');
                if (targetId !== '#') {
                    e.preventDefault();
                    const targetElement = document.querySelector(targetId);
                    if (targetElement) {
                        window.scrollTo({
                            top: targetElement.offsetTop - 100,
                            behavior: 'smooth'
                        });
                    }
                }
            });
        });
        
        // Animation des cartes au scroll
        const observerOptions = {
            threshold: 0.1,
            rootMargin: '0px 0px -50px 0px'
        };
        
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('animate__animated', 'animate__fadeInUp');
                }
            });
        }, observerOptions);
        
        // Observer les cartes de service
        document.querySelectorAll('.service-detail-card').forEach(card => {
            observer.observe(card);
        });
        
        // Validation des formulaires
        const forms = document.querySelectorAll('form');
        forms.forEach(form => {
            form.addEventListener('input', function(e) {
                if (e.target.checkValidity()) {
                    e.target.classList.remove('is-invalid');
                    e.target.classList.add('is-valid');
                } else {
                    e.target.classList.remove('is-valid');
                    e.target.classList.add('is-invalid');
                }
            });
        });
    });

    // Fonction pour animer un compteur
function animerCompteur(element, valeurFinale, duree = 2000) {
    let valeurActuelle = 0;
    const increment = valeurFinale / (duree / 30); // 16ms ≈ 60fps
    
    function miseAJour() {
        valeurActuelle += increment;
        
        if (valeurActuelle < valeurFinale) {
            element.textContent = Math.floor(valeurActuelle).toLocaleString();
            requestAnimationFrame(miseAJour);
        } else {
            element.textContent = valeurFinale.toLocaleString();
        }
    }
    
    requestAnimationFrame(miseAJour);
}

// Fonction pour démarrer l'animation
function demarrerCompteurs() {
    // Valeurs finales - MODIFIEZ CES CHIFFRES
    const valeurs = {
        habitants: 12500,
        quartiers: 8,
        villages: 12
    };
    
    // Récupérer les éléments
    const habitantsEl = document.getElementById('habitants');
    const quartiersEl = document.getElementById('quartiers');
    const villagesEl = document.getElementById('villages');
    
    // Vérifier que les éléments existent
    if (habitantsEl && quartiersEl && villagesEl) {
        // Démarrer les animations avec un léger délai pour chacune
        setTimeout(() => animerCompteur(habitantsEl, valeurs.habitants), 300);
        setTimeout(() => animerCompteur(quartiersEl, valeurs.quartiers), 600);
        setTimeout(() => animerCompteur(villagesEl, valeurs.villages), 900);
    }
}

// Démarrer quand la page est complètement chargée
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', demarrerCompteurs);
} else {
    demarrerCompteurs(); // DOM déjà chargé
}

document.addEventListener('DOMContentLoaded', function() {
    const filterButtons = document.querySelectorAll('.filters .btn');
    const articles = document.querySelectorAll('#articles-grid .col-lg-4');
    
    filterButtons.forEach(button => {
        button.addEventListener('click', function() {
            // Retirer la classe active de tous les boutons
            filterButtons.forEach(btn => btn.classList.remove('active'));
            // Ajouter la classe active au bouton cliqué
            this.classList.add('active');
            
            const filterValue = this.getAttribute('data-filter');
            
            // Filtrer les articles
            articles.forEach(article => {
                if (filterValue === 'all' || article.getAttribute('data-category') === filterValue) {
                    article.style.display = 'block';
                    setTimeout(() => {
                        article.style.opacity = '1';
                        article.style.transform = 'scale(1)';
                    }, 10);
                } else {
                    article.style.opacity = '0';
                    article.style.transform = 'scale(0.9)';
                    setTimeout(() => {
                        article.style.display = 'none';
                    }, 400);
                }
            });
        });
    });
});

