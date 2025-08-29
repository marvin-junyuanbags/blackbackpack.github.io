#!/usr/bin/env python3
"""
Update blog.html with all articles from the articles directory
"""

import os
import re
from datetime import datetime, timedelta
import random

def extract_article_info(file_path):
    """Extract article information from HTML file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Extract title from <title> tag or <h1>
        title_match = re.search(r'<title>([^<]+)</title>', content)
        if title_match:
            title = title_match.group(1).replace(' - Black Backpack', '').strip()
        else:
            h1_match = re.search(r'<h1[^>]*>([^<]+)</h1>', content)
            title = h1_match.group(1).strip() if h1_match else os.path.basename(file_path).replace('.html', '').replace('-', ' ').title()
        
        # Extract meta description
        desc_match = re.search(r'<meta name="description" content="([^"]+)"', content)
        description = desc_match.group(1) if desc_match else f"Learn about {title.lower()} in our comprehensive guide..."
        
        # Extract image from og:image or first img tag
        img_match = re.search(r'<meta property="og:image" content="[^"]*images/([^"]+)"', content)
        if img_match:
            image = img_match.group(1)
        else:
            # Look for first img tag
            img_tag_match = re.search(r'<img[^>]+src="[^"]*images/([^"]+)"', content)
            image = img_tag_match.group(1) if img_tag_match else 'blackbackpack (1).webp'
        
        return {
            'title': title,
            'description': description[:150] + '...' if len(description) > 150 else description,
            'image': image,
            'filename': os.path.basename(file_path)
        }
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return None

def categorize_article(filename, title):
    """Categorize article based on filename and title"""
    filename_lower = filename.lower()
    title_lower = title.lower()
    
    if any(word in filename_lower or word in title_lower for word in ['sustainable', 'eco', 'green', 'environment']):
        return 'sustainability'
    elif any(word in filename_lower or word in title_lower for word in ['technology', 'automation', 'digital', 'innovation', 'tech']):
        return 'technology'
    elif any(word in filename_lower or word in title_lower for word in ['design', 'trends', 'style', 'aesthetic']):
        return 'design'
    elif any(word in filename_lower or word in title_lower for word in ['material', 'quality', 'durability', 'fabric']):
        return 'materials'
    elif any(word in filename_lower or word in title_lower for word in ['business', 'marketing', 'brand', 'strategy', 'b2b']):
        return 'business'
    elif any(word in filename_lower or word in title_lower for word in ['guide', 'how-to', 'tutorial', 'step']):
        return 'guides'
    else:
        return 'manufacturing'

def get_category_display_name(category):
    """Get display name for category"""
    category_map = {
        'manufacturing': 'Manufacturing',
        'design': 'Design & Innovation',
        'materials': 'Materials & Quality',
        'business': 'Business',
        'trends': 'Industry Trends',
        'sustainability': 'Sustainability',
        'technology': 'Technology',
        'guides': 'How-to Guides'
    }
    return category_map.get(category, 'Manufacturing')

def generate_article_card(article_info, date_str, read_time):
    """Generate HTML for article card"""
    category = categorize_article(article_info['filename'], article_info['title'])
    category_display = get_category_display_name(category)
    
    return f'''                <article class="article-card" data-category="{category}" data-date="{date_str}">
                    <div class="article-image">
                        <img src="images/{article_info['image']}" alt="{article_info['title']}">
                        <div class="article-category">{category_display}</div>
                    </div>
                    <div class="article-content">
                        <h3><a href="articles/{article_info['filename']}">{article_info['title']}</a></h3>
                        <p>{article_info['description']}</p>
                        <div class="article-meta">
                            <span class="article-date">{datetime.strptime(date_str, '%Y-%m-%d').strftime('%b %d, %Y')}</span>
                            <span class="article-read-time">{read_time} min read</span>
                        </div>
                    </div>
                </article>'''

def main():
    articles_dir = 'articles'
    blog_file = 'blog.html'
    
    if not os.path.exists(articles_dir):
        print(f"Articles directory '{articles_dir}' not found!")
        return
    
    # Get all HTML files from articles directory
    article_files = [f for f in os.listdir(articles_dir) if f.endswith('.html')]
    article_files.sort()  # Sort alphabetically
    
    print(f"Found {len(article_files)} articles")
    
    # Extract article information
    articles_data = []
    start_date = datetime(2024, 12, 15)
    
    for i, filename in enumerate(article_files):
        file_path = os.path.join(articles_dir, filename)
        article_info = extract_article_info(file_path)
        
        if article_info:
            # Generate date (going backwards from start_date)
            article_date = start_date - timedelta(days=i)
            read_time = random.randint(7, 15)  # Random read time between 7-15 minutes
            
            articles_data.append({
                'info': article_info,
                'date': article_date.strftime('%Y-%m-%d'),
                'read_time': read_time
            })
    
    # Generate article cards HTML
    article_cards_html = '\n\n'.join([
        generate_article_card(article['info'], article['date'], article['read_time'])
        for article in articles_data
    ])
    
    # Read current blog.html
    with open(blog_file, 'r', encoding='utf-8') as f:
        blog_content = f.read()
    
    # Update article count in the content
    total_articles = len(articles_data)
    blog_content = re.sub(r'collection of \d+ articles', f'collection of {total_articles} articles', blog_content)
    blog_content = re.sub(r'All Articles \(\d+\)', f'All Articles ({total_articles})', blog_content)
    blog_content = re.sub(r'of \d+ articles', f'of {total_articles} articles', blog_content)
    
    # Replace the articles grid content
    start_marker = '<div class="articles-grid" id="articles-grid">'
    end_marker = '</div>\n\n            <!-- Pagination -->'
    
    start_pos = blog_content.find(start_marker)
    end_pos = blog_content.find(end_marker)
    
    if start_pos != -1 and end_pos != -1:
        new_content = (
            blog_content[:start_pos + len(start_marker)] +
            '\n' + article_cards_html + '\n\n            ' +
            blog_content[end_pos:]
        )
        
        # Update pagination info
        articles_per_page = 12
        total_pages = (total_articles + articles_per_page - 1) // articles_per_page
        
        # Update pagination numbers
        pagination_numbers = '\n'.join([
            f'                        <button class="pagination-number{" active" if i == 1 else ""}" data-page="{i}">{i}</button>'
            for i in range(1, min(total_pages + 1, 11))  # Show max 10 page numbers
        ])
        
        new_content = re.sub(
            r'<div class="pagination-numbers" id="pagination-numbers">.*?</div>',
            f'<div class="pagination-numbers" id="pagination-numbers">\n{pagination_numbers}\n                    </div>',
            new_content,
            flags=re.DOTALL
        )
        
        # Update total pages display
        new_content = re.sub(r'<span id="total-pages">\d+</span>', f'<span id="total-pages">{total_pages}</span>', new_content)
        
        # Write updated content
        with open(blog_file, 'w', encoding='utf-8') as f:
            f.write(new_content)
        
        print(f"Successfully updated {blog_file} with {total_articles} articles")
        print(f"Total pages: {total_pages}")
    else:
        print("Could not find articles grid section in blog.html")

if __name__ == '__main__':
    main()