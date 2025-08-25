// Mobile Navigation Toggle
const navToggle = document.querySelector('.nav-toggle');
const navMenu = document.querySelector('.nav-menu');

if (navToggle && navMenu) {
    navToggle.addEventListener('click', () => {
        navMenu.classList.toggle('active');
        navToggle.classList.toggle('active');
    });

    // Close menu when clicking on a link
    document.querySelectorAll('.nav-menu a').forEach(link => {
        link.addEventListener('click', () => {
            navMenu.classList.remove('active');
            navToggle.classList.remove('active');
        });
    });
}

// Smooth Scrolling for Anchor Links
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

// Header Scroll Effect
window.addEventListener('scroll', () => {
    const header = document.querySelector('.header');
    if (window.scrollY > 100) {
        header.style.background = 'rgba(26, 26, 26, 0.95)';
        header.style.backdropFilter = 'blur(10px)';
    } else {
        header.style.background = 'linear-gradient(135deg, #1a1a1a 0%, #2d2d2d 100%)';
        header.style.backdropFilter = 'none';
    }
});

// Intersection Observer for Animations
const observerOptions = {
    threshold: 0.1,
    rootMargin: '0px 0px -50px 0px'
};

const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.style.opacity = '1';
            entry.target.style.transform = 'translateY(0)';
        }
    });
}, observerOptions);

// Observe elements for animation
document.querySelectorAll('.feature-card, .product-card').forEach(el => {
    el.style.opacity = '0';
    el.style.transform = 'translateY(30px)';
    el.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
    observer.observe(el);
});

// Form Validation (for contact forms)
function validateForm(form) {
    const inputs = form.querySelectorAll('input[required], textarea[required]');
    let isValid = true;

    inputs.forEach(input => {
        const errorElement = input.parentNode.querySelector('.error-message');
        
        if (!input.value.trim()) {
            isValid = false;
            input.classList.add('error');
            if (errorElement) {
                errorElement.textContent = 'This field is required';
            }
        } else {
            input.classList.remove('error');
            if (errorElement) {
                errorElement.textContent = '';
            }
        }

        // Email validation
        if (input.type === 'email' && input.value.trim()) {
            const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
            if (!emailRegex.test(input.value)) {
                isValid = false;
                input.classList.add('error');
                if (errorElement) {
                    errorElement.textContent = 'Please enter a valid email address';
                }
            }
        }
    });

    return isValid;
}

// Handle form submissions
document.querySelectorAll('form').forEach(form => {
    form.addEventListener('submit', function(e) {
        e.preventDefault();
        
        if (validateForm(this)) {
            // Show success message
            const successMessage = document.createElement('div');
            successMessage.className = 'success-message';
            successMessage.textContent = 'Thank you for your message. We will get back to you soon!';
            successMessage.style.cssText = `
                background: #4CAF50;
                color: white;
                padding: 15px;
                border-radius: 5px;
                margin: 20px 0;
                text-align: center;
            `;
            
            this.insertBefore(successMessage, this.firstChild);
            this.reset();
            
            // Remove success message after 5 seconds
            setTimeout(() => {
                successMessage.remove();
            }, 5000);
        }
    });
});

// Loading Animation
window.addEventListener('load', () => {
    const loader = document.querySelector('.loader');
    if (loader) {
        loader.style.opacity = '0';
        setTimeout(() => {
            loader.style.display = 'none';
        }, 300);
    }
});

// Back to Top Button
const backToTopButton = document.createElement('button');
backToTopButton.innerHTML = '↑';
backToTopButton.className = 'back-to-top';
backToTopButton.style.cssText = `
    position: fixed;
    bottom: 30px;
    right: 30px;
    width: 50px;
    height: 50px;
    border: none;
    border-radius: 50%;
    background: #ff6b35;
    color: white;
    font-size: 20px;
    cursor: pointer;
    opacity: 0;
    visibility: hidden;
    transition: all 0.3s ease;
    z-index: 1000;
`;

document.body.appendChild(backToTopButton);

