#!/usr/bin/env python3
"""
Google搜索结果抓取 - 博客演示代码
完整可运行的示例，配合博客文章使用
"""

from brightdata import bdclient
import json
import time
from datetime import datetime
from typing import List, Dict, Optional

# API配置
API_TOKEN = "your_api_token_here"

class GoogleSearchScraper:
    """Google搜索结果抓取器"""
    
    def __init__(self, api_token: str):
        """初始化抓取器"""
        self.client = bdclient(api_token=api_token)
        self.results_cache = {}
        
    def search_single(self, query: str, country: str = "us") -> Dict:
        """
        执行单个搜索查询
        
        Args:
            query: 搜索关键词
            country: 国家代码
            
        Returns:
            包含搜索结果的字典
        """
        print(f"\n[{datetime.now().strftime('%H:%M:%S')}] 搜索: {query}")
        
        try:
            # 执行搜索
            raw_results = self.client.search(
                query=query,
                search_engine="google",
                country=country
            )
            
            # 处理结果
            if isinstance(raw_results, str):
                # HTML响应
                return {
                    "query": query,
                    "country": country,
                    "timestamp": datetime.now().isoformat(),
                    "status": "success",
                    "data_type": "html",
                    "content_length": len(raw_results),
                    "preview": raw_results[:500] + "..." if len(raw_results) > 500 else raw_results
                }
            else:
                # 其他格式
                return {
                    "query": query,
                    "country": country,
                    "timestamp": datetime.now().isoformat(),
                    "status": "success",
                    "data_type": type(raw_results).__name__,
                    "content": raw_results
                }
                
        except Exception as e:
            return {
                "query": query,
                "country": country,
                "timestamp": datetime.now().isoformat(),
                "status": "error",
                "error": str(e)
            }
    
    def search_batch(self, queries: List[str], delay: int = 2) -> List[Dict]:
        """
        批量搜索多个关键词
        
        Args:
            queries: 关键词列表
            delay: 请求间隔（秒）
            
        Returns:
            搜索结果列表
        """
        results = []
        total = len(queries)
        
        print(f"\n开始批量搜索 {total} 个关键词...")
        
        for i, query in enumerate(queries, 1):
            print(f"\n进度: [{i}/{total}]")
            
            # 执行搜索
            result = self.search_single(query)
            results.append(result)
            
            # 缓存结果
            self.results_cache[query] = result
            
            # 延迟（最后一个不需要）
            if i < total:
                print(f"等待 {delay} 秒...")
                time.sleep(delay)
        
        return results
    
    def search_multiple_regions(self, query: str, countries: List[str]) -> Dict[str, Dict]:
        """
        在多个地区搜索同一关键词
        
        Args:
            query: 搜索关键词
            countries: 国家代码列表
            
        Returns:
            按国家分组的结果
        """
        results = {}
        
        print(f"\n在 {len(countries)} 个地区搜索: {query}")
        
        for country in countries:
            print(f"\n地区: {country}")
            result = self.search_single(query, country)
            results[country] = result
            time.sleep(1)  # 短暂延迟
        
        return results
    
    def save_results(self, results: any, filename: str = None):
        """保存搜索结果到文件"""
        if filename is None:
            filename = f"search_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        
        print(f"\n✅ 结果已保存到: {filename}")
        return filename

# ===== 演示函数 =====

# def demo_basic_search():
#     """演示1：基础搜索"""
#     print("\n" + "="*60)
#     print("演示1：基础搜索")
#     print("="*60)
    
#     scraper = GoogleSearchScraper(API_TOKEN)
    
#     # 单个搜索
#     result = scraper.search_single("Python web scraping tutorial 2024")
    
#     # 显示结果
#     print("\n搜索结果:")
#     print(f"- 状态: {result['status']}")
#     print(f"- 数据类型: {result.get('data_type', 'unknown')}")
#     print(f"- 时间戳: {result['timestamp']}")
    
#     if result['status'] == 'success':
#         print(f"- 内容大小: {result.get('content_length', 0)} 字符")
    
#     # 保存结果
#     scraper.save_results(result, "demo1_basic_search.json")

