#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Precise Cleanup Article Optimizer for BlackBackpack.co.uk
This script removes ALL golf-related content from non-golf articles with precise detection.
"""

import os
import re
from bs4 import BeautifulSoup

def is_golf_article(content, filename):
    """Strictly determine if an article is actually about golf"""
    filename_lower = filename.lower()
    content_lower = content.lower()
    
    # Only consider it a golf article if:
    # 1. Filename explicitly contains 'golf'
    # 2. OR content has multiple golf-specific indicators
    
    if 'golf' in filename_lower:
        return True
    
    # Count golf-specific terms in content
    golf_terms = [
        'golf course', 'golf club', 'golf equipment', 'golfer', 'golf tournament',
        'golf swing', 'golf cart', 'tee time', 'fairway', 'green fee', 'caddie'
    ]
    
    golf_count = sum(1 for term in golf_terms if term in content_lower)
    
    # Only consider it golf if it has multiple golf-specific terms
    return golf_count >= 3

def is_bogg_article(content, filename):
    """Determine if an article is about Bogg bags"""
    filename_lower = filename.lower()
    content_lower = content.lower()
    
    return 'bogg' in filename_lower or 'bogg bag' in content_lower

def remove_all_golf_content(soup):
    """Remove ALL golf-related content from the article"""
    
    # Remove comparison sections with golf content
    sections_to_remove = []
    
    # Find all divs that might contain golf content
    all_divs = soup.find_all('div')
    for div in all_divs:
        div_text = div.get_text().lower()
        if 'golf' in div_text and ('comparison' in div_text or 'guide' in div_text):
            sections_to_remove.append(div)
    
    # Remove sections containing golf content
    for section in sections_to_remove:
        section.decompose()
    
    # Also remove any h3 tags with golf content and their following content
    h3_tags = soup.find_all('h3')
    for h3 in h3_tags:
        if h3 and 'golf' in h3.get_text().lower():
            # Remove the h3 and any following table or div
            current = h3
            while current:
                next_sibling = current.next_sibling
                if current.name in ['h3', 'div', 'table']:
                    current.decompose()
                    break
                elif current.name:
                    current.decompose()
                current = next_sibling

def add_factory_comparison_table(soup):
    """Add manufacturing capabilities comparison table"""
    
    main_content = soup.find('main') or soup.find('article') or soup.find('div', class_='content')
    if not main_content:
        return
    
    comparison_html = '''
<div class="comparison-section">
<h3>Manufacturing Capabilities Comparison</h3>
<div class="table-responsive">
<table class="comparison-table">
<thead>
<tr>
<th>Capability</th>
<th>Small Factory</th>
<th>Medium Factory</th>
<th>Large Factory</th>
<th>Premium Factory</th>
</tr>
</thead>
<tbody>
<tr>
<td><strong>MOQ</strong></td>
<td>100-500 pcs</td>
<td>500-2000 pcs</td>
<td>2000-10000 pcs</td>
<td>1000-5000 pcs</td>
</tr>
<tr>
<td><strong>Lead Time</strong></td>
<td>15-25 days</td>
<td>20-35 days</td>
<td>25-45 days</td>
<td>30-50 days</td>
</tr>
<tr>
<td><strong>Customization</strong></td>
<td>Basic</td>
<td>Moderate</td>
<td>Advanced</td>
<td>Full Custom</td>
</tr>
<tr>
<td><strong>Quality Control</strong></td>
<td>Standard</td>
<td>Enhanced</td>
<td>Comprehensive</td>
<td>Premium</td>
</tr>
</tbody>
</table>
</div>
</div>'''
    
    comparison_soup = BeautifulSoup(comparison_html, 'html.parser')
    
    # Find the best insertion point (after first few paragraphs)
    paragraphs = main_content.find_all('p')
    if len(paragraphs) >= 3:
        paragraphs[2].insert_after(comparison_soup)
    else:
        main_content.append(comparison_soup)

def add_factory_supplier_recommendation(soup):
    """Add backpack factory supplier recommendation"""
    
    main_content = soup.find('main') or soup.find('article') or soup.find('div', class_='content')
    if not main_content:
        return
    
    supplier_html = '''
<div class="supplier-recommendation">
<h3>How to Find a Reliable Backpack Factory</h3>
<p>Selecting the right backpack manufacturing partner is essential for your business success. Consider these important factors:</p>
<ul>
<li><strong>Production Capacity:</strong> Ensure the factory can handle your order volumes and delivery timelines</li>
<li><strong>Quality Management:</strong> Look for factories with robust QC systems and certifications</li>
<li><strong>Technical Capabilities:</strong> Verify their ability to work with various materials and construction methods</li>
<li><strong>Customization Services:</strong> Check their OEM/ODM capabilities for custom designs</li>
<li><strong>Communication:</strong> Ensure clear communication channels and English-speaking staff</li>
<li><strong>Compliance:</strong> Verify they meet international standards and ethical manufacturing practices</li>
</ul>
<p><strong>Recommended Factory:</strong> <a href="https://junyuanbags.com" target="_blank" rel="noopener">Junyuan Bags</a> is a professional backpack manufacturer with advanced production facilities, strict quality control, and extensive experience in custom bag manufacturing for global clients.</p>
</div>'''
    
    supplier_soup = BeautifulSoup(supplier_html, 'html.parser')
    main_content.append(supplier_soup)

def process_article(file_path):
    """Process a single article file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        soup = BeautifulSoup(content, 'html.parser')
        filename = os.path.basename(file_path)
        
        # Determine article type
        is_golf = is_golf_article(content, filename)
        is_bogg = is_bogg_article(content, filename)
        
        if is_golf:
            article_type = 'golf'
            # Keep golf content for actual golf articles
        elif is_bogg:
            article_type = 'bogg'
            # Remove golf content and add bogg content
            remove_all_golf_content(soup)
        else:
            # For all other articles, remove golf content and add factory content
            article_type = 'factory/general'
            remove_all_golf_content(soup)
            
            # Check if we need to add comparison table
            existing_comparison = soup.find('div', class_='comparison-section')
            if not existing_comparison:
                add_factory_comparison_table(soup)
            
            # Check if we need to add supplier recommendation
            existing_supplier = soup.find('div', class_='supplier-recommendation')
            if not existing_supplier:
                add_factory_supplier_recommendation(soup)
        
        # Write back to file
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(str(soup))
        
        return True, article_type
    
    except Exception as e:
        print(f"Error processing {file_path}: {str(e)}")
        return False, None

