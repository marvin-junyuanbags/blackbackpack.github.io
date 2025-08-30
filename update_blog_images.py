#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Blog Images Update Script for BlackBackpack.co.uk

This script updates all blog article images to use local images from the images folder.
If local images don't exist, it generates appropriate SVG icons.
"""

import os
import re
import glob
from pathlib import Path

def check_image_exists(image_path, base_dir):
    """Check if an image file exists in the images directory"""
    full_path = os.path.join(base_dir, image_path)
    return os.path.exists(full_path)

def generate_svg_icon(alt_text, category="general"):
    """Generate an appropriate SVG icon based on alt text and category"""
    
    # Define category-based colors and icons
    category_config = {
        "manufacturing": {"color": "#2563eb", "icon": "⚙️"},
        "technology": {"color": "#7c3aed", "icon": "💻"},
        "design": {"color": "#dc2626", "icon": "🎨"},
        "materials": {"color": "#059669", "icon": "🧵"},
        "business": {"color": "#ea580c", "icon": "📊"},
        "sustainability": {"color": "#16a34a", "icon": "🌱"},
        "guides": {"color": "#0891b2", "icon": "📖"},
        "general": {"color": "#6b7280", "icon": "🎒"}
    }
    
    config = category_config.get(category.lower(), category_config["general"])
    
    # Create a simple SVG with category-appropriate styling
    svg_content = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 300" width="400" height="300">
  <defs>
    <linearGradient id="bg-gradient" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:{config['color']};stop-opacity:0.1" />
      <stop offset="100%" style="stop-color:{config['color']};stop-opacity:0.3" />
    </linearGradient>
  </defs>
  
  <!-- Background -->
  <rect width="400" height="300" fill="url(#bg-gradient)" stroke="{config['color']}" stroke-width="2" rx="8"/>
  
  <!-- Icon Circle -->
  <circle cx="200" cy="120" r="40" fill="{config['color']}" opacity="0.2"/>
  
  <!-- Category Icon -->
  <text x="200" y="135" text-anchor="middle" font-size="32" fill="{config['color']}">{config['icon']}</text>
  
  <!-- Title Text -->
  <text x="200" y="180" text-anchor="middle" font-family="Arial, sans-serif" font-size="14" font-weight="bold" fill="{config['color']}">{category.title()}</text>
  
  <!-- Subtitle -->
  <text x="200" y="200" text-anchor="middle" font-family="Arial, sans-serif" font-size="12" fill="#6b7280">Black Backpack</text>
  
  <!-- Bottom decoration -->
  <rect x="150" y="220" width="100" height="2" fill="{config['color']}" opacity="0.5" rx="1"/>
</svg>'''
    
    return svg_content

def get_category_from_article_class(article_html):
    """Extract category from article class or content"""
    # Look for category in the article-category div
    category_match = re.search(r'<div class="article-category">([^<]+)</div>', article_html)
    if category_match:
        category = category_match.group(1).lower()
        # Map display categories to our internal categories
        category_mapping = {
            "design & innovation": "design",
            "materials & quality": "materials",
            "how-to guides": "guides"
        }
        return category_mapping.get(category, category.split()[0])
    return "general"

def update_blog_images():
    """Update all blog images to use local images or generate SVG icons"""
    
    base_dir = os.path.dirname(os.path.abspath(__file__))
    images_dir = os.path.join(base_dir, "images")
    
    print(f"Working directory: {base_dir}")
    print(f"Images directory: {images_dir}")
    
    # Get list of available images
    available_images = []
    if os.path.exists(images_dir):
        for ext in ['*.webp', '*.svg', '*.jpg', '*.jpeg', '*.png']:
            available_images.extend(glob.glob(os.path.join(images_dir, ext)))
        available_images = [os.path.basename(img) for img in available_images]
        print(f"Found {len(available_images)} images in images directory")
    
    # Update blog.html
    blog_file = os.path.join(base_dir, "blog.html")
    if os.path.exists(blog_file):
        print("\nUpdating blog.html...")
        
        with open(blog_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Find all article cards and their images
        article_pattern = r'(<article class="article-card"[^>]*>.*?</article>)'
        articles = re.findall(article_pattern, content, re.DOTALL)
        
        updated_content = content
        images_updated = 0
        
        for article in articles:
            # Extract current image src
            img_match = re.search(r'<img src="([^"]+)"', article)
            if img_match:
                current_src = img_match.group(1)
                current_filename = os.path.basename(current_src)
                
                # Get category for this article
                category = get_category_from_article_class(article)
                
                # Check if current image exists
                if current_filename in available_images:
                    # Image exists, ensure path is correct
                    new_src = f"images/{current_filename}"
                    if current_src != new_src:
                        updated_content = updated_content.replace(current_src, new_src)
                        images_updated += 1
                        print(f"  ✓ Updated path: {current_src} -> {new_src}")
                else:
                    # Image doesn't exist, try to find a suitable replacement
                    replacement_found = False
                    
                    # Try to find category-specific images
                    category_images = [img for img in available_images if category in img.lower()]
                    if category_images:
                        new_src = f"images/{category_images[0]}"
                        updated_content = updated_content.replace(current_src, new_src)
                        images_updated += 1
                        print(f"  ✓ Replaced with category image: {current_src} -> {new_src}")
                        replacement_found = True
                    
                    # If no category-specific image, try webp images
                    if not replacement_found:
                        webp_images = [img for img in available_images if img.endswith('.webp')]
                        if webp_images:
                            # Use a different webp image based on article index
                            article_index = articles.index(article) % len(webp_images)
                            new_src = f"images/{webp_images[article_index]}"
                            updated_content = updated_content.replace(current_src, new_src)
                            images_updated += 1
                            print(f"  ✓ Replaced with webp image: {current_src} -> {new_src}")
                            replacement_found = True
                    
                    # If still no replacement, generate SVG
                    if not replacement_found:
                        svg_filename = f"{category}-article-{articles.index(article) + 1}.svg"
                        svg_path = os.path.join(images_dir, svg_filename)
                        
                        # Generate and save SVG
                        svg_content = generate_svg_icon(current_src, category)
                        with open(svg_path, 'w', encoding='utf-8') as svg_file:
                            svg_file.write(svg_content)
                        
                        new_src = f"images/{svg_filename}"
                        updated_content = updated_content.replace(current_src, new_src)
                        images_updated += 1
                        print(f"  ✓ Generated SVG: {current_src} -> {new_src}")
        
        # Save updated blog.html
        if images_updated > 0:
            with open(blog_file, 'w', encoding='utf-8') as f:
                f.write(updated_content)
            print(f"\n✅ Updated {images_updated} images in blog.html")
        else:
            print("\n✅ No images needed updating in blog.html")
    
    # Update individual article files
    articles_dir = os.path.join(base_dir, "articles")
    if os.path.exists(articles_dir):
        print("\nUpdating individual article files...")
        
        article_files = glob.glob(os.path.join(articles_dir, "*.html"))
        total_articles_updated = 0
        total_images_updated = 0
        
        for article_file in article_files:
            with open(article_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Find all img tags
            img_pattern = r'<img([^>]*src="([^"]+)"[^>]*)>'
            images = re.findall(img_pattern, content)
            
            updated_content = content
            article_images_updated = 0
            
            for img_attrs, img_src in images:
                if img_src.startswith('images/'):
                    filename = os.path.basename(img_src)
                    
                    # Check if image exists
                    if filename not in available_images:
                        # Try to find a suitable replacement
                        replacement_found = False
                        
                        # Try webp images first
                        webp_images = [img for img in available_images if img.endswith('.webp')]
                        if webp_images:
                            # Use a random webp image
                            import random
                            new_filename = random.choice(webp_images)
                            new_src = f"images/{new_filename}"
                            updated_content = updated_content.replace(img_src, new_src)
                            article_images_updated += 1
                            replacement_found = True
                        
                        # If no webp, generate SVG
                        if not replacement_found:
                            svg_filename = f"article-image-{len(images)}.svg"
                            svg_path = os.path.join(images_dir, svg_filename)
                            
                            if not os.path.exists(svg_path):
                                svg_content = generate_svg_icon(img_src, "general")
                                with open(svg_path, 'w', encoding='utf-8') as svg_file:
                                    svg_file.write(svg_content)
                            
                            new_src = f"images/{svg_filename}"
                            updated_content = updated_content.replace(img_src, new_src)
                            article_images_updated += 1
            
            # Save updated article if changes were made
            if article_images_updated > 0:
                with open(article_file, 'w', encoding='utf-8') as f:
                    f.write(updated_content)
                total_articles_updated += 1
                total_images_updated += article_images_updated
                print(f"  ✓ Updated {article_images_updated} images in {os.path.basename(article_file)}")
        
        if total_articles_updated > 0:
            print(f"\n✅ Updated {total_images_updated} images across {total_articles_updated} article files")
        else:
            print("\n✅ No article images needed updating")
    
    print("\n🎉 Blog images update completed successfully!")

if __name__ == "__main__":
    update_blog_images()