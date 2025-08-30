#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
批量更新blackbackpack.co.uk网站中的联系信息
将旧的联系信息替换为新的Junyuan Bags联系信息
"""

import os
import re
from pathlib import Path

def update_contact_info():
    """
    批量更新网站中的联系信息
    """
    # 网站根目录
    website_root = Path(r'c:\Users\A1775\blackbackpack.co.uk')
    
    # 需要替换的内容映射
    replacements = {
        # 邮箱替换
        r'info@blackbackpack\.co\.uk': 'cco@junyuanbags.com',
        
        # 电话号码替换
        r'\+44 20 1234 5678': 'WhatsApp +86 17750020688',
        
        # Connect with Junyuan Bags部分的更新
        r'📧 Email: info@junyuanbags\.com\s*\n\s*🌐 Website: www\.junyuanbags\.com\s*\n\s*📱 WhatsApp: \+86 138 0262 9738': 
        '📧 Email: cco@junyuanbags.com\n🌐 Website: www.junyuanbags.com\n📱 WhatsApp: +86 17750020688',
        
        # 单独的info@junyuanbags.com替换为cco@junyuanbags.com
        r'info@junyuanbags\.com': 'cco@junyuanbags.com',
        
        # WhatsApp号码更新
        r'\+86 138 0262 9738': '+86 17750020688',
        r'\+86 15920637637': '+86 17750020688'
    }
    
    # 需要处理的文件扩展名
    file_extensions = ['.html', '.py']
    
    # 统计信息
    files_processed = 0
    files_updated = 0
    
    print("开始更新联系信息...")
    
    # 遍历所有文件
    for file_path in website_root.rglob('*'):
        if file_path.is_file() and file_path.suffix in file_extensions:
            # 跳过当前脚本文件
            if file_path.name == 'update_contact_info.py':
                continue
                
            try:
                # 读取文件内容
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                original_content = content
                files_processed += 1
                
                # 应用所有替换规则
                for pattern, replacement in replacements.items():
                    content = re.sub(pattern, replacement, content, flags=re.MULTILINE)
                
                # 如果内容有变化，写回文件
                if content != original_content:
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(content)
                    files_updated += 1
                    print(f"已更新: {file_path.relative_to(website_root)}")
                    
            except Exception as e:
                print(f"处理文件 {file_path} 时出错: {e}")
    
    print(f"\n更新完成!")
    print(f"处理文件数: {files_processed}")
    print(f"更新文件数: {files_updated}")

if __name__ == '__main__':
    update_contact_info()