def main():
    """Main function to process all articles"""
    articles_dir = 'articles'
    
    if not os.path.exists(articles_dir):
        print(f"Articles directory '{articles_dir}' not found!")
        return
    
    html_files = [f for f in os.listdir(articles_dir) if f.endswith('.html')]
    
    print(f"Found {len(html_files)} HTML files to process...")
    print("Removing ALL golf content from non-golf articles...")
    
    processed_count = 0
    failed_count = 0
    type_counts = {'golf': 0, 'bogg': 0, 'factory/general': 0}
    
    for filename in html_files:
        file_path = os.path.join(articles_dir, filename)
        print(f"Processing: {filename}")
        
        success, article_type = process_article(file_path)
        
        if success:
            processed_count += 1
            if article_type:
                type_counts[article_type] += 1
            print(f"  ✓ Successfully processed as '{article_type}' type")
        else:
            failed_count += 1
            print(f"  ✗ Failed to process")
    
    print(f"\n=== Precise Cleanup Results ===")
    print(f"Total files processed: {processed_count}")
    print(f"Failed: {failed_count}")
    print(f"\nArticle type distribution:")
    for article_type, count in type_counts.items():
        print(f"  {article_type}: {count} articles")
    
    print("\n✓ Precise cleanup completed successfully!")
    print("All golf content removed from non-golf articles.")

if __name__ == "__main__":
    main()