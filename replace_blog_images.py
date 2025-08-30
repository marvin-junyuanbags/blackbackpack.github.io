#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
import os

def replace_blog_images():
    """Replace remaining logo.svg references in blog.html with webp images"""
    
    blog_file = 'blog.html'
    
    if not os.path.exists(blog_file):
        print(f"Error: {blog_file} not found")
        return
    
    # Read the file
    with open(blog_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Count current logo.svg references
    logo_count = content.count('images/logo.svg')
    print(f"Found {logo_count} logo.svg references to replace")
    
    if logo_count == 0:
        print("No logo.svg references found to replace")
        return
    
    # Available webp images (continuing from where we left off)
    webp_images = [
        'blackbackpack (23).webp',
        'blackbackpack (24).webp', 
        'blackbackpack (25).webp',
        'blackbackpack (26).webp',
        'blackbackpack (27).webp',
        'blackbackpack (28).webp',
        'blackbackpack (29).webp',
        'blackbackpack (30).webp',
        'blackbackpack (31).webp',
        'blackbackpack (32).webp',
        'blackbackpack (33).webp',
        'blackbackpack (34).webp',
        'blackbackpack (35).webp',
        'blackbackpack (36).webp',
        'blackbackpack (37).webp',
        'blackbackpack (38).webp',
        'blackbackpack (39).webp',
        'blackbackpack (40).webp',
        'blackbackpack (41).webp',
        'blackbackpack (42).webp',
        'blackbackpack (43).webp',
        'blackbackpack (44).webp',
        'blackbackpack (45).webp',
        'blackbackpack (46).webp',
        'blackbackpack (47).webp',
        'blackbackpack (48).webp',
        'blackbackpack (49).webp',
        'blackbackpack (50).webp',
        'blackbackpack (51).webp',
        'blackbackpack (52).webp',
        'blackbackpack (53).webp',
        'blackbackpack (54).webp',
        'blackbackpack (55).webp',
        'blackbackpack (56).webp',
        'blackbackpack (57).webp',
        'blackbackpack (58).webp',
        'blackbackpack (59).webp',
        'blackbackpack (60).webp'
    ]
    
    # Replace logo.svg references one by one
    replacement_count = 0
    webp_index = 0
    
    # Find and replace each logo.svg reference
    while 'images/logo.svg' in content and webp_index < len(webp_images):
        # Replace the first occurrence
        content = content.replace('images/logo.svg', f'images/{webp_images[webp_index]}', 1)
        replacement_count += 1
        webp_index += 1
        
        if replacement_count % 5 == 0:
            print(f"Replaced {replacement_count} references...")
    
    # Write the updated content back
    with open(blog_file, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"Successfully replaced {replacement_count} logo.svg references with webp images")
    
    # Check for any remaining logo.svg references
    remaining_count = content.count('images/logo.svg')
    if remaining_count > 0:
        print(f"Warning: {remaining_count} logo.svg references still remain")
    else:
        print("All logo.svg references have been successfully replaced!")

if __name__ == '__main__':
    replace_blog_images()