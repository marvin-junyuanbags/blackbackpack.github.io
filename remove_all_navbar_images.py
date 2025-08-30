import os
import re

def remove_navbar_images(file_path):
    """移除HTML文件中所有导航栏的背包图片"""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        
        original_content = content
        
        # 移除所有可能的导航栏图片格式
        patterns = [
            # nav__logo-img 类
            r'<img[^>]*class="nav__logo-img"[^>]*src="../images/blackbackpack[^>]*>',
            # logo 类
            r'<img[^>]*class="logo"[^>]*src="../images/blackbackpack[^>]*>',
            # 其他可能的logo相关类
            r'<img[^>]*class="[^"]*logo[^"]*"[^>]*src="../images/blackbackpack[^>]*>',
            # 通用导航栏图片（在nav标签内的图片）
            r'<nav[^>]*>.*?<img[^>]*src="../images/blackbackpack[^>]*>.*?</nav>',
            # 带有logo alt文本的图片
            r'<img[^>]*alt="[^"]*[Ll]ogo[^"]*"[^>]*src="../images/blackbackpack[^>]*>',
            # 在header中的logo图片
            r'<header[^>]*>.*?<img[^>]*src="../images/blackbackpack[^>]*>.*?</header>',
        ]
        
        for pattern in patterns:
            content = re.sub(pattern, '', content, flags=re.DOTALL | re.IGNORECASE)
        
        # 清理可能留下的空标签
        content = re.sub(r'<a[^>]*>\s*</a>', '', content)
        content = re.sub(r'<div[^>]*class="[^"]*logo[^"]*"[^>]*>\s*</div>', '', content)
        
        if content != original_content:
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(content)
            return True
        return False
        
    except Exception as e:
        print(f"处理文件 {file_path} 时出错: {e}")
        return False

def main():
    articles_dir = "C:\\Users\\A1775\\blackbackpack.co.uk\\articles"
    
    if not os.path.exists(articles_dir):
        print(f"目录不存在: {articles_dir}")
        return
    
    modified_count = 0
    total_count = 0
    
    for filename in os.listdir(articles_dir):
        if filename.endswith('.html'):
            file_path = os.path.join(articles_dir, filename)
            total_count += 1
            
            if remove_navbar_images(file_path):
                modified_count += 1
                print(f"已修改: {filename}")
            else:
                print(f"跳过: {filename} (未找到导航栏图片)")
    
    print(f"\n处理完成!")
    print(f"总文件数: {total_count}")
    print(f"修改文件数: {modified_count}")
    print(f"跳过文件数: {total_count - modified_count}")

if __name__ == "__main__":
    main()