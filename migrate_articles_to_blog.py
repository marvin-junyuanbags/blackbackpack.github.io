#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Migrate Articles to Blog Script
Moves all articles from articles.html to blog.html with pagination support
"""

import re
import os
from datetime import datetime

def extract_articles_from_html(file_path):
    """Extract all article cards from articles.html"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find all article cards
    article_pattern = r'<article class="article-card"[^>]*>.*?</article>'
    articles = re.findall(article_pattern, content, re.DOTALL)
    
    return articles

def create_enhanced_blog_html(articles):
    """Create enhanced blog.html with all articles and pagination"""
    
    # Split articles into pages (12 articles per page)
    articles_per_page = 12
    total_pages = (len(articles) + articles_per_page - 1) // articles_per_page
    
    html_content = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Backpack Industry Blog | blackbackpack.co.uk - Expert Insights & Guides</title>
    <meta name="description" content="Explore our comprehensive blog covering backpack industry trends, manufacturing insights, design guides, and expert advice for businesses and professionals.">
    <meta name="keywords" content="backpack blog, industry insights, manufacturing guides, design trends, B2B backpack knowledge, custom backpack tips">
    <link rel="stylesheet" href="css/style.css">
    <link rel="canonical" href="https://blackbackpack.co.uk/blog.html">
</head>
<body>
    <!-- Header -->
    <header class="header">
        <nav class="navbar">
            <div class="nav-container">
                <div class="nav-logo">
                    <a href="index.html" class="logo-link">
                        <i class="fas fa-backpack"></i>
                        <span class="logo-text">BlackBackpack</span>
                    </a>
                </div>
                <ul class="nav-menu">
                    <li class="nav-item">
                        <a href="products.html" class="nav-link">Products</a>
                    </li>
                    <li class="nav-item">
                        <a href="services.html" class="nav-link">Services</a>
                    </li>
                    <li class="nav-item">
                        <a href="about.html" class="nav-link">About</a>
                    </li>
                    <li class="nav-item">
                        <a href="portfolio.html" class="nav-link">Portfolio</a>
                    </li>
                    <li class="nav-item">
                        <a href="blog.html" class="nav-link active">Blog</a>
                    </li>
                    <li class="nav-item">
                        <a href="contact.html" class="nav-link">Contact</a>
                    </li>
                </ul>
                <div class="nav-actions">
                    <a href="contact.html" class="btn btn-primary">Get Free Quote</a>
                    <div class="nav-toggle" id="mobile-menu">
                        <span class="bar"></span>
                        <span class="bar"></span>
                        <span class="bar"></span>
                    </div>
                </div>
            </div>
        </nav>
    </header>

    <!-- Page Header -->
    <section class="page-header">
        <div class="container">
            <h1>Industry Insights & Expert Guides</h1>
            <p>Stay informed with the latest trends, tips, and insights from the backpack manufacturing industry. Browse our complete collection of {total_articles} articles.</p>
        </div>
    </section>

    <!-- Blog Categories -->
    <section class="blog-categories">
        <div class="container">
            <div class="categories-filter">
                <button class="category-btn active" data-category="all">All Articles ({total_articles})</button>
                <button class="category-btn" data-category="manufacturing">Manufacturing</button>
                <button class="category-btn" data-category="design">Design & Innovation</button>
                <button class="category-btn" data-category="materials">Materials & Quality</button>
                <button class="category-btn" data-category="business">Business Insights</button>
                <button class="category-btn" data-category="trends">Industry Trends</button>
                <button class="category-btn" data-category="sustainability">Sustainability</button>
                <button class="category-btn" data-category="technology">Technology</button>
                <button class="category-btn" data-category="guides">How-to Guides</button>
            </div>
        </div>
    </section>

    <!-- Articles Grid -->
    <section class="articles-section">
        <div class="container">
            <div class="articles-header">
                <h2>All Articles</h2>
                <div class="articles-count">
                    <span>Showing <span id="showing-start">1</span>-<span id="showing-end">12</span> of {total_articles} articles</span>
                </div>
            </div>
            
            <div class="articles-grid" id="articles-grid">
'''.format(total_articles=len(articles))
    
    # Add first page of articles
    for i, article in enumerate(articles[:articles_per_page]):
        html_content += f"                {article}\n\n"
    
    html_content += '''            </div>

            <!-- Pagination -->
            <div class="pagination-container">
                <div class="pagination">
                    <button class="pagination-btn" id="prev-page" disabled>← Previous</button>
                    <div class="pagination-numbers" id="pagination-numbers">
