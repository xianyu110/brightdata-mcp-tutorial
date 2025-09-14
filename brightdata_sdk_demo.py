#!/usr/bin/env python3
"""
Bright Data SDK 实战演示
使用官方Python SDK进行网页搜索和抓取
"""

from brightdata import bdclient
import json
from datetime import datetime
import os

# 设置API令牌
API_TOKEN = "your_api_token_here"

def demo_basic_search():
    """基础搜索演示"""
    print("="*80)
    print("Bright Data SDK - 搜索演示")
    print("="*80)
    
    try:
        # 初始化客户端
        client = bdclient(api_token=API_TOKEN)
        print(f"[{datetime.now()}] 客户端初始化成功")
        
        # 执行搜索
        query = "Python web scraping tutorial 2024"
        print(f"\n[搜索] 关键词: {query}")
        
        results = client.search(
            query=query,
            search_engine="google",
            country="us",
            data_format="markdown"
        )
        
        # 解析并显示结果
        print("\n[原始响应]")
        print(json.dumps(results, indent=2, ensure_ascii=False)[:1000] + "...")
        
        # 使用SDK的解析功能
        parsed_content = client.parse_content(results)
        print("\n[解析后的内容]")
        print(parsed_content[:1000] + "...")
        
    except Exception as e:
        print(f"\n[错误] {type(e).__name__}: {e}")

def demo_scrape_website():
    """网页抓取演示"""
    print("\n" + "="*80)
    print("Bright Data SDK - 网页抓取演示")
    print("="*80)
    
    try:
        client = bdclient(api_token=API_TOKEN)
        
        # 抓取单个URL
        url = "https://docs.brightdata.com/api-reference/SDK"
        print(f"\n[抓取] URL: {url}")
        
        results = client.scrape(
            url=url,
            country="us",
            data_format="markdown"
        )
        
        print("\n[抓取结果]")
        print(f"状态: {'成功' if results else '失败'}")
        
        if results:
            # 保存结果到文件
            filename = "scrape_results.json"
            client.download_content(results, filename=filename)
            print(f"结果已保存到: {filename}")
            
    except Exception as e:
        print(f"\n[错误] {type(e).__name__}: {e}")

def demo_batch_operations():
    """批量操作演示"""
    print("\n" + "="*80)
    print("Bright Data SDK - 批量操作演示")
    print("="*80)
    
    try:
        client = bdclient(api_token=API_TOKEN)
        
        # 批量搜索
        queries = [
            "Python SDK best practices",
            "Web scraping legal considerations",
            "API integration tutorials"
        ]
        
        print(f"\n[批量搜索] 查询数量: {len(queries)}")
        for i, q in enumerate(queries, 1):
            print(f"  {i}. {q}")
        
        # SDK自动处理并发请求
        results = client.search(query=queries)
        
        print(f"\n[结果] 收到 {len(results) if isinstance(results, list) else 1} 个响应")
        
    except Exception as e:
        print(f"\n[错误] {type(e).__name__}: {e}")

def demo_linkedin_search():
    """LinkedIn搜索演示"""
    print("\n" + "="*80)
    print("Bright Data SDK - LinkedIn搜索演示")
    print("="*80)
    
    try:
        client = bdclient(api_token=API_TOKEN)
        
        # 搜索LinkedIn职位
        print("\n[LinkedIn职位搜索]")
        result = client.search_linkedin.jobs(
            location="San Francisco",
            keyword="Python developer",
            country="US",
            time_range="Past month",
            job_type="Full-time"
        )
        
        print(f"搜索完成，快照ID: {result.get('snapshot_id', 'N/A')}")
        
        # 搜索公司
        company_urls = ["https://www.linkedin.com/company/bright-data"]
        print(f"\n[LinkedIn公司搜索] URL: {company_urls[0]}")
        
        result = client.scrape_linkedin.companies(company_urls)
        print(f"抓取状态: {result}")
        
    except Exception as e:
        print(f"\n[错误] {type(e).__name__}: {e}")

def demo_chatgpt_search():
    """ChatGPT搜索演示"""
    print("\n" + "="*80)
    print("Bright Data SDK - ChatGPT搜索演示")
    print("="*80)
    
    try:
        client = bdclient(api_token=API_TOKEN)
        
        prompts = [
            "What are the best practices for web scraping in 2024?",
            "How to use Bright Data SDK effectively?"
        ]
        
        print(f"\n[ChatGPT查询] 提示词数量: {len(prompts)}")
        
        result = client.search_chatGPT(
            prompt=prompts,
            additional_prompt=["Please provide code examples", "Focus on Python"]
        )
        
        print(f"\n[结果] 快照ID: {result.get('snapshot_id', 'N/A')}")
        
        # 下载结果
        if result.get('snapshot_id'):
            client.download_content(result, filename="chatgpt_results.json")
            print("结果已保存到: chatgpt_results.json")
            
    except Exception as e:
        print(f"\n[错误] {type(e).__name__}: {e}")

def demo_advanced_features():
    """高级功能演示"""
    print("\n" + "="*80)
    print("Bright Data SDK - 高级功能演示")
    print("="*80)
    
    try:
        # 自定义zone配置
        client = bdclient(
            api_token=API_TOKEN,
            auto_create_zones=True,  # 自动创建zone
            web_unlocker_zone="custom_web_zone",
            serp_zone="custom_serp_zone"
        )
        
        # 列出可用的zones
        print("\n[可用Zones]")
        zones = client.list_zones()
        if zones:
            for zone in zones[:5]:  # 只显示前5个
                print(f"  - {zone}")
        
        # 异步请求示例
        print("\n[异步请求]")
        urls = [
            "https://example.com/page1",
            "https://example.com/page2"
        ]
        
        results = client.scrape(
            url=urls,
            async_request=True,
            max_workers=5,
            timeout=60
        )
        
        print(f"异步请求已提交，结果: {type(results)}")
        
    except Exception as e:
        print(f"\n[错误] {type(e).__name__}: {e}")

def main():
    """主函数"""
    print(f"Bright Data SDK 实战演示")
    print(f"时间: {datetime.now()}")
    print(f"API令牌: {API_TOKEN[:20]}...")
    
    # 运行各个演示
    demo_basic_search()
    demo_scrape_website()
    demo_batch_operations()
    demo_linkedin_search()
    demo_chatgpt_search()
    demo_advanced_features()
    
    print("\n" + "="*80)
    print("演示完成！")
    print("\n提示：")
    print("1. 确保API令牌有效且具有管理员权限")
    print("2. 某些功能可能需要特定的zone配置")
    print("3. 查看生成的JSON文件以获取完整结果")

if __name__ == "__main__":
    main()