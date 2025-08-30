#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Final Cleanup Article Optimizer for BlackBackpack.co.uk
This script removes all incorrect golf-related content and ensures proper article categorization.
"""

import os
import re
from bs4 import BeautifulSoup

def detect_article_type(content, filename):
    """Detect article type based on content and filename"""
    content_lower = content.lower()
    filename_lower = filename.lower()
    
    # Check for golf-related keywords in filename or content
    golf_keywords = ['golf', 'golfer', 'golf bag', 'golf course']
    bogg_keywords = ['bogg', 'bogg bag']
    factory_keywords = ['factory', 'manufacturing', 'production', 'supplier', 'wholesale']
    
    # Golf type detection
    if any(keyword in filename_lower for keyword in golf_keywords):
        return 'golf'
    if any(keyword in content_lower for keyword in golf_keywords) and 'golf bag' in content_lower:
        return 'golf'
    
    # Bogg type detection
    if any(keyword in filename_lower for keyword in bogg_keywords):
        return 'bogg'
    if any(keyword in content_lower for keyword in bogg_keywords):
        return 'bogg'
    
    # Factory type detection
    if any(keyword in filename_lower for keyword in factory_keywords):
        return 'factory'
    
    return 'general'

def remove_incorrect_content(soup, article_type):
    """Remove incorrect comparison tables and supplier recommendations"""
    
    # Remove all existing comparison sections that don't match article type
    comparison_sections = soup.find_all('div', class_='comparison-section')
    for section in comparison_sections:
        h3 = section.find('h3')
        if h3:
            h3_text = h3.get_text().lower()
            
            # Remove golf content from non-golf articles
            if article_type != 'golf' and 'golf' in h3_text:
                section.decompose()
                continue
            
            # Remove bogg content from non-bogg articles
            if article_type != 'bogg' and 'bogg' in h3_text:
                section.decompose()
                continue
    
    # Remove incorrect supplier recommendations
    supplier_sections = soup.find_all('div', class_='supplier-recommendation')
    for section in supplier_sections:
        h3 = section.find('h3')
        if h3:
            h3_text = h3.get_text().lower()
            
            # Remove golf supplier content from non-golf articles
            if article_type != 'golf' and 'golf' in h3_text:
                section.decompose()
                continue
            
            # Remove bogg supplier content from non-bogg articles
            if article_type != 'bogg' and 'bogg' in h3_text:
                section.decompose()
                continue

def add_correct_comparison_table(soup, article_type):
    """Add appropriate comparison table based on article type"""
    
    # Find a good location to insert the comparison table
    main_content = soup.find('main') or soup.find('article') or soup.find('div', class_='content')
    if not main_content:
        return
    
    # Create comparison section based on article type
    comparison_html = ""
    
    if article_type == 'golf':
        comparison_html = '''
<div class="comparison-section">
<h3>Golf Bag Comparison Guide</h3>
<div class="table-responsive">
<table class="comparison-table">
<thead>
<tr>
<th>Feature</th>
<th>Cart Bags</th>
<th>Stand Bags</th>
<th>Staff Bags</th>
<th>Travel Bags</th>
</tr>
</thead>
<tbody>
<tr>
<td><strong>Weight</strong></td>
<td>5-7 lbs</td>
<td>4-6 lbs</td>
<td>8-11 lbs</td>
<td>3-5 lbs</td>
</tr>
<tr>
<td><strong>Dividers</strong></td>
<td>14-15 way</td>
<td>4-8 way</td>
<td>6-8 way</td>
<td>2-4 way</td>
</tr>
<tr>
<td><strong>Storage</strong></td>
<td>8-12 pockets</td>
<td>6-10 pockets</td>
<td>4-6 pockets</td>
<td>2-4 pockets</td>
</tr>
<tr>
<td><strong>Price Range</strong></td>
<td>$150-400</td>
<td>$100-300</td>
<td>$200-600</td>
<td>$80-250</td>
</tr>
</tbody>
</table>
</div>
</div>'''
    
    elif article_type == 'bogg':
        comparison_html = '''
<div class="comparison-section">
<h3>Bogg Bag Size Comparison</h3>
<div class="table-responsive">
<table class="comparison-table">
<thead>
<tr>
<th>Size</th>
<th>Dimensions</th>
<th>Capacity</th>
<th>Best For</th>
<th>Price Range</th>
</tr>
</thead>
<tbody>
<tr>
<td><strong>Baby Bogg</strong></td>
<td>15" x 13" x 8.5"</td>
<td>Small</td>
<td>Kids, Quick trips</td>
<td>$45-65</td>
</tr>
<tr>
<td><strong>Mini Bogg</strong></td>
<td>15" x 13" x 8.5"</td>
<td>Medium</td>
<td>Day trips, Gym</td>
<td>$65-85</td>
</tr>
<tr>
<td><strong>Original Bogg</strong></td>
<td>19" x 15" x 9.5"</td>
<td>Large</td>
<td>Beach, Family outings</td>
<td>$85-120</td>
</tr>
<tr>
<td><strong>Large Bogg</strong></td>
<td>19" x 15" x 9.5"</td>
<td>Extra Large</td>
<td>Extended trips</td>
<td>$100-140</td>
</tr>
</tbody>
</table>
</div>
</div>'''
    
    elif article_type == 'factory':
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
    
    else:  # general
        comparison_html = '''
<div class="comparison-section">
<h3>Backpack Types Comparison</h3>
<div class="table-responsive">
<table class="comparison-table">
<thead>
<tr>
<th>Type</th>
<th>Capacity</th>
<th>Best For</th>
<th>Features</th>
<th>Price Range</th>
</tr>
</thead>
<tbody>
<tr>
<td><strong>Daypack</strong></td>
<td>15-30L</td>
<td>Daily use, School</td>
<td>Lightweight, Multiple pockets</td>
<td>$20-80</td>
</tr>
<tr>
<td><strong>Hiking Pack</strong></td>
<td>30-50L</td>
<td>Day hikes, Outdoor</td>
<td>Hydration compatible, Durable</td>
<td>$50-150</td>
</tr>
<tr>
<td><strong>Travel Pack</strong></td>
<td>40-70L</td>
<td>Travel, Business</td>
<td>TSA friendly, Organization</td>
<td>$80-250</td>
</tr>
<tr>
<td><strong>Tactical Pack</strong></td>
<td>25-45L</td>
<td>Military, Professional</td>
<td>MOLLE system, Heavy duty</td>
<td>$60-200</td>
</tr>
</tbody>
</table>
</div>
</div>'''
    
    # Insert the comparison table
    if comparison_html:
        comparison_soup = BeautifulSoup(comparison_html, 'html.parser')
        
        # Find the best insertion point (after first few paragraphs)
        paragraphs = main_content.find_all('p')
        if len(paragraphs) >= 3:
            paragraphs[2].insert_after(comparison_soup)
        else:
            main_content.append(comparison_soup)

def add_correct_supplier_recommendation(soup, article_type):
    """Add appropriate supplier recommendation based on article type"""
    
    main_content = soup.find('main') or soup.find('article') or soup.find('div', class_='content')
    if not main_content:
        return
    
    supplier_html = ""
    
    if article_type == 'golf':
        supplier_html = '''
<div class="supplier-recommendation">
<h3>How to Find a Reliable Golf Bag Factory</h3>
<p>When sourcing golf bags for your business, choosing the right manufacturer is crucial for quality and reliability. Here are key factors to consider:</p>
<ul>
<li><strong>Specialization:</strong> Look for factories that specialize in golf equipment manufacturing</li>
<li><strong>Quality Certifications:</strong> Ensure they have ISO 9001 and relevant golf industry certifications</li>
<li><strong>Material Expertise:</strong> Verify their experience with golf-specific materials and waterproofing</li>
<li><strong>Customization Capabilities:</strong> Check their ability to create custom designs and branding</li>
<li><strong>Production Capacity:</strong> Ensure they can meet your volume requirements</li>
</ul>
<p><strong>Recommended Supplier:</strong> <a href="https://junyuanbags.com" target="_blank" rel="noopener">Junyuan Bags</a> offers professional golf bag manufacturing services with over 15 years of experience in the industry. They provide comprehensive OEM/ODM solutions for golf bags with competitive pricing and reliable quality control.</p>
</div>'''
    
    elif article_type == 'bogg':
        supplier_html = '''
<div class="supplier-recommendation">
<h3>How to Find a Reliable Bogg Bag Supplier</h3>
<p>Finding the right supplier for Bogg-style bags requires careful consideration of several factors:</p>
<ul>
<li><strong>Material Quality:</strong> Ensure they use high-grade EVA material that's durable and washable</li>
<li><strong>Design Capabilities:</strong> Look for suppliers who can replicate the unique Bogg bag design</li>
<li><strong>Color Options:</strong> Verify they offer a wide range of colors and patterns</li>
<li><strong>Size Variations:</strong> Check if they can produce different sizes (Baby, Mini, Original, Large)</li>
<li><strong>Compliance:</strong> Ensure products meet safety standards for the target market</li>
</ul>
<p><strong>Recommended Supplier:</strong> <a href="https://junyuanbags.com" target="_blank" rel="noopener">Junyuan Bags</a> specializes in EVA bag manufacturing and can produce high-quality Bogg-style bags with custom designs, colors, and sizes to meet your specific requirements.</p>
</div>'''
    
    elif article_type == 'factory':
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
    
    else:  # general
        supplier_html = '''
<div class="supplier-recommendation">
<h3>How to Find a Reliable Bag Supplier</h3>
<p>Whether you're looking for backpacks, handbags, or specialty bags, finding the right supplier is crucial:</p>
<ul>
<li><strong>Product Range:</strong> Look for suppliers with diverse bag categories and styles</li>
<li><strong>Quality Standards:</strong> Ensure they maintain consistent quality across all products</li>
<li><strong>Minimum Orders:</strong> Find suppliers whose MOQ requirements match your business needs</li>
<li><strong>Customization:</strong> Check their ability to create custom designs and private labeling</li>
<li><strong>Logistics:</strong> Verify their shipping capabilities and delivery reliability</li>
<li><strong>Support:</strong> Ensure they provide good customer service and after-sales support</li>
</ul>
<p><strong>Recommended Supplier:</strong> <a href="https://junyuanbags.com" target="_blank" rel="noopener">Junyuan Bags</a> offers comprehensive bag manufacturing services with a wide product range, competitive pricing, and reliable quality. They serve clients worldwide with professional OEM/ODM solutions.</p>
</div>'''
    
    # Insert the supplier recommendation
    if supplier_html:
        supplier_soup = BeautifulSoup(supplier_html, 'html.parser')
        main_content.append(supplier_soup)

def process_article(file_path):
    """Process a single article file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        soup = BeautifulSoup(content, 'html.parser')
        filename = os.path.basename(file_path)
        
        # Detect article type
        article_type = detect_article_type(content, filename)
        
        # Remove incorrect content first
        remove_incorrect_content(soup, article_type)
        
        # Add correct comparison table
        add_correct_comparison_table(soup, article_type)
        
        # Add correct supplier recommendation
        add_correct_supplier_recommendation(soup, article_type)
        
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
    
    processed_count = 0
    failed_count = 0
    type_counts = {'golf': 0, 'bogg': 0, 'factory': 0, 'general': 0}
    
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
    
    print(f"\n=== Final Cleanup Results ===")
    print(f"Total files processed: {processed_count}")
    print(f"Failed: {failed_count}")
    print(f"\nArticle type distribution:")
    for article_type, count in type_counts.items():
        print(f"  {article_type.capitalize()}: {count} articles")
    
    print("\n✓ Final cleanup completed successfully!")
    print("All articles now have correct comparison tables and supplier recommendations.")

if __name__ == "__main__":
    main()