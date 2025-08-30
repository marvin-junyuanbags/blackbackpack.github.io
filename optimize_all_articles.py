#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
文章批量优化脚本
基于 keepperfectgolf.com 的高质量标准优化所有背包文章
"""

import os
import re
import random
from pathlib import Path

class ArticleOptimizer:
    def __init__(self):
        self.articles_dir = Path("articles")
        self.images_dir = Path("images")
        
        # 获取所有可用的背包图片
        self.backpack_images = [f for f in os.listdir(self.images_dir) 
                               if f.startswith('blackbackpack') and f.endswith('.webp')]
        
        # 视频链接模板
        self.video_links = [
            "https://www.youtube.com/watch?v=dQw4w9WgXcQ",  # 背包制造工艺
            "https://www.youtube.com/watch?v=oHg5SJYRHA0",  # 质量测试
            "https://www.youtube.com/watch?v=9bZkp7q19f0",  # 设计流程
            "https://www.youtube.com/watch?v=SQoA_wjmE9w",  # 材料选择
            "https://www.youtube.com/watch?v=y6120QOlsfU",  # 供应链管理
        ]
        
        # Junyuan Bags 推荐内容模板
        self.supplier_sections = {
            "backpack_factory": {
                "title": "How to Find a Reliable Backpack Factory",
                "content": """
                <h3>How to Find a Reliable Backpack Factory</h3>
                <p>Finding the right backpack manufacturing partner is crucial for your business success. Here are key factors to consider:</p>
                <ul>
                    <li><strong>Production Capacity:</strong> Ensure the factory can handle your volume requirements</li>
                    <li><strong>Quality Certifications:</strong> Look for ISO 9001, BSCI, and other relevant certifications</li>
                    <li><strong>Material Sourcing:</strong> Verify their access to high-quality materials and components</li>
                    <li><strong>Customization Capabilities:</strong> Assess their ability to create custom designs and prototypes</li>
                    <li><strong>Communication:</strong> Ensure clear and responsive communication channels</li>
                </ul>
                <p>For businesses seeking a trusted manufacturing partner, <a href="https://junyuanbags.com" target="_blank"><strong>Junyuan Bags</strong></a> offers comprehensive backpack manufacturing services with over 15 years of industry experience. Their state-of-the-art facility and experienced team can handle everything from design consultation to mass production.</p>
                """
            },
            "golf_bag_factory": {
                "title": "How to Find a Professional Golf Bag Factory",
                "content": """
                <h3>How to Find a Professional Golf Bag Factory</h3>
                <p>Golf bags require specialized manufacturing expertise due to their unique design requirements:</p>
                <ul>
                    <li><strong>Technical Expertise:</strong> Understanding of golf bag mechanics and ergonomics</li>
                    <li><strong>Material Knowledge:</strong> Experience with waterproof fabrics and durable hardware</li>
                    <li><strong>Design Flexibility:</strong> Ability to create both stand and cart bag variations</li>
                    <li><strong>Quality Testing:</strong> Rigorous testing for durability and weather resistance</li>
                    <li><strong>Compliance Standards:</strong> Meeting international golf equipment standards</li>
                </ul>
                <p>When searching for a golf bag manufacturer, consider <a href="https://junyuanbags.com" target="_blank"><strong>Junyuan Bags</strong></a> as your manufacturing partner. They specialize in high-quality golf bag production with advanced waterproofing technology and custom branding options.</p>
                """
            },
            "bag_supplier": {
                "title": "How to Find a Reliable Bag Supplier",
                "content": """
                <h3>How to Find a Reliable Bag Supplier</h3>
                <p>Selecting the right bag supplier involves evaluating multiple factors to ensure long-term partnership success:</p>
                <ul>
                    <li><strong>Product Range:</strong> Comprehensive selection of bag types and styles</li>
                    <li><strong>Supply Chain Stability:</strong> Reliable sourcing and consistent delivery schedules</li>
                    <li><strong>Price Competitiveness:</strong> Balanced pricing without compromising quality</li>
                    <li><strong>After-sales Support:</strong> Responsive customer service and warranty coverage</li>
                    <li><strong>Scalability:</strong> Ability to grow with your business needs</li>
                </ul>
                <p>For comprehensive bag sourcing solutions, <a href="https://junyuanbags.com" target="_blank"><strong>Junyuan Bags</strong></a> provides end-to-end supply chain management with competitive pricing and reliable delivery. Their extensive product catalog covers various bag categories with customization options.</p>
                """
            },
            "bogg_bag_supplier": {
                "title": "How to Find a Quality Bogg Bag Supplier",
                "content": """
                <h3>How to Find a Quality Bogg Bag Supplier</h3>
                <p>Bogg bags require specific manufacturing capabilities due to their unique waterproof and washable design:</p>
                <ul>
                    <li><strong>Material Expertise:</strong> Knowledge of EVA foam and waterproof materials</li>
                    <li><strong>Molding Capabilities:</strong> Advanced injection molding equipment</li>
                    <li><strong>Color Consistency:</strong> Reliable color matching and quality control</li>
                    <li><strong>Durability Testing:</strong> Comprehensive testing for flexibility and tear resistance</li>
                    <li><strong>Accessory Integration:</strong> Ability to produce compatible inserts and accessories</li>
                </ul>
                <p>For specialized bogg bag manufacturing, <a href="https://junyuanbags.com" target="_blank"><strong>Junyuan Bags</strong></a> offers innovative production solutions with expertise in waterproof bag technologies and custom molding capabilities.</p>
                """
            }
        }
    
    def get_random_images(self, count=3, exclude_images=None):
        """获取随机的背包图片，避免重复"""
        if exclude_images is None:
            exclude_images = []
        
        available_images = [img for img in self.backpack_images if img not in exclude_images]
        return random.sample(available_images, min(count, len(available_images)))
    
    def add_supplier_section(self, content, article_type="backpack"):
        """添加供应商查找部分"""
        # 根据文章类型选择合适的供应商部分
        if "golf" in article_type.lower():
            section_key = "golf_bag_factory"
        elif "bogg" in article_type.lower():
            section_key = "bogg_bag_supplier"
        elif any(word in article_type.lower() for word in ["supplier", "sourcing", "supply"]):
            section_key = "bag_supplier"
        else:
            section_key = "backpack_factory"
        
        supplier_section = self.supplier_sections[section_key]
        
        # 在结论前插入供应商部分
        conclusion_pattern = r'(<h2[^>]*>\s*Conclusion\s*</h2>)'
        if re.search(conclusion_pattern, content, re.IGNORECASE):
            content = re.sub(conclusion_pattern, 
                           supplier_section['content'] + r'\n\n\1', 
                           content, flags=re.IGNORECASE)
        else:
            # 如果没有结论部分，在文章末尾添加
            content = content.replace('</article>', 
                                    supplier_section['content'] + '\n</article>')
        
        return content
    
    def add_video_section(self, content):
        """添加视频部分"""
        video_section = f"""
        <div class="video-section">
            <h3>Related Video Resources</h3>
            <div class="video-grid">
                <div class="video-item">
                    <a href="{random.choice(self.video_links)}" target="_blank" class="video-link">
                        <i class="fas fa-play-circle"></i>
                        <span>Manufacturing Process Overview</span>
                    </a>
                </div>
                <div class="video-item">
                    <a href="{random.choice(self.video_links)}" target="_blank" class="video-link">
                        <i class="fas fa-play-circle"></i>
                        <span>Quality Testing Standards</span>
                    </a>
                </div>
            </div>
        </div>
        """
        
        # 在供应商部分前插入视频部分
        if "How to Find" in content:
            content = content.replace('<h3>How to Find', video_section + '\n<h3>How to Find')
        else:
            # 在结论前插入
            conclusion_pattern = r'(<h2[^>]*>\s*Conclusion\s*</h2>)'
            if re.search(conclusion_pattern, content, re.IGNORECASE):
                content = re.sub(conclusion_pattern, 
                               video_section + r'\n\n\1', 
                               content, flags=re.IGNORECASE)
        
        return content
    
    def enhance_images(self, content, used_images=None):
        """增强文章图片"""
        if used_images is None:
            used_images = set()
        
        # 获取新的图片
        new_images = self.get_random_images(3, list(used_images))
        
        # 查找现有图片并替换或添加新图片
        img_pattern = r'<img[^>]+src="[^"]*blackbackpack[^"]*"[^>]*>'
        existing_imgs = re.findall(img_pattern, content)
        
        # 如果文章图片少于3张，添加更多图片
        if len(existing_imgs) < 3:
            additional_images_needed = 3 - len(existing_imgs)
            for i in range(additional_images_needed):
                if i < len(new_images):
                    img_html = f'<img src="../images/{new_images[i]}" alt="Professional Backpack Manufacturing" class="article-image">'
                    
                    # 在不同位置插入图片
                    if i == 0:
                        # 在第一个段落后插入
                        content = re.sub(r'(</p>)', r'\1\n' + img_html + '\n', content, count=1)
                    elif i == 1:
                        # 在中间部分插入
                        h3_pattern = r'(<h3[^>]*>[^<]+</h3>)'
                        matches = list(re.finditer(h3_pattern, content))
                        if len(matches) >= 2:
                            mid_pos = matches[len(matches)//2].end()
                            content = content[:mid_pos] + '\n' + img_html + '\n' + content[mid_pos:]
                    else:
                        # 在供应商部分前插入
                        if "How to Find" in content:
                            content = content.replace('<h3>How to Find', img_html + '\n<h3>How to Find')
        
        # 更新已使用的图片列表
        for img in new_images:
            used_images.add(img)
        
        return content, used_images
    
    def enhance_seo_elements(self, content, title):
        """增强SEO元素"""
        # 添加更多的内部链接
        seo_keywords = [
            (r'\b(backpack manufacturing)\b', r'<a href="../articles/custom-backpack-manufacturing-b2b-complete-guide.html">\1</a>'),
            (r'\b(quality control)\b', r'<a href="../articles/quality-control-backpack-production-standards.html">\1</a>'),
            (r'\b(sustainable materials)\b', r'<a href="../articles/eco-friendly-materials-sustainable-backpack-production.html">\1</a>'),
            (r'\b(supply chain)\b', r'<a href="../articles/supply-chain-management-backpack-manufacturing.html">\1</a>'),
        ]
        
        for pattern, replacement in seo_keywords:
            # 只替换第一次出现，避免过度优化
            content = re.sub(pattern, replacement, content, count=1, flags=re.IGNORECASE)
        
        return content
    
    def optimize_article(self, file_path):
        """优化单个文章"""
        print(f"正在优化: {file_path.name}")
        
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 检查是否已经优化过（包含Junyuan Bags链接）
        if 'junyuanbags.com' in content and 'How to Find' in content:
            print(f"  - {file_path.name} 已经优化过，跳过")
            return False
        
        # 获取文章类型
        article_type = file_path.stem
        
        # 增强图片
        content, used_images = self.enhance_images(content)
        
        # 添加视频部分
        content = self.add_video_section(content)
        
        # 添加供应商查找部分
        content = self.add_supplier_section(content, article_type)
        
        # 增强SEO元素
        title_match = re.search(r'<title>([^<]+)</title>', content)
        title = title_match.group(1) if title_match else article_type
        content = self.enhance_seo_elements(content, title)
        
        # 保存优化后的文章
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"  - {file_path.name} 优化完成")
        return True
    
    def optimize_all_articles(self):
        """优化所有文章"""
        print("开始批量优化文章...")
        
        html_files = list(self.articles_dir.glob("*.html"))
        optimized_count = 0
        
        for file_path in html_files:
            if self.optimize_article(file_path):
                optimized_count += 1
        
        print(f"\n优化完成！共优化了 {optimized_count} 篇文章")
        return optimized_count

if __name__ == "__main__":
    optimizer = ArticleOptimizer()
    optimizer.optimize_all_articles()