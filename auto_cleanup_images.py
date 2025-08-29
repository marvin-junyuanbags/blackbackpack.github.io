#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
自动图片文件清理脚本
分析当前网站使用的图片文件，自动删除未使用的文件
"""

import os
import re
from pathlib import Path

def get_used_images():
    """获取网站中实际使用的所有图片文件"""
    used_images = set()
    project_root = Path('.')
    
    # 搜索所有HTML文件中的图片引用
    html_files = list(project_root.glob('*.html'))
    
    for html_file in html_files:
        try:
            with open(html_file, 'r', encoding='utf-8') as f:
                content = f.read()
                
            # 查找所有图片引用
            # 匹配 src="images/filename.ext" 格式
            img_matches = re.findall(r'src=["\']images/([^"\'\']+)["\']', content)
            for img in img_matches:
                used_images.add(img)
                
            # 匹配 content="...images/filename.ext" 格式 (meta标签)
            meta_matches = re.findall(r'content=["\'][^"\'\']*images/([^"\'\']+)["\']', content)
            for img in meta_matches:
                used_images.add(img)
                
            # 匹配 background-image: url('images/filename.ext') 格式
            bg_matches = re.findall(r'background-image:\s*url\(["\']?images/([^"\'\'\)]+)["\']?\)', content)
            for img in bg_matches:
                used_images.add(img)
                
        except Exception as e:
            print(f"读取文件 {html_file} 时出错: {e}")
    
    return used_images

def get_all_image_files():
    """获取images目录下的所有图片文件"""
    images_dir = Path('images')
    if not images_dir.exists():
        return set()
    
    all_images = set()
    for img_file in images_dir.iterdir():
        if img_file.is_file() and img_file.suffix.lower() in ['.svg', '.webp', '.jpg', '.png', '.gif']:
            all_images.add(img_file.name)
    
    return all_images

def main():
    print("开始分析网站使用的图片文件...")
    
    # 获取使用的图片和所有图片
    used_images = get_used_images()
    all_images = get_all_image_files()
    
    print(f"\n发现 {len(all_images)} 个图片文件")
    print(f"网站实际使用 {len(used_images)} 个图片文件")
    
    # 找出未使用的图片
    unused_images = all_images - used_images
    
    print(f"\n未使用的图片文件 ({len(unused_images)} 个)")
    
    if unused_images:
        images_dir = Path('images')
        deleted_count = 0
        
        print("\n开始删除未使用的图片文件...")
        for img in sorted(unused_images):
            img_path = images_dir / img
            try:
                img_path.unlink()
                deleted_count += 1
                print(f"已删除: {img}")
            except Exception as e:
                print(f"删除 {img} 时出错: {e}")
        
        print(f"\n成功删除 {deleted_count} 个未使用的图片文件")
        print(f"images目录现在有 {len(all_images) - deleted_count} 个文件")
    else:
        print("所有图片文件都在使用中，无需删除")
    
    print(f"\n保留的图片文件 ({len(used_images)} 个):")
    for img in sorted(used_images):
        print(f"  - {img}")

if __name__ == '__main__':
    main()