def demo_batch_search():
    """演示2：批量搜索"""
    print("\n" + "="*60)
    print("演示2：批量搜索")
    print("="*60)
    
    scraper = GoogleSearchScraper(API_TOKEN)
    
    # 搜索关键词列表
    keywords = [
        "machine learning algorithms",
        "deep learning frameworks",
        "neural network architectures"
    ]
    
    # 批量搜索
    results = scraper.search_batch(keywords, delay=2)
    
    # 统计结果
    success_count = sum(1 for r in results if r['status'] == 'success')
    print(f"\n搜索完成: {success_count}/{len(results)} 成功")
    
    # 保存结果
    scraper.save_results(results, "demo2_batch_search.json")

def demo_regional_search():
    """演示3：多地区搜索"""
    print("\n" + "="*60)
    print("演示3：多地区搜索")
    print("="*60)
    
    scraper = GoogleSearchScraper(API_TOKEN)
    
    # 在不同地区搜索同一关键词
    query = "AI technology trends"
    countries = ["us", "uk", "ca", "au"]  # 美国、英国、加拿大、澳大利亚
    
    results = scraper.search_multiple_regions(query, countries)
    
    # 显示各地区结果
    print("\n各地区搜索结果:")
    for country, result in results.items():
        status = "✅" if result['status'] == 'success' else "❌"
        print(f"- {country}: {status}")
    
    # 保存结果
    scraper.save_results(results, "demo3_regional_search.json")

def demo_competitor_monitoring():
    """演示4：竞争对手监控"""
    print("\n" + "="*60)
    print("演示4：竞争对手监控")
    print("="*60)
    
    scraper = GoogleSearchScraper(API_TOKEN)
    
    # 监控的关键词和竞争对手
    keywords = [
        "web scraping services",
        "data extraction API",
        "proxy network providers"
    ]
    
    competitors = [
        {"name": "Bright Data", "domain": "brightdata.com"},
        {"name": "ScrapingBee", "domain": "scrapingbee.com"},
        {"name": "Oxylabs", "domain": "oxylabs.io"}
    ]
    
    monitoring_results = {
        "timestamp": datetime.now().isoformat(),
        "keywords": keywords,
        "competitors": competitors,
        "results": {}
    }
    
    # 搜索每个关键词
    for keyword in keywords:
        print(f"\n监控关键词: {keyword}")
        
        result = scraper.search_single(keyword)
        
        # 简单的竞争对手检测（实际应用中需要更复杂的解析）
        if result['status'] == 'success' and 'preview' in result:
            content_lower = result['preview'].lower()
            
            keyword_result = {
                "search_result": result,
                "competitor_found": {}
            }
            
            for competitor in competitors:
                found = competitor['domain'].lower() in content_lower
                keyword_result['competitor_found'][competitor['name']] = found
                
            monitoring_results['results'][keyword] = keyword_result
            
            # 显示发现的竞争对手
            found_competitors = [name for name, found in keyword_result['competitor_found'].items() if found]
            if found_competitors:
                print(f"  发现竞争对手: {', '.join(found_competitors)}")
            else:
                print(f"  未在预览中发现监控的竞争对手")
        
        time.sleep(2)
    
    # 保存监控结果
    scraper.save_results(monitoring_results, "demo4_competitor_monitoring.json")

def main():
    """主函数 - 运行所有演示"""
    print("Google搜索结果抓取 - 完整演示")
    print("使用Bright Data SDK")
    print(f"时间: {datetime.now()}")
    
    # 选择要运行的演示
    demos = {
        "1": ("基础搜索", demo_basic_search),
        "2": ("批量搜索", demo_batch_search),
        "3": ("多地区搜索", demo_regional_search),
        "4": ("竞争对手监控", demo_competitor_monitoring),
        "5": ("运行所有演示", None)
    }
    
    print("\n请选择演示:")
    for key, (name, _) in demos.items():
        print(f"{key}. {name}")
    
    choice = input("\n请输入选项 (1-5): ").strip()
    
    if choice == "5":
        # 运行所有演示
        for key, (name, func) in demos.items():
            if key != "5" and func:
                func()
                time.sleep(3)  # 演示之间的延迟
    elif choice in demos and demos[choice][1]:
        # 运行选定的演示
        demos[choice][1]()
    else:
        print("无效选项")

if __name__ == "__main__":
    # 直接运行多地区搜索演示
    # print("Google搜索结果抓取 - 多地区搜索演示")
    # print("使用Bright Data SDK")
    # print(f"时间: {datetime.now()}")
    
    # 运行多地区搜索演示
    demo_competitor_monitoring()