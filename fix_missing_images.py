#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
修复网站中缺失的图片文件
将不存在的图片替换为现有的backpack图片或生成SVG图片
"""

import os
import re
from pathlib import Path

def create_author_svg(filename, name, role):
    """创建作者头像SVG"""
    svg_content = f'''<svg width="80" height="80" viewBox="0 0 80 80" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="avatarGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:#2563eb;stop-opacity:1" />
      <stop offset="100%" style="stop-color:#1e40af;stop-opacity:1" />
    </linearGradient>
  </defs>
  <circle cx="40" cy="40" r="40" fill="url(#avatarGrad)"/>
  <circle cx="40" cy="30" r="12" fill="white" opacity="0.9"/>
  <path d="M20 65 Q20 50 40 50 Q60 50 60 65 L60 80 L20 80 Z" fill="white" opacity="0.9"/>
  <text x="40" y="75" text-anchor="middle" fill="white" font-family="Arial, sans-serif" font-size="8" font-weight="bold">{role}</text>
</svg>'''
    return svg_content

def create_hero_image_svg(filename, title):
    """创建英雄图片SVG"""
    svg_content = f'''<svg width="800" height="400" viewBox="0 0 800 400" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="heroGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:#1f2937;stop-opacity:1" />
      <stop offset="50%" style="stop-color:#374151;stop-opacity:1" />
      <stop offset="100%" style="stop-color:#111827;stop-opacity:1" />
    </linearGradient>
    <pattern id="backpackPattern" x="0" y="0" width="100" height="100" patternUnits="userSpaceOnUse">
      <rect width="100" height="100" fill="#1f2937" opacity="0.1"/>
      <path d="M30 20 L70 20 L75 25 L75 75 L25 75 L25 25 Z" fill="#374151" opacity="0.3"/>
      <rect x="35" y="30" width="30" height="35" fill="#4b5563" opacity="0.4"/>
      <circle cx="40" cy="25" r="3" fill="#6b7280"/>
      <circle cx="60" cy="25" r="3" fill="#6b7280"/>
    </pattern>
  </defs>
  <rect width="800" height="400" fill="url(#heroGrad)"/>
  <rect width="800" height="400" fill="url(#backpackPattern)" opacity="0.3"/>
  <text x="400" y="200" text-anchor="middle" fill="white" font-family="Arial, sans-serif" font-size="32" font-weight="bold">{title}</text>
  <text x="400" y="240" text-anchor="middle" fill="#d1d5db" font-family="Arial, sans-serif" font-size="16">Professional Backpack Manufacturing</text>
</svg>'''
    return svg_content

def fix_images():
    """修复缺失的图片"""
    base_dir = Path('.')
    images_dir = base_dir / 'images'
    
    # 需要创建的作者头像
    author_images = {
        'author-finance.jpg': ('Finance Expert', 'FINANCE'),
        'author-manufacturing-expert.jpg': ('Manufacturing Expert', 'MFG'),
        'author-market-research.jpg': ('Market Research', 'MARKET'),
        'author-tech.jpg': ('Tech Expert', 'TECH'),
        'author-design.jpg': ('Design Expert', 'DESIGN'),
        'author-sustainability.jpg': ('Sustainability', 'ECO'),
        'author-quality-control.jpg': ('Quality Expert', 'QC'),
        'author-supply-chain.jpg': ('Supply Chain', 'SC'),
        'author-business.jpg': ('Business Expert', 'BIZ'),
        'author-innovation.jpg': ('Innovation', 'INNOV')
    }
    
    # 需要创建的英雄图片
    hero_images = {
        'laptop-backpack-hero.jpg': 'Professional Laptop Backpacks',
        'outdoor-backpack-hero.jpg': 'Professional Outdoor Backpacks',
        'case-study-tech-company.jpg': 'Tech Company Case Study',
        'case-study-university.jpg': 'University Case Study',
        'case-study-retail.jpg': 'Retail Case Study'
    }
    
    # 创建作者头像SVG
    for filename, (name, role) in author_images.items():
        svg_filename = filename.replace('.jpg', '.svg')
        svg_path = images_dir / svg_filename
        if not svg_path.exists():
            svg_content = create_author_svg(svg_filename, name, role)
            with open(svg_path, 'w', encoding='utf-8') as f:
                f.write(svg_content)
            print(f"Created: {svg_filename}")
    
    # 创建英雄图片SVG
    for filename, title in hero_images.items():
        svg_filename = filename.replace('.jpg', '.svg')
        svg_path = images_dir / svg_filename
        if not svg_path.exists():
            svg_content = create_hero_image_svg(svg_filename, title)
            with open(svg_path, 'w', encoding='utf-8') as f:
                f.write(svg_content)
            print(f"Created: {svg_filename}")
    
    # 更新HTML文件中的图片引用
    html_files = list(base_dir.glob('*.html')) + list(base_dir.glob('articles/*.html'))
    
    replacements = {
        # 作者头像替换
        'author-finance.jpg': 'author-finance.svg',
        'author-manufacturing-expert.jpg': 'author-manufacturing-expert.svg',
        'author-market-research.jpg': 'author-market-research.svg',
        'author-tech.jpg': 'author-tech.svg',
        'author-design.jpg': 'author-design.svg',
        'author-sustainability.jpg': 'author-sustainability.svg',
        'author-quality-control.jpg': 'author-quality-control.svg',
        'author-supply-chain.jpg': 'author-supply-chain.svg',
        'author-business.jpg': 'author-business.svg',
        'author-innovation.jpg': 'author-innovation.svg',
        # 英雄图片替换
        'laptop-backpack-hero.jpg': 'laptop-backpack-hero.svg',
        'outdoor-backpack-hero.jpg': 'outdoor-backpack-hero.svg',
        'case-study-tech-company.jpg': 'case-study-tech-company.svg',
        'case-study-university.jpg': 'case-study-university.svg',
        'case-study-retail.jpg': 'case-study-retail.svg'
    }
    
    for html_file in html_files:
        try:
            with open(html_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            original_content = content
            
            # 替换图片引用
            for old_img, new_img in replacements.items():
                content = content.replace(old_img, new_img)
            
            # 如果内容有变化，写回文件
            if content != original_content:
                with open(html_file, 'w', encoding='utf-8') as f:
                    f.write(content)
                print(f"Updated: {html_file}")
                
        except Exception as e:
            print(f"Error processing {html_file}: {e}")
    
    print("\n图片修复完成！")
    print("已创建的SVG图片:")
    for svg_file in images_dir.glob('author-*.svg'):
        print(f"  - {svg_file.name}")
    for svg_file in images_dir.glob('*-hero.svg'):
        print(f"  - {svg_file.name}")
    for svg_file in images_dir.glob('case-study-*.svg'):
        print(f"  - {svg_file.name}")

if __name__ == '__main__':
    fix_images()