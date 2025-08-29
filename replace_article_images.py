#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
批量替换文章页面中的图片引用为本地存在的背包图片
"""

import os
import re
import glob
from pathlib import Path

def get_available_backpack_images():
    """获取所有可用的背包图片"""
    images_dir = Path('images')
    backpack_images = []
    
    # 查找所有blackbackpack开头的webp文件
    for i in range(1, 58):  # 根据之前的列表，有57个图片
        img_path = images_dir / f'blackbackpack ({i}).webp'
        if img_path.exists():
            backpack_images.append(f'blackbackpack ({i}).webp')
    
    return backpack_images

def replace_images_in_file(file_path, backpack_images):
    """替换单个文件中的图片引用"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # 定义需要替换的图片映射
        image_replacements = {
            # 文章相关图片
            'manufacturing-technology.jpg': 'blackbackpack (10).webp',
            'market-trends.jpg': 'blackbackpack (20).webp',
            'competitive-analysis.jpg': 'blackbackpack (30).webp',
            'brand-building.jpg': 'blackbackpack (40).webp',
            'business-management.jpg': 'blackbackpack (50).webp',
            'custom-design.jpg': 'blackbackpack (5).webp',
            'branding-strategy.jpg': 'blackbackpack (15).webp',
            'cost-analysis.jpg': 'blackbackpack (25).webp',
            'sustainable-manufacturing.jpg': 'blackbackpack (35).webp',
            'innovation-design.jpg': 'blackbackpack (45).webp',
            'human-resources.jpg': 'blackbackpack (55).webp',
            'technology-innovation.jpg': 'blackbackpack (8).webp',
            'environmental-sustainability.jpg': 'blackbackpack (18).webp',
            'customer-experience.jpg': 'blackbackpack (28).webp',
            'digital-transformation.jpg': 'blackbackpack (38).webp',
            'global-expansion-backpack-manufacturing.jpg': 'blackbackpack (48).webp',
            'international-trade-global-expansion.jpg': 'blackbackpack (12).webp',
            'corporate-governance-backpack-manufacturing.jpg': 'blackbackpack (22).webp',
            'project-management-backpack-manufacturing.jpg': 'blackbackpack (32).webp',
            'sustainable-packaging.jpg': 'blackbackpack (42).webp',
            'innovation-management-backpack-manufacturing.jpg': 'blackbackpack (52).webp',
            'customer-experience-service.jpg': 'blackbackpack (7).webp',
            'human-resources-talent.jpg': 'blackbackpack (17).webp',
            'marketing-brand-backpack-manufacturing.jpg': 'blackbackpack (27).webp',
            'data-analytics-backpack-manufacturing.jpg': 'blackbackpack (37).webp',
            'strategic-management-backpack-manufacturing.jpg': 'blackbackpack (47).webp',
            'corporate-culture-backpack-manufacturing.jpg': 'blackbackpack (11).webp',
            'supplier-management-backpack-manufacturing.jpg': 'blackbackpack (21).webp',
            'financial-management-manufacturing.jpg': 'blackbackpack (31).webp',
            'risk-management-backpack-manufacturing.jpg': 'blackbackpack (41).webp',
            'innovation-product-development.jpg': 'blackbackpack (51).webp',
            'legal-compliance-ip.jpg': 'blackbackpack (6).webp',
            'hr-workforce-development-manufacturing.jpg': 'blackbackpack (16).webp',
            'brand-building-strategies.jpg': 'blackbackpack (26).webp',
            'market-trends-analysis.jpg': 'blackbackpack (36).webp',
            'technology-innovation-digital.jpg': 'blackbackpack (46).webp',
            'csr-sustainability.jpg': 'blackbackpack (56).webp',
            # Logo保持不变
            'logo.png': 'logo.svg'
        }
        
        # 执行替换
        changes_made = False
        for old_img, new_img in image_replacements.items():
            if old_img in content:
                content = content.replace(old_img, new_img)
                changes_made = True
                print(f"  替换: {old_img} -> {new_img}")
        
        # 如果有更改，写回文件
        if changes_made:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            return True
        
        return False
        
    except Exception as e:
        print(f"处理文件 {file_path} 时出错: {e}")
        return False

def main():
    """主函数"""
    print("开始替换文章页面中的图片引用...")
    
    # 获取可用的背包图片
    backpack_images = get_available_backpack_images()
    print(f"找到 {len(backpack_images)} 个可用的背包图片")
    
    # 查找所有HTML文件
    html_files = []
    html_files.extend(glob.glob('*.html'))
    html_files.extend(glob.glob('articles/*.html'))
    
    print(f"找到 {len(html_files)} 个HTML文件")
    
    updated_files = 0
    
    # 处理每个文件
    for file_path in html_files:
        print(f"\n处理文件: {file_path}")
        if replace_images_in_file(file_path, backpack_images):
            updated_files += 1
            print(f"  ✓ 已更新")
        else:
            print(f"  - 无需更新")
    
    print(f"\n完成！共更新了 {updated_files} 个文件")

if __name__ == '__main__':
    main()