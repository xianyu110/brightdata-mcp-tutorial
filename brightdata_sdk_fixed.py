#!/usr/bin/env python3
"""
Bright Data SDK 修复版演示
解决了解析错误和其他问题
"""

from brightdata import bdclient
import json
from datetime import datetime
import time

# API令牌
API_TOKEN = "your_api_token_here"

def safe_parse(client, results):
    """安全的解析函数，处理各种数据格式"""
    try:
        # 如果results已经是字符串，直接返回
        if isinstance(results, str):
            return {
                "type": "raw_text",
                "content": results[:1000],  # 只显示前1000字符
                "length": len(results)
            }
        
        # 如果是列表，处理每个元素
        if isinstance(results, list):
            parsed_list = []
            for item in results:
                if isinstance(item, str):
                    parsed_list.append(item[:500])
                else:
                    parsed_list.append(str(item)[:500])
            return {
                "type": "list",
                "count": len(results),
                "items": parsed_list[:5]  # 只显示前5个
            }
        
        # 尝试使用客户端的parse_content
        return client.parse_content(results)
        
    except Exception as e:
        # 如果解析失败，返回原始数据的字符串表示
        return {
            "type": "parse_error",
            "error": str(e),
            "raw_preview": str(results)[:500]
        }

def search_google(query):
    """执行Google搜索并安全处理结果"""
    print(f"\n{'='*60}")
    print(f"搜索: {query}")
    print(f"{'='*60}")
    
    try:
        client = bdclient(api_token=API_TOKEN)
        
        # 执行搜索
        print("正在搜索...")
        results = client.search(query=query)
        
        # 显示原始结果类型
        print(f"结果类型: {type(results)}")
        
        # 安全解析
        parsed = safe_parse(client, results)
        
        # 显示解析结果
        print("\n解析结果:")
        print(json.dumps(parsed, indent=2, ensure_ascii=False)[:1000])
        
        return parsed
        
    except Exception as e:
        print(f"错误: {e}")
        return None

def batch_search_fixed(queries):
    """修复版的批量搜索"""
    print(f"\n{'='*60}")
    print(f"批量搜索 {len(queries)} 个查询")
    print(f"{'='*60}")
    
    client = bdclient(api_token=API_TOKEN)
    all_results = []
    
    for i, query in enumerate(queries, 1):
        print(f"\n[{i}/{len(queries)}] 搜索: {query}")
        
        try:
            # 单独搜索每个查询
            result = client.search(query=query)
            
            # 安全解析
            parsed = safe_parse(client, result)
            
            all_results.append({
                "query": query,
                "success": True,
                "data": parsed
            })
            
            print(f"✅ 成功")
            
        except Exception as e:
            print(f"❌ 失败: {e}")
            all_results.append({
                "query": query,
                "success": False,
                "error": str(e)
            })
        
        # 避免请求过快
        if i < len(queries):
            time.sleep(2)
    
    return all_results

def extract_text_from_html(html_content):
    """从HTML中提取文本内容"""
    try:
        from bs4 import BeautifulSoup
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # 提取所有文本
        text = soup.get_text(separator='\n', strip=True)
        
        # 查找可能的搜索结果
        results = []
        
        # 尝试找到搜索结果的常见模式
        for tag in soup.find_all(['h3', 'a', 'div']):
            text_content = tag.get_text(strip=True)
            if text_content and len(text_content) > 10:
                href = tag.get('href') if tag.name == 'a' else None
                results.append({
                    "text": text_content[:200],
                    "url": href
                })
        
        return {
            "total_text_length": len(text),
            "potential_results": results[:10],  # 前10个可能的结果
            "preview": text[:500]
        }
        
    except Exception as e:
        return {"error": f"HTML解析失败: {e}"}

def demo_working_search():
    """演示可工作的搜索功能"""
    print("\nBright Data SDK - 工作演示")
    print("="*60)
    
    # 1. 单个搜索
    query = "Python programming"
    result = search_google(query)
    
    # 2. 尝试从HTML提取信息
    if result and result.get("type") == "raw_text":
        print("\n尝试解析HTML内容...")
        extracted = extract_text_from_html(result.get("content", ""))
        print(json.dumps(extracted, indent=2, ensure_ascii=False)[:1000])
    
    # 3. 批量搜索
    queries = [
        "machine learning",
        "data science",
        "artificial intelligence"
    ]
    
    batch_results = batch_search_fixed(queries)
    
    # 4. 保存结果
    output_file = f"search_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump({
            "single_search": result,
            "batch_search": batch_results,
            "timestamp": datetime.now().isoformat()
        }, f, indent=2, ensure_ascii=False)
    
    print(f"\n结果已保存到: {output_file}")

def test_basic_functionality():
    """测试基本功能"""
    print("\n测试基本功能")
    print("="*60)
    
    try:
        client = bdclient(api_token=API_TOKEN)
        
        # 测试zones
        print("\n1. 列出zones:")
        zones = client.list_zones()
        for zone in zones:
            print(f"   - {zone}")
        
        # 测试简单搜索
        print("\n2. 测试搜索功能:")
        result = client.search("test")
        print(f"   搜索返回类型: {type(result)}")
        print(f"   数据大小: {len(str(result))} 字符")
        
        # 测试下载功能
        print("\n3. 测试下载功能:")
        try:
            client.download_content(result, filename="test_download.txt")
            print("   ✅ 下载成功")
        except Exception as e:
            print(f"   ❌ 下载失败: {e}")
            
    except Exception as e:
        print(f"错误: {e}")

if __name__ == "__main__":
    # 运行测试
    test_basic_functionality()
    
    # 运行工作演示
    demo_working_search()