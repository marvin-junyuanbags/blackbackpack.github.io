#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Replace SVG images in articles.html with available backpack images
"""

import re
import os

def replace_svg_images():
    """Replace SVG images in articles.html with backpack images"""
    
    # Define SVG to backpack image mapping
    svg_replacements = {
        'sustainable-backpack-manufacturing.svg': 'blackbackpack (29).webp',
        'advanced-manufacturing-technology.svg': 'blackbackpack (30).webp',
        'quality-assurance.svg': 'blackbackpack (31).webp',
        'quality-control-backpack-production.svg': 'blackbackpack (32).webp',
        'automated-backpack-production.svg': 'blackbackpack (33).webp',
        'lean-manufacturing-backpacks.svg': 'blackbackpack (34).webp',
        'backpack-assembly-line-optimization.svg': 'blackbackpack (35).webp',
        'smart-backpack-technology.svg': 'blackbackpack (36).webp',
        'ergonomic-backpack-design.svg': 'blackbackpack (37).webp',
        'modular-backpack-design-concept.svg': 'blackbackpack (38).webp',
        'cost-optimization-manufacturing.svg': 'blackbackpack (39).webp',
        'digital-transformation-manufacturing.svg': 'blackbackpack (40).webp',
        'environmental-impact-manufacturing.svg': 'blackbackpack (41).webp',
        'quality-testing-standards.svg': 'blackbackpack (42).webp',
        'sustainable-manufacturing-practices.svg': 'blackbackpack (43).webp',
        'backpack-hardware-quality.svg': 'blackbackpack (44).webp',
        'b2b-market-trends.svg': 'blackbackpack (45).webp',
        'backpack-branding-strategies.svg': 'blackbackpack (46).webp',
        'pricing-strategies-manufacturing.svg': 'blackbackpack (47).webp',
        'global-supply-chain.svg': 'blackbackpack (48).webp',
        'import-export-regulations.svg': 'blackbackpack (49).webp',
        'color-trends-backpack-design.svg': 'blackbackpack (50).webp',
        'material-selection-guide.svg': 'blackbackpack (51).webp',
        'testing-procedures.svg': 'blackbackpack (52).webp',
        'size-optimization.svg': 'blackbackpack (53).webp',
        '3d-printing-backpack-prototyping.svg': 'blackbackpack (54).webp',
        'recycled-materials-backpack.svg': 'blackbackpack (55).webp',
        'international-trade-backpack.svg': 'blackbackpack (56).webp',
        'production-scaling-strategies.svg': 'blackbackpack (57).webp',
        'waterproof-backpack-design.svg': 'blackbackpack (1).webp',
        'customer-relationship-management.svg': 'blackbackpack (2).webp',
        'inventory-management-manufacturing.svg': 'blackbackpack (3).webp',
        'ai-manufacturing-optimization.svg': 'blackbackpack (4).webp',
        'anti-theft-backpack-features.svg': 'blackbackpack (9).webp',
        'carbon-footprint-manufacturing.svg': 'blackbackpack (13).webp',
        'market-research-backpack-industry.svg': 'blackbackpack (14).webp',
        'workforce-training-manufacturing.svg': 'blackbackpack (24).webp',
        'iot-smart-manufacturing.svg': 'blackbackpack (29).webp',
        'laptop-backpack-design.svg': 'blackbackpack (33).webp',
        'competitive-analysis-backpack.svg': 'blackbackpack (34).webp',
        'future-sustainable-manufacturing.svg': 'blackbackpack (39).webp'
    }
    
    # Read the articles.html file
    articles_file = 'articles.html'
    
    if not os.path.exists(articles_file):
        print(f"Error: {articles_file} not found")
        return
    
    with open(articles_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Track replacements
    replacements_made = 0
    
    # Replace each SVG image
    for svg_name, webp_name in svg_replacements.items():
        # Pattern to match the SVG image src
        pattern = f'src="images/{re.escape(svg_name)}"'
        replacement = f'src="images/{webp_name}"'
        
        # Count occurrences before replacement
        count_before = len(re.findall(pattern, content))
        
        if count_before > 0:
            content = re.sub(pattern, replacement, content)
            replacements_made += count_before
            print(f"Replaced {count_before} occurrence(s) of {svg_name} with {webp_name}")
    
    # Write the updated content back to the file
    with open(articles_file, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"\nTotal replacements made: {replacements_made}")
    print(f"Updated {articles_file} successfully!")

if __name__ == "__main__":
    replace_svg_images()