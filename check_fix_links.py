#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
检查并修复blackbackpack.co.uk网站中的链接问题
"""

import os
import re
from pathlib import Path

def check_and_fix_links():
    """
    检查并修复网站中的链接问题
    """
    website_root = Path(r'c:\Users\A1775\blackbackpack.co.uk')
    
    # 需要修复的链接映射
    link_fixes = {
        # 统一隐私政策链接
        r'href="privacy\.html"': 'href="privacy-policy.html"',
        
        # 统一服务条款链接
        r'href="terms\.html"': 'href="terms-of-service.html"',
        
        # 修复空链接
        r'href="#"(?!\s+aria-label)': 'href="javascript:void(0)"',
        
        # 修复sitemap链接
        r'<a href="#">Sitemap</a>': '<a href="sitemap.html">Sitemap</a>',
        
        # 修复cookies链接
        r'href="cookies\.html"': 'href="cookie-policy.html"',
    }
    
    # 需要检查是否存在的页面
    required_pages = [
        'index.html', 'products.html', 'services.html', 'about.html', 
        'portfolio.html', 'blog.html', 'contact.html', 'quote.html',
        'privacy-policy.html', 'terms-of-service.html', 'sitemap.html'
    ]
    
    # 可选页面（如果不存在会创建基本版本）
    optional_pages = {
        'articles.html': 'Articles - blackbackpack.co.uk',
        'business-backpacks.html': 'Business Backpacks - blackbackpack.co.uk',
        'outdoor-backpacks.html': 'Outdoor Backpacks - blackbackpack.co.uk',
        'school-backpacks.html': 'School Backpacks - blackbackpack.co.uk',
        'travel-backpacks.html': 'Travel Backpacks - blackbackpack.co.uk',
        'sports-backpacks.html': 'Sports Backpacks - blackbackpack.co.uk',
        'laptop-backpacks.html': 'Laptop Backpacks - blackbackpack.co.uk',
        'tactical-backpacks.html': 'Tactical Backpacks - blackbackpack.co.uk',
        'cookie-policy.html': 'Cookie Policy - blackbackpack.co.uk'
    }
    
    print("开始检查和修复链接...")
    
    # 统计信息
    files_processed = 0
    files_updated = 0
    missing_pages = []
    
    # 检查必需页面是否存在
    print("\n检查必需页面...")
    for page in required_pages:
        page_path = website_root / page
        if not page_path.exists():
            missing_pages.append(page)
            print(f"❌ 缺失必需页面: {page}")
        else:
            print(f"✅ 页面存在: {page}")
    
    # 检查可选页面，如果不存在则创建基本版本
    print("\n检查可选页面...")
    for page, title in optional_pages.items():
        page_path = website_root / page
        if not page_path.exists():
            print(f"⚠️  创建缺失页面: {page}")
            create_basic_page(page_path, title)
        else:
            print(f"✅ 页面存在: {page}")
    
    # 修复HTML文件中的链接
    print("\n修复HTML文件中的链接...")
    for file_path in website_root.rglob('*.html'):
        if file_path.name in ['update_contact_info.py', 'check_fix_links.py']:
            continue
            
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            original_content = content
            files_processed += 1
            
            # 应用链接修复
            for pattern, replacement in link_fixes.items():
                content = re.sub(pattern, replacement, content, flags=re.MULTILINE)
            
            # 如果内容有变化，写回文件
            if content != original_content:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                files_updated += 1
                print(f"已修复: {file_path.relative_to(website_root)}")
                
        except Exception as e:
            print(f"处理文件 {file_path} 时出错: {e}")
    
    print(f"\n修复完成!")
    print(f"处理文件数: {files_processed}")
    print(f"更新文件数: {files_updated}")
    
    if missing_pages:
        print(f"\n⚠️  仍缺失的必需页面: {', '.join(missing_pages)}")
        print("建议手动创建这些页面或检查链接是否正确。")

def create_basic_page(page_path, title):
    """
    创建基本页面模板
    """
    basic_template = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <meta name="description" content="{title} - Professional backpack manufacturing and custom solutions.">
    <link rel="stylesheet" href="css/style.css">
    <link rel="canonical" href="https://blackbackpack.co.uk/{page_path.name}">
</head>
<body>
    <!-- Header -->
    <header class="header">
        <nav class="navbar">
            <div class="nav-container">
                <div class="nav-logo">
                    <a href="index.html">
                        <img src="images/logo.svg" alt="blackbackpack.co.uk Logo">
                        <span>blackbackpack.co.uk</span>
                    </a>
                </div>
                <ul class="nav-menu">
                    <li class="nav-item">
                        <a href="products.html" class="nav-link">Products</a>
                    </li>
                    <li class="nav-item">
                        <a href="services.html" class="nav-link">Services</a>
                    </li>
                    <li class="nav-item">
                        <a href="about.html" class="nav-link">About</a>
                    </li>
                    <li class="nav-item">
                        <a href="portfolio.html" class="nav-link">Portfolio</a>
                    </li>
                    <li class="nav-item">
                        <a href="blog.html" class="nav-link">Blog</a>
                    </li>
                    <li class="nav-item">
                        <a href="contact.html" class="nav-link">Contact</a>
                    </li>
                </ul>
                <div class="nav-actions">
                    <a href="quote.html" class="btn btn-primary">Get Free Quote</a>
                </div>
            </div>
        </nav>
    </header>

    <!-- Main Content -->
    <main>
        <section class="hero-section">
            <div class="container">
                <h1>{title.replace(' - blackbackpack.co.uk', '')}</h1>
                <p>This page is under construction. Please check back soon or <a href="contact.html">contact us</a> for more information.</p>
                <div class="hero-actions">
                    <a href="products.html" class="btn btn-primary">View Products</a>
                    <a href="contact.html" class="btn btn-secondary">Contact Us</a>
                </div>
            </div>
        </section>
    </main>

    <!-- Footer -->
    <footer class="footer">
        <div class="container">
            <div class="footer-content">
                <div class="footer-section">
                    <h3>Contact Info</h3>
                    <p>Email: <a href="mailto:cco@junyuanbags.com">cco@junyuanbags.com</a></p>
                    <p>WhatsApp: <a href="https://wa.me/8617750020688">+86 17750020688</a></p>
                </div>
                <div class="footer-section">
                    <h3>Quick Links</h3>
                    <ul>
                        <li><a href="products.html">Products</a></li>
                        <li><a href="services.html">Services</a></li>
                        <li><a href="about.html">About Us</a></li>
                        <li><a href="contact.html">Contact</a></li>
                    </ul>
                </div>
            </div>
            <div class="footer-bottom">
                <p>&copy; 2024 blackbackpack.co.uk. All rights reserved.</p>
                <div class="footer-links">
                    <a href="privacy-policy.html">Privacy Policy</a>
                    <a href="terms-of-service.html">Terms of Service</a>
                    <a href="sitemap.html">Sitemap</a>
                </div>
            </div>
        </div>
    </footer>
</body>
</html>'''
    
    try:
        with open(page_path, 'w', encoding='utf-8') as f:
            f.write(basic_template)
        print(f"✅ 已创建: {page_path.name}")
    except Exception as e:
        print(f"❌ 创建 {page_path.name} 失败: {e}")

if __name__ == '__main__':
    check_and_fix_links()