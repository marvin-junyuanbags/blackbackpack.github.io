#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
批量移除所有文章导航栏中的背包图片
"""

import os
import re
import glob

def remove_navbar_images():
    """移除所有文章导航栏中的背包图片"""
    
    # 获取所有HTML文章文件
    articles_dir = "articles"
    html_files = glob.glob(os.path.join(articles_dir, "*.html"))
    
    print(f"找到 {len(html_files)} 个HTML文件")
    
    # 定义要移除的图片标签模式
    img_pattern = r'<img alt="Black Backpack Logo" class="logo" loading="lazy" src="../images/blackbackpack \([0-9]+\)\.webp"[^>]*/>'
    
    modified_count = 0
    
    for html_file in html_files:
        try:
            # 读取文件内容
            with open(html_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 检查是否包含目标图片标签
            if re.search(img_pattern, content):
                # 移除图片标签，但保留<a>标签结构
                # 将整个img标签替换为空字符串
                new_content = re.sub(img_pattern, '', content)
                
                # 写回文件
                with open(html_file, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                
                modified_count += 1
                print(f"✓ 已处理: {os.path.basename(html_file)}")
            else:
                print(f"- 跳过: {os.path.basename(html_file)} (未找到目标图片)")
                
        except Exception as e:
            print(f"✗ 错误处理 {html_file}: {e}")
    
    print(f"\n处理完成！共修改了 {modified_count} 个文件")
    return modified_count

if __name__ == "__main__":
    remove_navbar_images()