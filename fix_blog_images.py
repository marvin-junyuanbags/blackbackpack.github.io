#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Blog Images Fix Script
修复BLOG页面和文章内部图片问题
1. 替换BLOG页面中的logo.svg为合适的产品图片
2. 调整文章内部第一张配图的尺寸
"""

import os
import re
from pathlib import Path

def get_available_images():
    """获取可用的产品图片列表"""
    images_dir = Path('images')
    if not images_dir.exists():
        return []
    
    # 获取所有webp格式的blackbackpack图片
    webp_images = list(images_dir.glob('blackbackpack*.webp'))
    return [img.name for img in webp_images]

def fix_blog_page_images():
    """修复BLOG页面的图片"""
    blog_file = Path('blog.html')
    if not blog_file.exists():
        print("Blog.html文件不存在")
        return
    
    # 读取blog.html内容
    with open(blog_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 获取可用图片
    available_images = get_available_images()
    if not available_images:
        print("没有找到可用的产品图片")
        return
    
    # 替换logo.svg为产品图片
    # 为不同类别的文章分配不同的图片
    image_mapping = {
        'manufacturing': 'blackbackpack (1).webp',
        'technology': 'blackbackpack (2).webp', 
        'design': 'blackbackpack (3).webp',
        'materials': 'blackbackpack (4).webp',
        'business': 'blackbackpack (5).webp',
        'trends': 'blackbackpack (6).webp',
        'sustainability': 'blackbackpack (7).webp',
        'guides': 'blackbackpack (8).webp'
    }
    
    # 计数器用于循环分配图片
    image_counter = 1
    
    def replace_logo_svg(match):
        nonlocal image_counter
        full_match = match.group(0)
        
        # 检查是否包含logo.svg
        if 'logo.svg' in full_match:
            # 选择图片
            if image_counter <= len(available_images):
                selected_image = available_images[image_counter - 1]
            else:
                selected_image = available_images[(image_counter - 1) % len(available_images)]
            
            # 替换图片路径
            new_match = full_match.replace('logo.svg', selected_image)
            image_counter += 1
            return new_match
        
        return full_match
    
    # 使用正则表达式替换logo.svg
    pattern = r'<img[^>]*src="[^"]*logo\.svg"[^>]*>'
    content = re.sub(pattern, replace_logo_svg, content)
    
    # 写回文件
    with open(blog_file, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"Blog页面图片修复完成，替换了 {image_counter - 1} 个logo.svg图片")

def fix_article_first_images():
    """修复文章内部第一张配图的尺寸"""
    articles_dir = Path('articles')
    if not articles_dir.exists():
        print("Articles目录不存在")
        return
    
    html_files = list(articles_dir.glob('*.html'))
    fixed_count = 0
    
    for html_file in html_files:
        try:
            with open(html_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            original_content = content
            
            # 查找第一张配图（在header之后的第一个img标签）
            # 匹配模式：在</header>之后的第一个img标签
            header_end_pattern = r'</header>'
            header_match = re.search(header_end_pattern, content)
            
            if header_match:
                # 从header结束位置开始查找第一个img标签
                start_pos = header_match.end()
                remaining_content = content[start_pos:]
                
                # 查找第一个img标签，但排除logo图片
                img_pattern = r'<img[^>]*src="[^"]*(?:blackbackpack|images/)[^"]*"[^>]*style="[^"]*width:\s*640px[^"]*"[^>]*>'
                img_match = re.search(img_pattern, remaining_content)
                
                if img_match:
                    # 找到第一张配图，调整其尺寸
                    old_img = img_match.group(0)
                    
                    # 将640px改为200px，保持其他样式不变
                    new_img = re.sub(r'width:\s*640px', 'width: 200px', old_img)
                    new_img = re.sub(r'height:\s*640px', 'height: 200px', new_img)
                    
                    # 替换内容
                    new_remaining = remaining_content.replace(old_img, new_img, 1)
                    content = content[:start_pos] + new_remaining
                    
                    # 如果内容有变化，写回文件
                    if content != original_content:
                        with open(html_file, 'w', encoding='utf-8') as f:
                            f.write(content)
                        fixed_count += 1
                        print(f"修复文章: {html_file.name}")
        
        except Exception as e:
            print(f"处理文件 {html_file.name} 时出错: {e}")
    
    print(f"文章第一张配图尺寸修复完成，共修复 {fixed_count} 篇文章")

def main():
    """主函数"""
    print("开始修复BLOG页面和文章图片问题...")
    
    # 切换到正确的目录
    os.chdir('C:/Users/A1775/blackbackpack.co.uk')
    
    # 1. 修复BLOG页面图片
    print("\n1. 修复BLOG页面图片...")
    fix_blog_page_images()
    
    # 2. 修复文章内部第一张配图尺寸
    print("\n2. 修复文章内部第一张配图尺寸...")
    fix_article_first_images()
    
    print("\n所有图片问题修复完成！")

if __name__ == '__main__':
    main()