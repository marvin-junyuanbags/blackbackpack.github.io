#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import re
from pathlib import Path

def get_referenced_images():
    """获取所有HTML文件中引用的图片"""
    referenced_images = set()
    
    # 搜索所有HTML文件
    for html_file in Path('.').rglob('*.html'):
        try:
            with open(html_file, 'r', encoding='utf-8') as f:
                content = f.read()
                
            # 查找所有图片引用
            # 匹配 src="images/..." 和 src="../images/..."
            img_patterns = [
                r'src="images/([^"]+)"',
                r'src="\.\.?/images/([^"]+)"',
                r'content="[^"]*images/([^"]+)"',
                r'content="[^"]*\.\./images/([^"]+)"'
            ]
            
            for pattern in img_patterns:
                matches = re.findall(pattern, content)
                for match in matches:
                    referenced_images.add(match)
                    
        except Exception as e:
            print(f"Error reading {html_file}: {e}")
    
    return referenced_images

def get_existing_images():
    """获取images目录中实际存在的图片文件"""
    existing_images = set()
    images_dir = Path('images')
    
    if images_dir.exists():
        for img_file in images_dir.iterdir():
            if img_file.is_file() and img_file.suffix.lower() in ['.svg', '.png', '.jpg', '.jpeg', '.webp']:
                existing_images.add(img_file.name)
    
    return existing_images

def create_missing_svg(filename, title=None):
    """创建缺失的SVG图片"""
    if not title:
        title = filename.replace('-', ' ').replace('.svg', '').title()
    
    svg_content = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 300" width="400" height="300">
  <defs>
    <linearGradient id="bg" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:#1a1a1a;stop-opacity:1" />
      <stop offset="100%" style="stop-color:#333333;stop-opacity:1" />
    </linearGradient>
  </defs>
  
  <!-- Background -->
  <rect width="400" height="300" fill="url(#bg)"/>
  
  <!-- Icon placeholder -->
  <circle cx="200" cy="120" r="40" fill="#666" opacity="0.8"/>
  <rect x="180" y="100" width="40" height="40" fill="#999" opacity="0.6"/>
  
  <!-- Title -->
  <text x="200" y="200" text-anchor="middle" fill="#ffffff" font-family="Arial, sans-serif" font-size="16" font-weight="bold">
    {title}
  </text>
  
  <!-- Subtitle -->
  <text x="200" y="220" text-anchor="middle" fill="#cccccc" font-family="Arial, sans-serif" font-size="12">
    Professional Backpack Solutions
  </text>
  
  <!-- Decorative elements -->
  <rect x="50" y="250" width="300" height="2" fill="#666" opacity="0.5"/>
  <circle cx="80" cy="270" r="3" fill="#999"/>
  <circle cx="200" cy="270" r="3" fill="#999"/>
  <circle cx="320" cy="270" r="3" fill="#999"/>
</svg>'''
    
    return svg_content

def main():
    print("检查缺失的图片文件...")
    
    referenced_images = get_referenced_images()
    existing_images = get_existing_images()
    
    missing_images = referenced_images - existing_images
    
    print(f"\n引用的图片总数: {len(referenced_images)}")
    print(f"存在的图片总数: {len(existing_images)}")
    print(f"缺失的图片总数: {len(missing_images)}")
    
    if missing_images:
        print("\n缺失的图片文件:")
        for img in sorted(missing_images):
            print(f"  - {img}")
        
        # 创建缺失的图片
        images_dir = Path('images')
        images_dir.mkdir(exist_ok=True)
        
        created_count = 0
        for img in missing_images:
            img_path = images_dir / img
            
            if img.endswith('.svg'):
                # 创建SVG文件
                title = img.replace('-', ' ').replace('.svg', '').title()
                svg_content = create_missing_svg(img, title)
                
                try:
                    with open(img_path, 'w', encoding='utf-8') as f:
                        f.write(svg_content)
                    print(f"✓ 创建了 {img}")
                    created_count += 1
                except Exception as e:
                    print(f"✗ 创建 {img} 失败: {e}")
            
            elif img.endswith(('.jpg', '.jpeg', '.png', '.webp')):
                # 对于非SVG图片，创建一个占位符SVG
                placeholder_name = img.rsplit('.', 1)[0] + '.svg'
                placeholder_path = images_dir / placeholder_name
                
                if not placeholder_path.exists():
                    title = img.replace('-', ' ').rsplit('.', 1)[0].title()
                    svg_content = create_missing_svg(placeholder_name, title)
                    
                    try:
                        with open(placeholder_path, 'w', encoding='utf-8') as f:
                            f.write(svg_content)
                        print(f"✓ 创建了占位符 {placeholder_name} (替代 {img})")
                        created_count += 1
                    except Exception as e:
                        print(f"✗ 创建占位符 {placeholder_name} 失败: {e}")
        
        print(f"\n成功创建了 {created_count} 个图片文件")
    else:
        print("\n✓ 所有引用的图片文件都存在")

if __name__ == "__main__":
    main()