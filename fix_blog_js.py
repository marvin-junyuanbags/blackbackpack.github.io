#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Fix Blog JavaScript Issues
Removes duplicate variable declarations and fixes syntax errors
"""

import re

def fix_blog_javascript():
    """Fix JavaScript issues in blog.html"""
    
    with open('blog.html', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find the script section with allArticles
    script_pattern = r'<script>\s*const allArticles = \[.*?</script>'
    script_match = re.search(script_pattern, content, re.DOTALL)
    
    if script_match:
        # Remove the duplicate script section
        content = content.replace(script_match.group(0), '')
        
        # Add the corrected script at the end before closing body tag
        corrected_script = '''
    <script>
        // Blog pagination and filtering functionality
        const articlesPerPage = 12;
        let currentPage = 1;
        let allArticles = [];
        
        // Extract articles from the DOM
        function initializeArticles() {
            const articleElements = document.querySelectorAll('.article-card');
            allArticles = Array.from(articleElements).map(article => article.outerHTML);
        }
        
        const totalPages = Math.ceil(document.querySelectorAll('.article-card').length / articlesPerPage);
        
        function showPage(page) {
            const startIndex = (page - 1) * articlesPerPage;
            const endIndex = Math.min(startIndex + articlesPerPage, allArticles.length);
            
            const articlesGrid = document.getElementById('articles-grid');
            articlesGrid.innerHTML = '';
            
            for (let i = startIndex; i < endIndex; i++) {
                if (allArticles[i]) {
                    articlesGrid.innerHTML += allArticles[i];
                }
            }
            
            // Update pagination info
            document.getElementById('current-page').textContent = page;
            document.getElementById('total-pages').textContent = totalPages;
            document.getElementById('showing-start').textContent = startIndex + 1;
            document.getElementById('showing-end').textContent = Math.min(endIndex, allArticles.length);
            
            // Update pagination buttons
            const prevBtn = document.getElementById('prev-page');
            const nextBtn = document.getElementById('next-page');
            
            if (prevBtn) prevBtn.disabled = page === 1;
            if (nextBtn) nextBtn.disabled = page === totalPages;
            
            // Update active page number
            document.querySelectorAll('.pagination-number').forEach(btn => {
                btn.classList.remove('active');
                if (parseInt(btn.dataset.page) === page) {
                    btn.classList.add('active');
                }
            });
            
            currentPage = page;
            
            // Scroll to top of articles section
            const articlesSection = document.querySelector('.articles-section');
            if (articlesSection) {
                articlesSection.scrollIntoView({ behavior: 'smooth' });
            }
        }
        
        // Initialize when DOM is loaded
        document.addEventListener('DOMContentLoaded', function() {
            initializeArticles();
            
            // Event listeners for pagination
            const prevBtn = document.getElementById('prev-page');
            const nextBtn = document.getElementById('next-page');
            
            if (prevBtn) {
                prevBtn.addEventListener('click', () => {
                    if (currentPage > 1) showPage(currentPage - 1);
                });
            }
            
            if (nextBtn) {
                nextBtn.addEventListener('click', () => {
                    if (currentPage < totalPages) showPage(currentPage + 1);
                });
            }
            
            // Pagination number buttons
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
                    const articlesGrid = document.getElementById('articles-grid');
                    const paginationContainer = document.querySelector('.pagination-container');
                    
                    if (category === 'all') {
                        showPage(1);
                        if (paginationContainer) paginationContainer.style.display = 'block';
                    } else {
                        // Filter articles by category
                        const filteredArticles = allArticles.filter(article => {
                            const categoryMap = {
                                'manufacturing': ['Manufacturing'],
                                'design': ['Design & Innovation'],
                                'materials': ['Materials & Quality'],
                                'business': ['Business', 'Business Insights'],
                                'trends': ['Industry Trends'],
                                'sustainability': ['Sustainability'],
                                'technology': ['Technology'],
                                'guides': ['How-to Guides', 'Guides']
                            };
                            
                            const categoryNames = categoryMap[category] || [category];
                            return categoryNames.some(catName => 
                                article.includes(`<div class="article-category">${catName}</div>`)
                            );
                        });
                        
                        articlesGrid.innerHTML = '';
                        filteredArticles.forEach(article => {
                            articlesGrid.innerHTML += article;
                        });
                        
                        // Hide pagination for filtered results
                        if (paginationContainer) paginationContainer.style.display = 'none';
                    }
                });
            });
        });
    </script>'''
        
        # Insert the corrected script before closing body tag
        content = content.replace('</body>', corrected_script + '\n</body>')
    
    # Write the fixed content back
    with open('blog.html', 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("Fixed JavaScript issues in blog.html")

def main():
    """Main function"""
    print("Fixing blog.html JavaScript issues...")
    fix_blog_javascript()
    print("Blog JavaScript fixes completed!")

if __name__ == "__main__":
    main()