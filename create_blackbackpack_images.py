#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
创建缺失的blackbackpack (X).webp图片
使用现有的backpack图片或生成SVG图片
"""

import os
import re
from pathlib import Path
import shutil

def create_backpack_svg(number, theme):
    """创建背包主题的SVG图片"""
    themes = {
        'business': {
            'color1': '#1f2937',
            'color2': '#374151',
            'accent': '#3b82f6',
            'title': 'Business Backpack'
        },
        'outdoor': {
            'color1': '#065f46',
            'color2': '#047857',
            'accent': '#10b981',
            'title': 'Outdoor Backpack'
        },
        'school': {
            'color1': '#7c2d12',
            'color2': '#dc2626',
            'accent': '#f59e0b',
            'title': 'School Backpack'
        },
        'travel': {
            'color1': '#581c87',
            'color2': '#7c3aed',
            'accent': '#a855f7',
            'title': 'Travel Backpack'
        },
        'sports': {
            'color1': '#b91c1c',
            'color2': '#dc2626',
            'accent': '#f97316',
            'title': 'Sports Backpack'
        },
        'tactical': {
            'color1': '#374151',
            'color2': '#4b5563',
            'accent': '#6b7280',
            'title': 'Tactical Backpack'
        }
    }
    
    theme_data = themes.get(theme, themes['business'])
    
    svg_content = f'''<svg width="400" height="300" viewBox="0 0 400 300" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="bgGrad{number}" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:{theme_data['color1']};stop-opacity:1" />
      <stop offset="100%" style="stop-color:{theme_data['color2']};stop-opacity:1" />
    </linearGradient>
    <linearGradient id="backpackGrad{number}" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:#000000;stop-opacity:0.8" />
      <stop offset="100%" style="stop-color:#1f1f1f;stop-opacity:0.9" />
    </linearGradient>
  </defs>
  
  <!-- Background -->
  <rect width="400" height="300" fill="url(#bgGrad{number})"/>
  
  <!-- Backpack Main Body -->
  <path d="M150 80 L250 80 L260 90 L260 220 L140 220 L140 90 Z" fill="url(#backpackGrad{number})" stroke="#333" stroke-width="2"/>
  
  <!-- Front Pocket -->
  <rect x="160" y="120" width="80" height="60" fill="#2a2a2a" stroke="#444" stroke-width="1" rx="5"/>
  
  <!-- Straps -->
  <rect x="130" y="85" width="8" height="120" fill="#1a1a1a" rx="4"/>
  <rect x="262" y="85" width="8" height="120" fill="#1a1a1a" rx="4"/>
  
  <!-- Top Handle -->
  <rect x="180" y="70" width="40" height="8" fill="#1a1a1a" rx="4"/>
  
  <!-- Zippers -->
  <line x1="170" y1="130" x2="230" y2="130" stroke="{theme_data['accent']}" stroke-width="2"/>
  <line x1="150" y1="90" x2="250" y2="90" stroke="{theme_data['accent']}" stroke-width="2"/>
  
  <!-- Logo Area -->
  <circle cx="200" cy="150" r="15" fill="{theme_data['accent']}" opacity="0.8"/>
  <text x="200" y="155" text-anchor="middle" fill="white" font-family="Arial, sans-serif" font-size="10" font-weight="bold">BB</text>
  
  <!-- Title -->
  <text x="200" y="260" text-anchor="middle" fill="white" font-family="Arial, sans-serif" font-size="16" font-weight="bold">{theme_data['title']}</text>
  <text x="200" y="280" text-anchor="middle" fill="#d1d5db" font-family="Arial, sans-serif" font-size="12">Premium Quality</text>
</svg>'''
    return svg_content

def create_blackbackpack_images():
    """创建所需的blackbackpack图片"""
    base_dir = Path('.')
    images_dir = base_dir / 'images'
    
    # 定义主题分配
    theme_mapping = {
        1: 'business', 2: 'business', 3: 'business', 4: 'business',
        5: 'sports', 6: 'sports', 7: 'sports', 8: 'sports',
        9: 'outdoor', 10: 'outdoor', 11: 'outdoor', 12: 'outdoor',
        13: 'school', 14: 'school', 15: 'school', 16: 'school',
        17: 'business', 18: 'business', 19: 'business', 20: 'business',
        21: 'tactical', 22: 'tactical', 23: 'tactical', 24: 'tactical',
        25: 'travel', 26: 'travel', 27: 'travel', 28: 'travel',
        29: 'business', 30: 'business', 31: 'business', 32: 'business',
        33: 'outdoor', 34: 'outdoor', 35: 'outdoor', 36: 'outdoor',
        37: 'sports', 38: 'sports', 39: 'sports', 40: 'sports',
        41: 'tactical', 42: 'tactical', 43: 'tactical', 44: 'tactical',
        45: 'travel', 46: 'travel', 47: 'travel', 48: 'travel',
        49: 'school', 50: 'school', 51: 'school', 52: 'school',
        53: 'business', 54: 'business', 55: 'business', 56: 'business'
    }
    
    # 创建blackbackpack (X).webp文件
    for i in range(1, 57):  # 创建1-56号图片
        filename = f"blackbackpack ({i}).webp"
        filepath = images_dir / filename
        
        if not filepath.exists():
            # 创建对应的SVG文件
            svg_filename = f"blackbackpack-{i}.svg"
            svg_filepath = images_dir / svg_filename
            
            theme = theme_mapping.get(i, 'business')
            svg_content = create_backpack_svg(i, theme)
            
            with open(svg_filepath, 'w', encoding='utf-8') as f:
                f.write(svg_content)
            
            print(f"Created SVG: {svg_filename}")
            
            # 创建一个简单的占位符webp文件（实际上是SVG内容）
            # 由于我们无法直接创建webp文件，我们创建SVG并在HTML中引用SVG
            print(f"SVG created for: {filename}")
    
    print(f"\n已创建 {len(theme_mapping)} 个背包主题SVG图片")
    
    # 更新HTML文件，将.webp引用替换为.svg
    html_files = list(base_dir.glob('*.html')) + list(base_dir.glob('articles/*.html'))
    
    for html_file in html_files:
        try:
            with open(html_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            original_content = content
            
            # 替换blackbackpack (X).webp为blackbackpack-X.svg
            for i in range(1, 57):
                old_ref = f"blackbackpack ({i}).webp"
                new_ref = f"blackbackpack-{i}.svg"
                content = content.replace(old_ref, new_ref)
            
            # 如果内容有变化，写回文件
            if content != original_content:
                with open(html_file, 'w', encoding='utf-8') as f:
                    f.write(content)
                print(f"Updated: {html_file}")
                
        except Exception as e:
            print(f"Error processing {html_file}: {e}")
    
    print("\n所有blackbackpack图片引用已更新为SVG格式！")

if __name__ == '__main__':
    create_blackbackpack_images()