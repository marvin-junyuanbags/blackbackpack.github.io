#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Image Reference Fixer for BlackBackpack.co.uk
Replaces missing .jpg image references with existing .svg or .webp files
"""

import os
import re
import glob
from pathlib import Path

# Define the website root directory
WEBSITE_ROOT = Path(r"C:\Users\A1775\blackbackpack.co.uk")
IMAGES_DIR = WEBSITE_ROOT / "images"

# Create mapping from missing .jpg files to existing alternatives
IMAGE_MAPPINGS = {
    # Hero images
    "sports-backpack-hero.jpg": "sports-backpack.svg",
    "outdoor-backpack-hero.jpg": "outdoor-backpack.svg", 
    "school-backpack-hero.jpg": "school-backpack.svg",
    "laptop-backpack-hero.jpg": "laptop-backpack.svg",
    "tactical-backpack-hero.jpg": "tactical-backpacks-category.svg",
    "travel-backpack-hero.jpg": "travel-backpack.svg",
    
    # Case study images (keep existing .jpg files)
    "case-study-tech-company.jpg": "case-study-tech-company.jpg",
    "case-study-university.jpg": "case-study-university.jpg", 
    "case-study-retail.jpg": "case-study-retail.jpg",
    
    # Business category images
    "corporate-executive.jpg": "blackbackpack (1).webp",
    "business-traveler.jpg": "blackbackpack (2).webp",
    "tech-professional.jpg": "blackbackpack (3).webp",
    "sales-professional.jpg": "blackbackpack (4).webp",
    
    # Sports category images
    "gym-fitness-case.jpg": "blackbackpack (5).webp",
    "team-sports-case.jpg": "blackbackpack (6).webp",
    "endurance-sports-case.jpg": "blackbackpack (7).webp",
    "adventure-sports-case.jpg": "blackbackpack (8).webp",
    
    # Outdoor category images
    "hiking-adventure.jpg": "blackbackpack (9).webp",
    "camping-expedition.jpg": "blackbackpack (10).webp",
    "climbing-adventure.jpg": "blackbackpack (11).webp",
    "adventure-travel.jpg": "blackbackpack (12).webp",
    
    # School category images
    "elementary-students.jpg": "blackbackpack (13).webp",
    "middle-school-students.jpg": "blackbackpack (14).webp",
    "high-school-students.jpg": "blackbackpack (15).webp",
    "university-students.jpg": "blackbackpack (16).webp",
    
    # Laptop category images
    "business-professionals.jpg": "blackbackpack (17).webp",
    "students-academics.jpg": "blackbackpack (18).webp",
    "tech-professionals.jpg": "blackbackpack (19).webp",
    "creative-professionals.jpg": "blackbackpack (20).webp",
    
    # Tactical category images
    "military-operations.jpg": "blackbackpack (21).webp",
    "law-enforcement.jpg": "blackbackpack (22).webp",
    "security-professionals.jpg": "blackbackpack (23).webp",
    "emergency-response.jpg": "blackbackpack (24).webp",
    
    # Travel category images
    "business-travel-case.jpg": "blackbackpack (25).webp",
    "digital-nomad-case.jpg": "blackbackpack (26).webp",
    "adventure-travel-case.jpg": "blackbackpack (27).webp",
    "weekend-getaway-case.jpg": "blackbackpack (28).webp",
    
    # OG and Twitter images
    "og-image.jpg": "hero-backpack.svg",
    "twitter-image.jpg": "hero-backpack.svg",
}

# Additional mappings for article images
ARTICLE_IMAGE_MAPPINGS = {
    # Use existing SVG files for article images
    "human-resources-management.jpg": "supply-chain-management.svg",
    "supply-chain.jpg": "supply-chain-management.svg",
    "customer-experience.jpg": "customer-relationship-management.svg",
    "data-analytics-backpack-manufacturing.jpg": "market-research-backpack-industry.svg",
    "market-research.jpg": "market-research-backpack-industry.svg",
    "technology-innovation.jpg": "innovation-technology.svg",
    "financial-management.jpg": "supply-chain-management.svg",
    "innovation-technology.jpg": "innovation-technology.svg",
    "investment-analysis.jpg": "market-research-backpack-industry.svg",
    "quality-control-testing.jpg": "quality-assurance.svg",
    "sustainability-practices.jpg": "sustainable-manufacturing.svg",
    "product-development-design.jpg": "custom-backpack-design-process.svg",
    "digital-transformation.jpg": "digital-transformation.svg",
    "risk-management.jpg": "supply-chain-management.svg",
    "regulatory-compliance.jpg": "quality-assurance.svg",
    "globalization-strategies.jpg": "global-supply-chain.svg",
    "customer-service-excellence.jpg": "customer-relationship-management.svg",
    "ecommerce-strategies.jpg": "digital-transformation.svg",
}

# Combine all mappings
ALL_MAPPINGS = {**IMAGE_MAPPINGS, **ARTICLE_IMAGE_MAPPINGS}

def fix_html_file(file_path):
    """Fix image references in a single HTML file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        changes_made = 0
        
        # Replace image references
        for old_image, new_image in ALL_MAPPINGS.items():
            # Pattern to match both relative and absolute image paths
            patterns = [
                f'src="images/{old_image}"',
                f'src="../images/{old_image}"',
                f'content="https://blackbackpack.co.uk/images/{old_image}"',
                f'content="https://www.blackbackpack.co.uk/images/{old_image}"',
            ]
            
            replacements = [
                f'src="images/{new_image}"',
                f'src="../images/{new_image}"', 
                f'content="https://blackbackpack.co.uk/images/{new_image}"',
                f'content="https://www.blackbackpack.co.uk/images/{new_image}"',
            ]
            
            for pattern, replacement in zip(patterns, replacements):
                if pattern in content:
                    content = content.replace(pattern, replacement)
                    changes_made += 1
        
        # Write back if changes were made
        if content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"✓ Fixed {changes_made} image references in {file_path.name}")
            return changes_made
        else:
            print(f"- No changes needed in {file_path.name}")
            return 0
            
    except Exception as e:
        print(f"✗ Error processing {file_path}: {e}")
        return 0

def main():
    """Main function to fix all HTML files"""
    print("BlackBackpack.co.uk Image Reference Fixer")
    print("=" * 50)
    
    # Find all HTML files
    html_files = list(WEBSITE_ROOT.glob("*.html"))
    html_files.extend(WEBSITE_ROOT.glob("articles/*.html"))
    
    total_changes = 0
    files_processed = 0
    
    for html_file in html_files:
        changes = fix_html_file(html_file)
        total_changes += changes
        files_processed += 1
    
    print("\n" + "=" * 50)
    print(f"Processing complete!")
    print(f"Files processed: {files_processed}")
    print(f"Total image references fixed: {total_changes}")
    
    # Verify that mapped images exist
    print("\nVerifying mapped images exist:")
    missing_images = []
    for new_image in set(ALL_MAPPINGS.values()):
        image_path = IMAGES_DIR / new_image
        if not image_path.exists():
            missing_images.append(new_image)
            print(f"⚠ Warning: {new_image} does not exist")
        else:
            print(f"✓ {new_image} exists")
    
    if missing_images:
        print(f"\n⚠ {len(missing_images)} mapped images are missing!")
    else:
        print("\n✓ All mapped images exist!")

if __name__ == "__main__":
    main()