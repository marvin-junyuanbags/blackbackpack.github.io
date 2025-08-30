#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Verify SVG Replacement Script
验证SVG图片替换结果的脚本
"""

import re
import os

def verify_svg_replacement(file_path):
    """
    验证文件中是否还有SVG图片引用
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        
        # 查找所有.svg引用
        svg_pattern = r'src="[^"]*\.svg[^"]*"'
        svg_matches = re.findall(svg_pattern, content)
        
        if svg_matches:
            print(f"在 {file_path} 中发现 {len(svg_matches)} 个SVG引用:")
            for i, match in enumerate(svg_matches, 1):
                print(f"  {i}. {match}")
            return False
        else:
            print(f"✓ {file_path} 中没有发现SVG引用")
            return True
            
    except Exception as e:
        print(f"读取文件 {file_path} 时出错: {e}")
        return False

def count_webp_images(file_path):
    """
    统计文件中WEBP图片的数量
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        
        # 查找所有.webp引用
        webp_pattern = r'src="[^"]*\.webp[^"]*"'
        webp_matches = re.findall(webp_pattern, content)
        
        print(f"在 {file_path} 中发现 {len(webp_matches)} 个WEBP图片引用")
        return len(webp_matches)
        
    except Exception as e:
        print(f"读取文件 {file_path} 时出错: {e}")
        return 0

if __name__ == "__main__":
    blog_file = "blog.html"
    
    print("=== SVG替换验证结果 ===")
    print()
    
    # 验证SVG替换
    is_clean = verify_svg_replacement(blog_file)
    print()
    
    # 统计WEBP图片数量
    webp_count = count_webp_images(blog_file)
    print()
    
    if is_clean:
        print("🎉 所有SVG图片引用已成功替换为WEBP格式!")
        print(f"总共有 {webp_count} 个WEBP图片引用")
    else:
        print("⚠️  仍有SVG引用需要处理")
    
    print("\n验证完成!")