#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
恢复blackbackpack图片引用脚本
将HTML文件中错误的blackbackpack-X.svg引用恢复为原始的blackbackpack (X).webp格式
"""

import os
import re
import glob

def restore_image_references():
    """恢复所有HTML文件中的blackbackpack图片引用"""
    
    # 获取所有HTML文件
    html_files = []
    
    # 根目录下的HTML文件
    for file in glob.glob('*.html'):
        html_files.append(file)
    
    # articles目录下的HTML文件
    articles_dir = 'articles'
    if os.path.exists(articles_dir):
        for file in glob.glob(os.path.join(articles_dir, '*.html')):
            html_files.append(file)
    
    print(f"找到 {len(html_files)} 个HTML文件需要处理")
    
    updated_files = 0
    total_replacements = 0
    
    for html_file in html_files:
        try:
            with open(html_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            original_content = content
            
            # 将blackbackpack-X.svg恢复为blackbackpack (X).webp
            # 匹配模式: blackbackpack-数字.svg
            def replace_svg_to_webp(match):
                number = match.group(1)
                return f'blackbackpack ({number}).webp'
            
            content = re.sub(r'blackbackpack-(\d+)\.svg', replace_svg_to_webp, content)
            
            # 统计替换次数
            replacements = len(re.findall(r'blackbackpack-\d+\.svg', original_content))
            
            if content != original_content:
                with open(html_file, 'w', encoding='utf-8') as f:
                    f.write(content)
                
                updated_files += 1
                total_replacements += replacements
                print(f"✓ 更新文件: {html_file} (替换了 {replacements} 个引用)")
            
        except Exception as e:
            print(f"✗ 处理文件 {html_file} 时出错: {e}")
    
    print(f"\n恢复完成!")
    print(f"- 更新了 {updated_files} 个文件")
    print(f"- 总共恢复了 {total_replacements} 个图片引用")
    print(f"- 所有blackbackpack-X.svg引用已恢复为blackbackpack (X).webp")

if __name__ == '__main__':
    # 切换到脚本所在目录
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)
    
    print("开始恢复blackbackpack图片引用...")
    restore_image_references()
    print("恢复操作完成!")