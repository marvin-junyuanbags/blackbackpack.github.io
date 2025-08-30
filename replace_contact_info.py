import os
import re

def replace_contact_info(file_path):
    """替换HTML文件中的联系方式信息"""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        
        original_content = content
        
        # 替换邮箱地址 - 各种格式
        # 1. 带图标的格式: <i class="fas fa-envelope"></i> info@blackbackpack.co.uk
        content = re.sub(
            r'(<i class="fas fa-envelope"></i>\s*)info@blackbackpack\.co\.uk',
            r'\1cco@junyuanbags.com',
            content
        )
        
        # 2. 简单格式: Email: info@blackbackpack.co.uk
        content = re.sub(
            r'(Email:\s*)info@blackbackpack\.co\.uk',
            r'\1cco@junyuanbags.com',
            content
        )
        
        # 3. 表情符号格式: 📧 info@blackbackpack.co.uk
        content = re.sub(
            r'(📧\s*)info@blackbackpack\.co\.uk',
            r'\1cco@junyuanbags.com',
            content
        )
        
        # 4. span标签格式: <span>info@blackbackpack.co.uk</span>
        content = re.sub(
            r'(<span>)info@blackbackpack\.co\.uk(</span>)',
            r'\1cco@junyuanbags.com\2',
            content
        )
        
        # 5. 带图片的格式处理 - 先替换邮箱
        content = re.sub(
            r'info@blackbackpack\.co\.uk',
            'cco@junyuanbags.com',
            content
        )
        
        # 替换电话号码 - 各种格式
        # 1. 带图标的格式: <i class="fas fa-phone"></i> +44 20 1234 5678
        content = re.sub(
            r'(<i class="fas fa-phone"></i>\s*)\+44 20 1234 5678',
            r'\1+86 17750020688',
            content
        )
        
        # 2. 简单格式: Phone: +44 20 1234 5678
        content = re.sub(
            r'(Phone:\s*)\+44 20 1234 5678',
            r'What\'s App: +86 17750020688',
            content
        )
        
        # 3. span标签格式: <span>+44 20 1234 5678</span>
        content = re.sub(
            r'(<span>)\+44 20 1234 5678(</span>)',
            r'\1+86 17750020688\2',
            content
        )
        
        # 4. 其他可能的格式
        content = re.sub(
            r'\+44 20 1234 5678',
            '+86 17750020688',
            content
        )
        
        # 如果内容有变化，写回文件
        if content != original_content:
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(content)
            return True
        return False
        
    except Exception as e:
        print(f"处理文件 {file_path} 时出错: {e}")
        return False

def main():
    """主函数：处理articles目录下的所有HTML文件"""
    articles_dir = "C:\\Users\\A1775\\blackbackpack.co.uk\\articles"
    
    if not os.path.exists(articles_dir):
        print(f"目录不存在: {articles_dir}")
        return
    
    html_files = [f for f in os.listdir(articles_dir) if f.endswith('.html')]
    
    if not html_files:
        print("未找到HTML文件")
        return
    
    print(f"找到 {len(html_files)} 个HTML文件")
    
    modified_count = 0
    
    for filename in html_files:
        file_path = os.path.join(articles_dir, filename)
        if replace_contact_info(file_path):
            modified_count += 1
            print(f"已修改: {filename}")
    
    print(f"\n处理完成！")
    print(f"总文件数: {len(html_files)}")
    print(f"修改文件数: {modified_count}")

if __name__ == "__main__":
    main()