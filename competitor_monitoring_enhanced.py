#!/usr/bin/env python3
"""
竞争对手监控增强版
分析完整的搜索结果内容
"""

from brightdata import bdclient
from bs4 import BeautifulSoup
import json
import re
from datetime import datetime

# API配置
API_TOKEN = "your_api_token_here"

def analyze_html_content(html_content, competitors):
    """
    分析HTML内容，查找竞争对手信息
    
    Args:
        html_content: HTML内容
        competitors: 竞争对手列表
        
    Returns:
        分析结果
    """
    try:
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # 获取所有文本内容
        text_content = soup.get_text().lower()
        
        # 查找所有链接
        all_links = []
        for link in soup.find_all('a', href=True):
            href = link.get('href', '').lower()
            text = link.get_text(strip=True).lower()
            all_links.append({
                'href': href,
                'text': text
            })
        
        # 分析每个竞争对手
        competitor_analysis = {}
        
        for competitor in competitors:
            domain_lower = competitor['domain'].lower()
            name_lower = competitor['name'].lower()
            
            analysis = {
                'name': competitor['name'],
                'domain': competitor['domain'],
                'found_in_text': False,
                'found_in_links': False,
                'occurrences': 0,
                'positions': []
            }
            
            # 在文本中查找
            domain_count = text_content.count(domain_lower)
            name_count = text_content.count(name_lower)
            analysis['occurrences'] = domain_count + name_count
            analysis['found_in_text'] = analysis['occurrences'] > 0
            
            # 在链接中查找
            position = 1
            for link in all_links:
                if domain_lower in link['href'] or domain_lower in link['text']:
                    analysis['found_in_links'] = True
                    analysis['positions'].append({
                        'position': position,
                        'type': 'link',
                        'text': link['text'][:100]
                    })
                elif name_lower in link['text']:
                    analysis['positions'].append({
                        'position': position,
                        'type': 'mention',
                        'text': link['text'][:100]
                    })
                position += 1
            
            competitor_analysis[competitor['name']] = analysis
        
        # 提取页面标题和描述
        title = soup.find('title')
        page_info = {
            'title': title.text if title else 'N/A',
            'total_links': len(all_links),
            'content_length': len(text_content)
        }
        
        return {
            'page_info': page_info,
            'competitor_analysis': competitor_analysis,
            'success': True
        }
        
    except Exception as e:
        return {
            'error': str(e),
            'success': False
        }

def enhanced_competitor_monitoring():
    """增强版竞争对手监控"""
    print("\n" + "="*60)
    print("竞争对手监控 - 增强版")
    print("="*60)
    
    client = bdclient(api_token=API_TOKEN)
    
    # 监控配置
    keywords = [
        "web scraping services",
        "data extraction API",
        "proxy network providers"
    ]
    
    competitors = [
        {"name": "Bright Data", "domain": "brightdata.com"},
        {"name": "ScrapingBee", "domain": "scrapingbee.com"},
        {"name": "Oxylabs", "domain": "oxylabs.io"},
        {"name": "Apify", "domain": "apify.com"},
        {"name": "ScraperAPI", "domain": "scraperapi.com"}
    ]
    
    all_results = {
        "timestamp": datetime.now().isoformat(),
        "keywords": keywords,
        "competitors": competitors,
        "detailed_results": {}
    }
    
    # 搜索每个关键词
    for keyword in keywords:
        print(f"\n搜索关键词: {keyword}")
        
        try:
            # 执行搜索
            print(f"  正在获取搜索结果...")
            results = client.search(query=keyword, country="us")
            
            if isinstance(results, str):
                # 分析HTML内容
                print(f"  分析内容 ({len(results)} 字符)...")
                analysis = analyze_html_content(results, competitors)
                
                if analysis['success']:
                    # 显示发现的竞争对手
                    found_competitors = []
                    for comp_name, comp_data in analysis['competitor_analysis'].items():
                        if comp_data['found_in_text'] or comp_data['found_in_links']:
                            found_competitors.append(comp_name)
                            if comp_data['positions']:
                                print(f"    ✅ {comp_name}: 找到 {len(comp_data['positions'])} 处")
                    
                    if not found_competitors:
                        print(f"    ⚠️  未发现监控的竞争对手")
                    
                    # 保存结果
                    all_results['detailed_results'][keyword] = {
                        'search_time': datetime.now().isoformat(),
                        'page_info': analysis['page_info'],
                        'competitor_analysis': analysis['competitor_analysis']
                    }
                else:
                    print(f"    ❌ 分析失败: {analysis.get('error', 'Unknown error')}")
            else:
                print(f"    ⚠️  意外的响应格式: {type(results)}")
                
        except Exception as e:
            print(f"    ❌ 搜索错误: {e}")
    
    # 生成摘要报告
    print("\n" + "="*60)
    print("监控摘要报告")
    print("="*60)
    
    for keyword, data in all_results['detailed_results'].items():
        print(f"\n关键词: {keyword}")
        if 'competitor_analysis' in data:
            for comp_name, comp_data in data['competitor_analysis'].items():
                if comp_data['found_in_text'] or comp_data['found_in_links']:
                    print(f"  - {comp_name}: 出现 {comp_data['occurrences']} 次")
                    if comp_data['positions']:
                        print(f"    最高排名: 第 {comp_data['positions'][0]['position']} 位")
    
    # 保存详细结果
    output_file = f"competitor_monitoring_enhanced_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(all_results, f, indent=2, ensure_ascii=False)
    
    print(f"\n✅ 详细结果已保存到: {output_file}")

if __name__ == "__main__":
    enhanced_competitor_monitoring()