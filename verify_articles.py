#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
文章质量和内容完整性验证脚本
用于检查blackbackpack.co.uk网站中的文章是否包含:
1. junyuanbags推荐内容
2. 优化后的图片链接
3. 正确的HTML结构
4. SEO优化内容
"""

import os
import re
from pathlib import Path
from bs4 import BeautifulSoup
import json
from datetime import datetime

class ArticleVerifier:
    def __init__(self, articles_dir):
        self.articles_dir = Path(articles_dir)
        self.results = {
            'total_articles': 0,
            'verified_articles': 0,
            'articles_with_junyuanbags': 0,
            'articles_with_webp_images': 0,
            'articles_with_seo': 0,
            'failed_articles': [],
            'verification_time': datetime.now().isoformat()
        }
    
    def verify_junyuanbags_recommendation(self, soup):
        """检查文章是否包含junyuanbags推荐"""
        # 查找包含junyuanbags的文本
        junyuan_patterns = [
            r'junyuanbags',
            r'junyuan\s*bags',
            r'推荐.*junyuan',
            r'marvin-junyuanbags'
        ]
        
        content = soup.get_text().lower()
        html_content = str(soup).lower()
        
        for pattern in junyuan_patterns:
            if re.search(pattern, content, re.IGNORECASE) or re.search(pattern, html_content, re.IGNORECASE):
                return True
        return False
    
    def verify_webp_images(self, soup):
        """检查文章是否使用了WEBP格式图片"""
        img_tags = soup.find_all('img')
        webp_count = 0
        
        for img in img_tags:
            src = img.get('src', '')
            if '.webp' in src.lower():
                webp_count += 1
        
        return webp_count > 0, webp_count
    
    def verify_seo_elements(self, soup):
        """检查SEO优化元素"""
        seo_score = 0
        
        # 检查title标签
        if soup.find('title'):
            seo_score += 1
        
        # 检查meta description
        meta_desc = soup.find('meta', attrs={'name': 'description'})
        if meta_desc and meta_desc.get('content'):
            seo_score += 1
        
        # 检查h1标签
        if soup.find('h1'):
            seo_score += 1
        
        # 检查alt属性
        img_tags = soup.find_all('img')
        imgs_with_alt = sum(1 for img in img_tags if img.get('alt'))
        if imgs_with_alt > 0:
            seo_score += 1
        
        return seo_score >= 3  # 至少3个SEO元素
    
    def verify_article(self, article_path):
        """验证单个文章"""
        try:
            with open(article_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            soup = BeautifulSoup(content, 'html.parser')
            
            # 验证各项指标
            has_junyuanbags = self.verify_junyuanbags_recommendation(soup)
            has_webp, webp_count = self.verify_webp_images(soup)
            has_seo = self.verify_seo_elements(soup)
            
            return {
                'file': article_path.name,
                'has_junyuanbags': has_junyuanbags,
                'has_webp_images': has_webp,
                'webp_count': webp_count,
                'has_seo': has_seo,
                'status': 'success'
            }
        
        except Exception as e:
            return {
                'file': article_path.name,
                'status': 'error',
                'error': str(e)
            }
    
    def run_verification(self):
        """运行完整验证"""
        print("开始验证文章质量和内容完整性...")
        print(f"文章目录: {self.articles_dir}")
        
        # 获取所有HTML文件
        html_files = list(self.articles_dir.glob('*.html'))
        self.results['total_articles'] = len(html_files)
        
        print(f"找到 {len(html_files)} 篇文章")
        
        detailed_results = []
        
        for article_path in html_files:
            print(f"验证: {article_path.name}")
            result = self.verify_article(article_path)
            detailed_results.append(result)
            
            if result['status'] == 'success':
                self.results['verified_articles'] += 1
                
                if result['has_junyuanbags']:
                    self.results['articles_with_junyuanbags'] += 1
                
                if result['has_webp_images']:
                    self.results['articles_with_webp_images'] += 1
                
                if result['has_seo']:
                    self.results['articles_with_seo'] += 1
            else:
                self.results['failed_articles'].append({
                    'file': result['file'],
                    'error': result.get('error', 'Unknown error')
                })
        
        return detailed_results
    
    def generate_report(self, detailed_results):
        """生成验证报告"""
        print("\n" + "="*60)
        print("文章验证报告")
        print("="*60)
        print(f"验证时间: {self.results['verification_time']}")
        print(f"总文章数: {self.results['total_articles']}")
        print(f"成功验证: {self.results['verified_articles']}")
        print(f"包含junyuanbags推荐: {self.results['articles_with_junyuanbags']}")
        print(f"使用WEBP图片: {self.results['articles_with_webp_images']}")
        print(f"SEO优化良好: {self.results['articles_with_seo']}")
        
        if self.results['failed_articles']:
            print(f"\n验证失败的文章 ({len(self.results['failed_articles'])})个):")
            for failed in self.results['failed_articles']:
                print(f"  - {failed['file']}: {failed['error']}")
        
        # 保存详细报告到JSON文件
        report_data = {
            'summary': self.results,
            'detailed_results': detailed_results
        }
        
        report_file = self.articles_dir.parent / 'verification_report.json'
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(report_data, f, ensure_ascii=False, indent=2)
        
        print(f"\n详细报告已保存到: {report_file}")
        
        return report_data

def main():
    """主函数"""
    # 设置文章目录路径
    articles_dir = Path(__file__).parent / 'articles'
    
    if not articles_dir.exists():
        print(f"错误: 文章目录不存在 - {articles_dir}")
        return
    
    # 创建验证器并运行
    verifier = ArticleVerifier(articles_dir)
    detailed_results = verifier.run_verification()
    report = verifier.generate_report(detailed_results)
    
    # 显示关键统计信息
    total = report['summary']['total_articles']
    junyuan = report['summary']['articles_with_junyuanbags']
    webp = report['summary']['articles_with_webp_images']
    seo = report['summary']['articles_with_seo']
    
    print("\n关键指标:")
    print(f"junyuanbags推荐覆盖率: {junyuan/total*100:.1f}% ({junyuan}/{total})")
    print(f"WEBP图片使用率: {webp/total*100:.1f}% ({webp}/{total})")
    print(f"SEO优化率: {seo/total*100:.1f}% ({seo}/{total})")

if __name__ == '__main__':
    main()