window.addEventListener('scroll', () => {
    if (window.scrollY > 300) {
        backToTopButton.style.opacity = '1';
        backToTopButton.style.visibility = 'visible';
    } else {
        backToTopButton.style.opacity = '0';
        backToTopButton.style.visibility = 'hidden';
    }
});

backToTopButton.addEventListener('click', () => {
    window.scrollTo({
        top: 0,
        behavior: 'smooth'
    });
});

// Lazy Loading for Images
if ('IntersectionObserver' in window) {
    const imageObserver = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const img = entry.target;
                img.src = img.dataset.src;
                img.classList.remove('lazy');
                imageObserver.unobserve(img);
            }
        });
    });

    document.querySelectorAll('img[data-src]').forEach(img => {
        imageObserver.observe(img);
    });
}

// Blog Category Filter
const categoryButtons = document.querySelectorAll('.category-btn');
const articleCards = document.querySelectorAll('.article-card');

if (categoryButtons.length > 0) {
    categoryButtons.forEach(button => {
        button.addEventListener('click', () => {
            // Remove active class from all buttons
            categoryButtons.forEach(btn => btn.classList.remove('active'));
            // Add active class to clicked button
            button.classList.add('active');
            
            const category = button.getAttribute('data-category');
            
            articleCards.forEach(card => {
                if (category === 'all' || card.getAttribute('data-category') === category) {
                    card.style.display = 'block';
                    card.style.animation = 'fadeIn 0.5s ease';
                } else {
                    card.style.display = 'none';
                }
            });
        });
    });
}

// Load More Articles Functionality
let articlesVisible = 6; // Initially show 6 articles
const loadMoreBtn = document.querySelector('.load-more-btn');
const allArticles = document.querySelectorAll('.article-card');

if (loadMoreBtn && allArticles.length > 0) {
    // Initially hide articles beyond the first 6
    allArticles.forEach((article, index) => {
        if (index >= articlesVisible) {
            article.style.display = 'none';
        }
    });
    
    // Hide load more button if there are 6 or fewer articles
    if (allArticles.length <= articlesVisible) {
        loadMoreBtn.style.display = 'none';
    }
    
    loadMoreBtn.addEventListener('click', () => {
        // Add loading state
        const originalText = loadMoreBtn.textContent;
        loadMoreBtn.textContent = 'Loading...';
        loadMoreBtn.disabled = true;
        loadMoreBtn.style.opacity = '0.7';
        
        setTimeout(() => {
            const hiddenArticles = Array.from(allArticles).filter(article => 
                article.style.display === 'none' || 
                getComputedStyle(article).display === 'none'
            );
            
            // Show next 3 articles
            const articlesToShow = hiddenArticles.slice(0, 3);
            
            articlesToShow.forEach((article, index) => {
                setTimeout(() => {
                    article.style.display = 'block';
                    article.style.animation = 'fadeInUp 0.6s ease';
                }, index * 150); // Stagger the animation
            });
            
            articlesVisible += 3;
            
            // Reset button state
            loadMoreBtn.textContent = originalText;
            loadMoreBtn.disabled = false;
            loadMoreBtn.style.opacity = '1';
            
            // Hide load more button if no more articles to show
            if (hiddenArticles.length <= 3) {
                setTimeout(() => {
                    loadMoreBtn.style.animation = 'fadeOut 0.5s ease';
                    setTimeout(() => {
                        loadMoreBtn.style.display = 'none';
                    }, 500);
                }, 600);
            }
            
            // Smooth scroll to show new articles
            if (articlesToShow.length > 0) {
                setTimeout(() => {
                    articlesToShow[0].scrollIntoView({
                        behavior: 'smooth',
                        block: 'center'
                    });
                }, 600);
            }
        }, 800); // Simulate loading time
    });
}

// Add CSS animations for article loading
const style = document.createElement('style');
style.textContent = `
    @keyframes fadeIn {
        from { opacity: 0; }
        to { opacity: 1; }
    }
    
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(30px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    @keyframes fadeOut {
        from {
            opacity: 1;
            transform: scale(1);
        }
        to {
            opacity: 0;
            transform: scale(0.9);
        }
    }
    
    .load-more-btn:disabled {
        cursor: not-allowed;
        transform: none !important;
    }
`;
document.head.appendChild(style);