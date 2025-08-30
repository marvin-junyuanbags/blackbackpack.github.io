import os
import re

def fix_whatsapp_format(file_path):
    """修复HTML文件中WhatsApp格式的转义字符问题"""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        
        original_content = content
        
        # 修复 What\'s App 为 What's App
        content = re.sub(r"What\\'s App", "What's App", content)
        
        # 检查是否有修改
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
    articles_dir = "articles"
    
    if not os.path.exists(articles_dir):
        print(f"目录 {articles_dir} 不存在")
        return
    
    total_files = 0
    modified_files = 0
    
    # 遍历articles目录下的所有HTML文件
    for filename in os.listdir(articles_dir):
        if filename.endswith('.html'):
            file_path = os.path.join(articles_dir, filename)
            total_files += 1
            
            if fix_whatsapp_format(file_path):
                modified_files += 1
                print(f"已修复: {filename}")
    
    print(f"\n处理完成！")
    print(f"总文件数: {total_files}")
    print(f"修改文件数: {modified_files}")

if __name__ == "__main__":
    main()