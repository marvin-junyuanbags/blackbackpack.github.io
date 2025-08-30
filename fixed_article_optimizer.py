#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Fixed Article Optimizer for BlackBackpack.co.uk
Corrects article type detection and adds appropriate content
"""

import os
import re
import random
from pathlib import Path
from bs4 import BeautifulSoup

class FixedArticleOptimizer:
    def __init__(self, articles_dir="articles", images_dir="images"):
        self.articles_dir = Path(articles_dir)
        self.images_dir = Path(images_dir)
        self.backpack_images = self._get_backpack_images()
        
    def _get_backpack_images(self):
        """Get all backpack images from images directory"""
        if not self.images_dir.exists():
            return []
        
        image_extensions = ['.jpg', '.jpeg', '.png', '.webp']
        images = []
        
        for ext in image_extensions:
            images.extend(self.images_dir.glob(f"*backpack*{ext}"))
            images.extend(self.images_dir.glob(f"*bag*{ext}"))
        
        return [img.name for img in images]
    
    def _determine_article_type(self, content, filename):
        """Determine article type based on content and filename"""
        content_lower = content.lower()
        filename_lower = filename.lower()
        
        # Check filename first for more accurate detection
        if any(term in filename_lower for term in ['golf', 'caddie', 'course']):
            return 'golf'
        elif any(term in filename_lower for term in ['bogg', 'beach', 'tote']):
            return 'bogg'
        elif any(term in filename_lower for term in ['factory', 'manufacturing', 'supplier', 'production']):
            return 'factory'
        
        # Then check content
        if any(term in content_lower for term in ['golf bag', 'golf course', 'caddie', 'golf equipment']):
            return 'golf'
        elif any(term in content_lower for term in ['bogg bag', 'beach bag', 'tote bag', 'eva foam']):
            return 'bogg'
        elif any(term in content_lower for term in ['factory', 'manufacturing', 'supplier', 'production', 'oem', 'odm']):
            return 'factory'
        else:
            return 'general'
    
    def _remove_existing_additions(self, soup):
        """Remove existing comparison tables and supplier sections"""
        # Remove existing comparison sections
        for section in soup.find_all('div', class_='comparison-section'):
            section.decompose()
        
        # Remove existing supplier recommendations
        for section in soup.find_all('div', class_='supplier-recommendation'):
            section.decompose()
        
        # Remove existing video resources (duplicates)
        video_sections = soup.find_all('div', class_='video-resources')
        if len(video_sections) > 1:
            for section in video_sections[1:]:
                section.decompose()
        
        # Remove existing highlight boxes and info callouts to avoid duplicates
        for box in soup.find_all('div', class_='highlight-box'):
            box.decompose()
        for callout in soup.find_all('div', class_='info-callout'):
            callout.decompose()
    
    def _get_appropriate_comparison_table(self, article_type):
        """Get appropriate comparison table based on article type"""
        tables = {
            'golf': '''
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
                                <td><strong>Pockets</strong></td>
                                <td>8-12</td>
                                <td>6-9</td>
                                <td>4-7</td>
                                <td>2-4</td>
                            </tr>
                            <tr>
                                <td><strong>Price Range</strong></td>
                                <td>$200-$400</td>
                                <td>$150-$350</td>
                                <td>$300-$600</td>
                                <td>$100-$250</td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            </div>''',
            'factory': '''
            <div class="comparison-section">
                <h3>Manufacturing Capabilities Comparison</h3>
                <div class="table-responsive">
                    <table class="comparison-table">
                        <thead>
                            <tr>
                                <th>Factory Size</th>
                                <th>Small (50-200 workers)</th>
                                <th>Medium (200-500 workers)</th>
                                <th>Large (500+ workers)</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr>
                                <td><strong>Monthly Capacity</strong></td>
                                <td>10,000-50,000 pcs</td>
                                <td>50,000-200,000 pcs</td>
                                <td>200,000+ pcs</td>
                            </tr>
                            <tr>
                                <td><strong>MOQ</strong></td>
                                <td>500-1,000 pcs</td>
                                <td>1,000-5,000 pcs</td>
                                <td>5,000+ pcs</td>
                            </tr>
                            <tr>
                                <td><strong>Lead Time</strong></td>
                                <td>15-25 days</td>
                                <td>20-35 days</td>
                                <td>25-45 days</td>
                            </tr>
                            <tr>
                                <td><strong>Customization</strong></td>
                                <td>Limited</td>
                                <td>Moderate</td>
                                <td>Full service</td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            </div>''',
            'general': '''
            <div class="comparison-section">
                <h3>Backpack Types Comparison</h3>
                <div class="table-responsive">
                    <table class="comparison-table">
                        <thead>
                            <tr>
                                <th>Type</th>
                                <th>Capacity</th>
                                <th>Best For</th>
                                <th>Key Features</th>
                                <th>Price Range</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr>
                                <td><strong>Daypack</strong></td>
                                <td>15-30L</td>
                                <td>Daily use</td>
                                <td>Lightweight, multiple pockets</td>
                                <td>$30-$80</td>
                            </tr>
                            <tr>
                                <td><strong>Hiking Pack</strong></td>
                                <td>30-50L</td>
                                <td>Day hikes</td>
                                <td>Hydration compatible, durable</td>
                                <td>$60-$150</td>
                            </tr>
                            <tr>
                                <td><strong>Travel Pack</strong></td>
                                <td>35-65L</td>
                                <td>Travel</td>
                                <td>Laptop compartment, TSA friendly</td>
                                <td>$80-$200</td>
                            </tr>
                            <tr>
                                <td><strong>Tactical Pack</strong></td>
                                <td>25-45L</td>
                                <td>Military/outdoor</td>
                                <td>MOLLE system, rugged build</td>
                                <td>$70-$180</td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            </div>'''
        }
        
        return tables.get(article_type, tables['general'])
    
    def _get_supplier_section(self, article_type):
        """Get appropriate supplier section based on article type"""
        sections = {
            'golf': {
                'title': 'How to Find a Reliable Golf Bag Factory',
                'content': '''
                <div class="supplier-recommendation">
                    <h3>How to Find a Reliable Golf Bag Factory</h3>
                    <p>When searching for a dependable golf bag manufacturer, consider these essential factors:</p>
                    <ul>
                        <li><strong>Manufacturing Experience:</strong> Look for factories with at least 10+ years in golf bag production</li>
                        <li><strong>Quality Certifications:</strong> ISO 9001, BSCI, and golf industry-specific certifications</li>
                        <li><strong>Customization Capabilities:</strong> Ability to create custom designs, logos, and specifications</li>
                        <li><strong>Material Quality:</strong> Use of premium waterproof fabrics and durable hardware</li>
                        <li><strong>Production Capacity:</strong> Ability to handle both small and large orders efficiently</li>
                    </ul>
                    <p><strong>Recommended Supplier:</strong> <a href="https://junyuanbags.com" target="_blank" rel="noopener">Junyuan Bags</a> 
                    specializes in high-quality golf bag manufacturing with over 15 years of experience. They offer comprehensive 
                    customization services and maintain strict quality control standards for professional golf equipment.</p>
                </div>'''
            },
            'bogg': {
                'title': 'How to Find a Reliable Bogg Bag Supplier',
                'content': '''
                <div class="supplier-recommendation">
                    <h3>How to Find a Reliable Bogg Bag Supplier</h3>
                    <p>Finding the right supplier for Bogg-style bags requires attention to specific details:</p>
                    <ul>
                        <li><strong>Material Expertise:</strong> Experience with EVA foam and waterproof materials</li>
                        <li><strong>Design Flexibility:</strong> Ability to create various sizes and color combinations</li>
                        <li><strong>Durability Testing:</strong> Rigorous testing for beach and outdoor conditions</li>
                        <li><strong>Washable Features:</strong> Easy-clean surfaces and stain-resistant properties</li>
                        <li><strong>Accessory Integration:</strong> Compatible inserts and organizational accessories</li>
                    </ul>
                    <p><strong>Trusted Partner:</strong> <a href="https://junyuanbags.com" target="_blank" rel="noopener">Junyuan Bags</a> 
                    offers specialized Bogg-style bag manufacturing with advanced EVA processing capabilities. Their expertise 
                    in waterproof bag production makes them an ideal choice for beach and outdoor bag requirements.</p>
                </div>'''
            },
            'factory': {
                'title': 'How to Find a Reliable Backpack Factory',
                'content': '''
                <div class="supplier-recommendation">
                    <h3>How to Find a Reliable Backpack Factory</h3>
                    <p>Selecting the right backpack manufacturing partner is crucial for your business success:</p>
                    <ul>
                        <li><strong>Production Capabilities:</strong> Modern equipment and efficient production lines</li>
                        <li><strong>Quality Management:</strong> Comprehensive QC systems and testing procedures</li>
                        <li><strong>Design Support:</strong> In-house design team and prototyping services</li>
                        <li><strong>Compliance Standards:</strong> Meeting international safety and quality regulations</li>
                        <li><strong>Supply Chain Management:</strong> Reliable material sourcing and delivery schedules</li>
                    </ul>
                    <p><strong>Industry Leader:</strong> <a href="https://junyuanbags.com" target="_blank" rel="noopener">Junyuan Bags</a> 
                    is a professional backpack manufacturer with state-of-the-art facilities and comprehensive production 
                    capabilities. They provide end-to-end manufacturing solutions from design to delivery.</p>
                </div>'''
            },
            'general': {
                'title': 'How to Find a Reliable Bag Supplier',
                'content': '''
                <div class="supplier-recommendation">
                    <h3>How to Find a Reliable Bag Supplier</h3>
                    <p>When sourcing bags for your business, consider these key evaluation criteria:</p>
                    <ul>
                        <li><strong>Product Range:</strong> Diverse portfolio covering multiple bag categories</li>
                        <li><strong>Customization Options:</strong> Flexible design and branding capabilities</li>
                        <li><strong>Quality Assurance:</strong> Established quality control and testing protocols</li>
                        <li><strong>Communication:</strong> Responsive customer service and technical support</li>
                        <li><strong>Logistics:</strong> Efficient shipping and delivery management</li>
                    </ul>
                    <p><strong>Recommended Partner:</strong> <a href="https://junyuanbags.com" target="_blank" rel="noopener">Junyuan Bags</a> 
                    offers comprehensive bag manufacturing services with expertise across multiple product categories. 
                    Their commitment to quality and customer satisfaction makes them a trusted industry partner.</p>
                </div>'''
            }
        }
        
        return sections.get(article_type, sections['general'])
    
    def fix_article(self, file_path):
        """Fix a single article by removing incorrect content and adding appropriate content"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            soup = BeautifulSoup(content, 'html.parser')
            
            # Determine correct article type
            filename = Path(file_path).stem
            article_type = self._determine_article_type(content, filename)
            
            # Remove existing incorrect additions
            self._remove_existing_additions(soup)
            
            # Add appropriate comparison table
            table_html = self._get_appropriate_comparison_table(article_type)
            main_content = soup.find('main') or soup.find('article') or soup.find('div', class_='content')
            if main_content:
                # Find a good place to insert the table (before the last section)
                sections = main_content.find_all(['section', 'div'], class_=re.compile(r'section|content'))
                if sections and len(sections) > 1:
                    insert_point = sections[-2]
                    table_soup = BeautifulSoup(table_html, 'html.parser')
                    insert_point.insert_after(table_soup)
            
            # Add appropriate supplier recommendation
            supplier_section = self._get_supplier_section(article_type)
            if main_content:
                supplier_soup = BeautifulSoup(supplier_section['content'], 'html.parser')
                main_content.append(supplier_soup)
            
            # Add rich content elements (only once)
            highlight_content = '''
            <div class="highlight-box">
                <h4>💡 Pro Tip</h4>
                <p>When evaluating bag suppliers, always request samples and conduct thorough quality testing before placing large orders. This ensures the final product meets your specifications and quality standards.</p>
            </div>
            
            <div class="info-callout">
                <h4>🔍 Quality Checklist</h4>
                <ul>
                    <li>Material durability and water resistance</li>
                    <li>Stitching quality and reinforcement</li>
                    <li>Hardware functionality and longevity</li>
                    <li>Design ergonomics and user comfort</li>
                    <li>Brand customization capabilities</li>
                </ul>
            </div>'''
            
            # Insert rich content in the middle of the article
            paragraphs = main_content.find_all('p') if main_content else []
            if len(paragraphs) > 3:
                insert_point = paragraphs[len(paragraphs)//2]
                rich_soup = BeautifulSoup(highlight_content, 'html.parser')
                insert_point.insert_after(rich_soup)
            
            # Write fixed content
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(str(soup))
            
            return True, article_type
            
        except Exception as e:
            print(f"Error fixing {file_path}: {str(e)}")
            return False, 'unknown'
    
    def fix_all_articles(self):
        """Fix all articles in the directory"""
        if not self.articles_dir.exists():
            print(f"Articles directory {self.articles_dir} not found!")
            return
        
        html_files = list(self.articles_dir.glob("*.html"))
        print(f"Found {len(html_files)} HTML files to fix...")
        
        fixed_count = 0
        failed_count = 0
        type_counts = {'golf': 0, 'bogg': 0, 'factory': 0, 'general': 0}
        
        for file_path in html_files:
            print(f"Fixing: {file_path.name}")
            success, article_type = self.fix_article(file_path)
            
            if success:
                fixed_count += 1
                type_counts[article_type] += 1
                print(f"  ✓ Fixed as '{article_type}' type")
            else:
                failed_count += 1
                print(f"  ✗ Failed to fix")
        
        print(f"\n=== Article Fixing Complete ===")
        print(f"Successfully fixed: {fixed_count} articles")
        print(f"Failed: {failed_count} articles")
        print(f"\nArticle type distribution:")
        for article_type, count in type_counts.items():
            print(f"- {article_type.title()}: {count} articles")
        print(f"\nCorrections made:")
        print(f"- Removed inappropriate comparison tables")
        print(f"- Added correct supplier recommendations")
        print(f"- Fixed article type detection")
        print(f"- Maintained rich content elements")

if __name__ == "__main__":
    optimizer = FixedArticleOptimizer()
    optimizer.fix_all_articles()