'''
    
    # Add pagination numbers
    for page in range(1, min(6, total_pages + 1)):
        active_class = " active" if page == 1 else ""
        html_content += f'                        <button class="pagination-number{active_class}" data-page="{page}">{page}</button>\n'
    
    if total_pages > 5:
        html_content += '                        <span class="pagination-dots">...</span>\n'
        html_content += f'                        <button class="pagination-number" data-page="{total_pages}">{total_pages}</button>\n'
    
    html_content += '''                    </div>
                    <button class="pagination-btn" id="next-page">Next →</button>
                </div>
                <div class="pagination-info">
                    <span>Page <span id="current-page">1</span> of <span id="total-pages">{total_pages}</span></span>
                </div>
            </div>
        </div>
    </section>

    <!-- Newsletter Signup -->
    <section class="newsletter-signup">
        <div class="container">
            <div class="newsletter-content">
                <h2>Stay Updated</h2>
                <p>Subscribe to our newsletter for the latest industry insights, manufacturing tips, and product updates.</p>
                <form class="newsletter-form">
                    <input type="email" placeholder="Enter your email address" required>
                    <button type="submit" class="btn btn-primary">Subscribe</button>
                </form>
            </div>
        </div>
    </section>

    <!-- CTA Section -->
    <section class="cta">
        <div class="container">
            <h2>Ready to Start Your Custom Project?</h2>
            <p>Let our expertise guide your next backpack manufacturing project from concept to completion.</p>
            <div class="cta-buttons">
                <a href="contact.html" class="btn btn-primary">Get Started</a>
                <a href="services.html" class="btn btn-secondary">Our Services</a>
            </div>
        </div>
    </section>

    <!-- Footer -->
    <footer class="footer">
        <div class="container">
            <div class="footer-content">
                <div class="footer-section">
                    <h3>Black Backpack</h3>
                    <p>Leading custom backpack manufacturer specializing in B2B solutions worldwide.</p>
                    <div class="contact-info">
                        <p>Email: <a href="mailto:cco@junyuanbags.com">cco@junyuanbags.com</a></p>
                    </div>
                </div>
                <div class="footer-section">
                    <h4>Quick Links</h4>
                    <ul>
                        <li><a href="products.html">Products</a></li>
                        <li><a href="services.html">Services</a></li>
                        <li><a href="about.html">About Us</a></li>
                        <li><a href="contact.html">Contact</a></li>
                    </ul>
                </div>
                <div class="footer-section">
                    <h4>Resources</h4>
                    <ul>
                        <li><a href="blog.html">Blog</a></li>
                    </ul>
                </div>
            </div>
            <div class="footer-bottom">
                <p>&copy; 2024 Black Backpack. All rights reserved.</p>
            </div>
        </div>
    </footer>

    <!-- Hidden Articles Data for Pagination -->
    <script>
        const allArticles = ['''.format(total_pages=total_pages)
    
    # Add all articles as JavaScript data
    for i, article in enumerate(articles):
        # Escape quotes and newlines for JavaScript
        escaped_article = article.replace('\\', '\\\\').replace('"', '\\"').replace('\n', '\\n').replace('\r', '')
        html_content += f'            "{escaped_article}"'
        if i < len(articles) - 1:
            html_content += ',\n'
        else:
            html_content += '\n'
    
    html_content += '''        ];
        
        const articlesPerPage = 12;
        const totalPages = Math.ceil(allArticles.length / articlesPerPage);
        let currentPage = 1;
        
        function showPage(page) {
            const startIndex = (page - 1) * articlesPerPage;
            const endIndex = Math.min(startIndex + articlesPerPage, allArticles.length);
            
            const articlesGrid = document.getElementById('articles-grid');
            articlesGrid.innerHTML = '';
            
            for (let i = startIndex; i < endIndex; i++) {
                articlesGrid.innerHTML += allArticles[i];
            }
            
            // Update pagination
            document.getElementById('current-page').textContent = page;
            document.getElementById('total-pages').textContent = totalPages;
            document.getElementById('showing-start').textContent = startIndex + 1;
            document.getElementById('showing-end').textContent = endIndex;
            
            // Update pagination buttons
            document.getElementById('prev-page').disabled = page === 1;
            document.getElementById('next-page').disabled = page === totalPages;
            
            // Update active page number
            document.querySelectorAll('.pagination-number').forEach(btn => {
                btn.classList.remove('active');
                if (parseInt(btn.dataset.page) === page) {
                    btn.classList.add('active');
                }
            });
            
            currentPage = page;
            
            // Scroll to top of articles section
            document.querySelector('.articles-section').scrollIntoView({ behavior: 'smooth' });
        }
        
        // Event listeners
        document.getElementById('prev-page').addEventListener('click', () => {
            if (currentPage > 1) showPage(currentPage - 1);
        });
        
        document.getElementById('next-page').addEventListener('click', () => {
            if (currentPage < totalPages) showPage(currentPage + 1);
        });
        
        document.querySelectorAll('.pagination-number').forEach(btn => {
            btn.addEventListener('click', () => {
                const page = parseInt(btn.dataset.page);
                showPage(page);
            });
        });
        
        // Category filtering
        document.querySelectorAll('.category-btn').forEach(btn => {
            btn.addEventListener('click', () => {
                document.querySelectorAll('.category-btn').forEach(b => b.classList.remove('active'));
                btn.classList.add('active');
                
                const category = btn.dataset.category;
                if (category === 'all') {
                    showPage(1);
                } else {
                    // Filter articles by category
                    const filteredArticles = allArticles.filter(article => 
                        article.includes(`data-category="${category}"`) || 
                        article.includes(`<div class="article-category">${category.charAt(0).toUpperCase() + category.slice(1)}</div>`) ||
                        article.includes(`<div class="article-category">Manufacturing</div>`) && category === 'manufacturing' ||
                        article.includes(`<div class="article-category">Design & Innovation</div>`) && category === 'design' ||
                        article.includes(`<div class="article-category">Materials & Quality</div>`) && category === 'materials' ||
                        article.includes(`<div class="article-category">Business Insights</div>`) && category === 'business' ||
                        article.includes(`<div class="article-category">Industry Trends</div>`) && category === 'trends' ||
                        article.includes(`<div class="article-category">Sustainability</div>`) && category === 'sustainability' ||
                        article.includes(`<div class="article-category">Technology</div>`) && category === 'technology' ||
                        article.includes(`<div class="article-category">How-to Guides</div>`) && category === 'guides'
                    );
                    
                    const articlesGrid = document.getElementById('articles-grid');
                    articlesGrid.innerHTML = '';
                    filteredArticles.forEach(article => {
                        articlesGrid.innerHTML += article;
                    });
                    
                    // Hide pagination for filtered results
                    document.querySelector('.pagination-container').style.display = 'none';
                }
            });
        });
    </script>
    
    <script src="js/script.js"></script>
    <script src="js/navigation.js"></script>
