import os
import re

def remove_address(file_path):
    """移除HTML文件中的地址信息"""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        
        original_content = content
        
        # 移除带图标的地址格式
        content = re.sub(r'<p><i class="fas fa-map-marker-alt"></i> 华创园, 广州市天河区, 中国</p>', '', content)
        
        # 移除span标签中的地址格式
        content = re.sub(r'<span>华创园, 广州市天河区, 中国</span>', '', content)
        
        # 移除其他可能的地址格式
        content = re.sub(r'华创园, 广州市天河区, 中国', '', content)
        
        # 清理可能留下的空行
        content = re.sub(r'\n\s*\n', '\n', content)
        
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
            
            if remove_address(file_path):
                modified_files += 1
                print(f"已移除地址: {filename}")
    
    print(f"\n处理完成！")
    print(f"总文件数: {total_files}")
    print(f"修改文件数: {modified_files}")

if __name__ == "__main__":
    main()