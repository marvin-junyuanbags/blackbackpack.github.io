// Dynamic Navigation Background Detection
class NavigationController {
    constructor() {
        this.header = document.querySelector('.header');
        this.init();
    }

    init() {
        // Check initial state
        this.updateNavigationStyle();
        
        // Listen for scroll events
        window.addEventListener('scroll', () => {
            this.updateNavigationStyle();
        });
        
        // Listen for page changes (if using SPA)
        window.addEventListener('popstate', () => {
            setTimeout(() => this.updateNavigationStyle(), 100);
        });
        
        // Check when page loads
        window.addEventListener('load', () => {
            this.updateNavigationStyle();
        });
    }

    updateNavigationStyle() {
        const scrollPosition = window.scrollY;
        const headerHeight = this.header.offsetHeight;
        
        // Get the element behind the header
        const elementBehindHeader = this.getElementBehindHeader(scrollPosition + headerHeight / 2);
        
        if (elementBehindHeader) {
            const bgColor = this.getBackgroundColor(elementBehindHeader);
            const isDark = this.isDarkBackground(bgColor, elementBehindHeader);
            
            if (isDark) {
                this.header.classList.add('dark-bg');
            } else {
                this.header.classList.remove('dark-bg');
            }
        }
    }

    getElementBehindHeader(yPosition) {
        // Temporarily hide header to get element behind it
        this.header.style.pointerEvents = 'none';
        const element = document.elementFromPoint(window.innerWidth / 2, yPosition - window.scrollY);
        this.header.style.pointerEvents = 'auto';
        
        return element;
    }

    getBackgroundColor(element) {
        let currentElement = element;
        
        while (currentElement && currentElement !== document.body) {
            const computedStyle = window.getComputedStyle(currentElement);
            const bgColor = computedStyle.backgroundColor;
            const bgImage = computedStyle.backgroundImage;
            
            // Check if element has a background color (not transparent)
            if (bgColor && bgColor !== 'rgba(0, 0, 0, 0)' && bgColor !== 'transparent') {
                return bgColor;
            }
            
            // Check if element has a background image
            if (bgImage && bgImage !== 'none') {
                // For background images, we'll assume they might be dark
                // You can enhance this by analyzing the actual image
                return this.analyzeBackgroundImage(currentElement, bgImage);
            }
            
            currentElement = currentElement.parentElement;
        }
        
        return 'rgb(255, 255, 255)'; // Default to white
    }

    analyzeBackgroundImage(element, bgImage) {
        // Check for common dark background patterns
        const darkPatterns = [
            'hero',
            'dark',
            'black',
            'night',
            'gradient'
        ];
        
        const elementClasses = element.className.toLowerCase();
        const elementId = element.id.toLowerCase();
        
        for (const pattern of darkPatterns) {
            if (elementClasses.includes(pattern) || elementId.includes(pattern)) {
                return 'rgb(0, 0, 0)'; // Assume dark
            }
        }
        
        // Check for gradient backgrounds that might be dark
        if (bgImage.includes('gradient')) {
            // Simple heuristic: if gradient contains dark colors
            if (bgImage.includes('rgba(0') || bgImage.includes('rgb(0') || 
                bgImage.includes('#000') || bgImage.includes('#111') || 
                bgImage.includes('#222') || bgImage.includes('#333')) {
                return 'rgb(0, 0, 0)';
            }
        }
        
        return 'rgb(255, 255, 255)'; // Default to light
    }

    isDarkBackground(bgColor, element) {
        // Parse RGB values
        const rgbMatch = bgColor.match(/rgb\((\d+),\s*(\d+),\s*(\d+)\)/);
        const rgbaMatch = bgColor.match(/rgba\((\d+),\s*(\d+),\s*(\d+),\s*([\d.]+)\)/);
        
        let r, g, b, a = 1;
        
        if (rgbaMatch) {
            [, r, g, b, a] = rgbaMatch.map(Number);
        } else if (rgbMatch) {
            [, r, g, b] = rgbMatch.map(Number);
        } else {
            // Handle hex colors
            const hex = bgColor.replace('#', '');
            if (hex.length === 6) {
                r = parseInt(hex.substr(0, 2), 16);
                g = parseInt(hex.substr(2, 2), 16);
                b = parseInt(hex.substr(4, 2), 16);
            } else {
                return false; // Can't determine, assume light
            }
        }
        
        // If alpha is very low, consider the background behind it
        if (a < 0.5) {
            return this.checkParentBackground(element);
        }
        
        // Calculate luminance
        const luminance = (0.299 * r + 0.587 * g + 0.114 * b) / 255;
        
        // Consider dark if luminance is below threshold
        return luminance < 0.5;
    }

    checkParentBackground(element) {
        // Check specific sections that are known to be dark
        const darkSections = ['hero', 'footer', 'dark-section', 'black-bg'];
        
        let currentElement = element;
        while (currentElement && currentElement !== document.body) {
            const classes = currentElement.className.toLowerCase();
            const id = currentElement.id.toLowerCase();
            
            for (const darkClass of darkSections) {
                if (classes.includes(darkClass) || id.includes(darkClass)) {
                    return true;
                }
            }
            
            currentElement = currentElement.parentElement;
        }
        
        return false;
    }
}

// Initialize when DOM is ready
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => {
        new NavigationController();
    });
} else {
    new NavigationController();
}

// Mobile menu toggle functionality
document.addEventListener('DOMContentLoaded', function() {
    const mobileMenuToggle = document.getElementById('mobile-menu');
    const navMenu = document.querySelector('.nav-menu');
    
    if (mobileMenuToggle && navMenu) {
        mobileMenuToggle.addEventListener('click', function() {
            this.classList.toggle('active');
            navMenu.classList.toggle('active');
        });
    }
});