</body>
</html>'''
    
    return html_content

def remove_articles_navigation():
    """Remove articles navigation from other pages"""
    files_to_update = [
        'index.html',
        'products.html', 
        'services.html',
        'about.html',
        'portfolio.html',
        'contact.html'
    ]
    
    for filename in files_to_update:
        file_path = filename
        if os.path.exists(file_path):
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Remove articles navigation link
            content = re.sub(r'<li class="nav-item">\s*<a href="articles\.html"[^>]*>.*?</a>\s*</li>', '', content, flags=re.DOTALL)
            
            # Remove articles quick links
            content = re.sub(r'<li><a href="articles\.html">.*?</a></li>', '', content)
            
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            print(f"Updated {filename} - removed articles navigation")

def main():
    """Main function to migrate articles to blog"""
    print("Starting articles migration to blog...")
    
    # Extract articles from articles.html
    articles = extract_articles_from_html('articles.html')
    print(f"Found {len(articles)} articles to migrate")
    
    # Create enhanced blog.html
    blog_content = create_enhanced_blog_html(articles)
    
    # Write new blog.html
    with open('blog.html', 'w', encoding='utf-8') as f:
        f.write(blog_content)
    
    print(f"Created enhanced blog.html with {len(articles)} articles and pagination")
    
    # Remove articles navigation from other pages
    remove_articles_navigation()
    
    print("Migration completed successfully!")
    print(f"- Blog now contains {len(articles)} articles")
    print("- Pagination implemented (12 articles per page)")
    print("- Category filtering available")
    print("- Articles navigation removed from other pages")

if __name__ == "__main__":
    main()