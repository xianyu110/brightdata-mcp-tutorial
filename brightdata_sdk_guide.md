# Bright Data Python SDK 完整使用指南

## 📋 目录

1. [快速开始](#快速开始)
2. [SDK安装与配置](#sdk安装与配置)
3. [核心功能详解](#核心功能详解)
4. [实战示例](#实战示例)
5. [高级功能](#高级功能)
6. [错误处理](#错误处理)
7. [最佳实践](#最佳实践)

## 快速开始

### 安装SDK

```bash
pip install brightdata-sdk
```

### 基础示例

```python
from brightdata import bdclient

# 初始化客户端
client = bdclient(api_token="your_api_token")

# 执行搜索
results = client.search("Python web scraping")

# 解析结果
print(client.parse_content(results))
```

## SDK安装与配置

### 1. 安装要求

- Python 3.8+
- 依赖包会自动安装：requests, aiohttp, beautifulsoup4, openai等

### 2. 客户端配置

```python
from brightdata import bdclient

# 基础配置
client = bdclient(api_token="your_api_token")

# 高级配置
client = bdclient(
    api_token="your_api_token",
    auto_create_zones=True,      # 自动创建zones
    web_unlocker_zone="custom_web_zone",
    serp_zone="custom_serp_zone"
)
```

### 3. 环境变量配置

创建 `.env` 文件：

```env
BRIGHTDATA_API_TOKEN=your_api_token
```

然后在代码中：

```python
client = bdclient()  # 自动从.env读取
```

## 核心功能详解

### 1. 网页搜索 - search()

```python
# 单个搜索
result = client.search("best laptops 2024")

# 批量搜索
queries = ["Python tutorial", "Web scraping", "API integration"]
results = client.search(query=queries)

# 高级参数
result = client.search(
    query="machine learning",
    search_engine="google",    # 或 "bing", "yandex"
    country="us",             # 两字母国家代码
    data_format="markdown",   # 或 "screenshot", "json"
    async_request=True,       # 异步处理
    max_workers=10,          # 并发数
    timeout=30               # 超时时间
)
```

### 2. 网页抓取 - scrape()

```python
# 单个URL
result = client.scrape("https://example.com")

# 多个URL（并发处理）
urls = [
    "https://example.com/page1",
    "https://example.com/page2",
    "https://example.com/page3"
]
results = client.scrape(url=urls)

# 高级参数
result = client.scrape(
    url="https://example.com",
    country="us",
    data_format="markdown",
    async_request=True
)

# 保存结果
client.download_content(result, filename="scrape_results.json")
```

### 3. 网站爬取 - crawl()

```python
# 爬取整个网站（包括子页面）
result = client.crawl(
    url="https://example.com/",
    depth=2,                              # 爬取深度
    filter="/product/",                   # 只爬取包含此路径的URL
    exclude_filter="/ads/",               # 排除包含此路径的URL
    custom_output_fields=["markdown", "url", "page_title"]
)

print(f"爬取任务ID: {result['snapshot_id']}")
```

### 4. LinkedIn数据采集

#### 搜索功能

```python
# 搜索职位
jobs = client.search_linkedin.jobs(
    location="San Francisco",
    keyword="Python developer",
    country="US",
    time_range="Past month",
    job_type="Full-time"
)

# 搜索个人资料
profiles = client.search_linkedin.profiles(
    first_names=["John", "Jane"],
    last_names=["Smith", "Doe"]
)

# 搜索帖子
posts = client.search_linkedin.posts(
    profile_url="https://www.linkedin.com/in/username",
    start_date="2024-01-01T00:00:00.000Z",
    end_date="2024-12-31T23:59:59.000Z"
)
```

#### 抓取功能

```python
# 抓取公司信息
company_urls = [
    "https://www.linkedin.com/company/bright-data",
    "https://www.linkedin.com/company/microsoft"
]
companies = client.scrape_linkedin.companies(company_urls)

# 抓取职位信息
job_urls = ["https://www.linkedin.com/jobs/view/123456789"]
jobs = client.scrape_linkedin.jobs(job_urls)

# 抓取个人资料
profile_url = "https://www.linkedin.com/in/username"
profile = client.scrape_linkedin.profiles(profile_url)
```

### 5. ChatGPT集成

```python
# 单个提示
result = client.search_chatGPT(
    prompt="Explain quantum computing in simple terms"
)

# 多个提示和后续问题
result = client.search_chatGPT(
    prompt=[
        "What are the top 3 programming languages in 2024?",
        "Best practices for web scraping",
        "How to build an API"
    ],
    additional_prompt=[
        "Can you provide code examples?",
        "What about legal considerations?",
        "Which frameworks do you recommend?"
    ]
)

# 下载结果
client.download_content(result, filename="chatgpt_responses.json")
```

### 6. 浏览器连接

```python
from playwright.sync_api import Playwright, sync_playwright

# 配置浏览器凭据
client = bdclient(
    api_token="your_api_token",
    browser_username="username-zone-browser_zone1",
    browser_password="your_password"
)

def scrape_with_browser(playwright: Playwright):
    # 连接到Bright Data的浏览器
    browser = playwright.chromium.connect_over_cdp(client.connect_browser())
    
    try:
        page = browser.new_page()
        page.goto("https://example.com", timeout=120000)
        
        # 执行浏览器操作
        content = page.content()
        title = page.title()
        
        # 截图
        page.screenshot(path="screenshot.png")
        
        return {"title": title, "content": content}
    finally:
        browser.close()

# 运行
with sync_playwright() as playwright:
    result = scrape_with_browser(playwright)
```

## 实战示例

### 示例1：电商价格监控

```python
import json
from datetime import datetime

def monitor_product_prices(product_urls):
    """监控产品价格"""
    client = bdclient(api_token="your_api_token")
    
    results = []
    for url in product_urls:
        try:
            # 抓取产品页面
            data = client.scrape(
                url=url,
                data_format="markdown"
            )
            
            # 解析内容
            parsed = client.parse_content(data)
            
            results.append({
                "url": url,
                "timestamp": datetime.now().isoformat(),
                "data": parsed
            })
            
        except Exception as e:
            print(f"错误抓取 {url}: {e}")
    
    # 保存结果
    with open("price_monitor.json", "w") as f:
        json.dump(results, f, indent=2)
    
    return results

# 使用示例
products = [
    "https://www.amazon.com/dp/B08N5WRWNW",
    "https://www.amazon.com/dp/B09G9FPHY6"
]
monitor_product_prices(products)
```

### 示例2：新闻聚合器

```python
def aggregate_news(topics):
    """聚合多个主题的新闻"""
    client = bdclient(api_token="your_api_token")
    
    all_news = {}
    
    for topic in topics:
        # 搜索新闻
        search_query = f"{topic} news {datetime.now().year}"
        results = client.search(
            query=search_query,
            search_engine="google",
            data_format="markdown"
        )
        
        # 解析结果
        parsed = client.parse_content(results)
        all_news[topic] = parsed
    
    return all_news

# 使用示例
topics = ["AI technology", "climate change", "space exploration"]
news = aggregate_news(topics)
```

### 示例3：竞品分析

```python
def analyze_competitors(competitor_domains):
    """分析竞争对手网站"""
    client = bdclient(api_token="your_api_token")
    
    analysis = {}
    
    for domain in competitor_domains:
        # 爬取网站
        crawl_result = client.crawl(
            url=f"https://{domain}",
            depth=2,
            filter="/product/",
            custom_output_fields=["markdown", "url", "page_title"]
        )
        
        snapshot_id = crawl_result['snapshot_id']
        
        # 等待爬取完成并下载结果
        # 注意：crawl是异步操作，可能需要等待
        analysis[domain] = {
            "snapshot_id": snapshot_id,
            "crawl_time": datetime.now().isoformat()
        }
    
    return analysis
```

## 高级功能

### 1. 异步操作

```python
import asyncio

async def async_scraping():
    """异步抓取示例"""
    client = bdclient(api_token="your_api_token")
    
    urls = ["https://example1.com", "https://example2.com", "https://example3.com"]
    
    # 异步抓取
    results = await client.scrape(
        url=urls,
        async_request=True,
        max_workers=5
    )
    
    return results

# 运行异步函数
results = asyncio.run(async_scraping())
```

### 2. Zone管理

```python
# 列出所有zones
zones = client.list_zones()
for zone in zones:
    print(f"Zone: {zone['name']}, Type: {zone['type']}")

# 使用特定zone
result = client.scrape(
    url="https://example.com",
    zone="custom_unlocker_zone"
)
```

### 3. 数据处理工具

```python
# 下载快照
client.download_snapshot(
    snapshot_id="s_abc123xyz",
    filename="snapshot_data.json"
)

# 批量下载
snapshots = ["s_abc123", "s_def456", "s_ghi789"]
for snapshot in snapshots:
    client.download_snapshot(snapshot, f"{snapshot}.json")
```

## 错误处理

### 常见错误和解决方案

```python
from brightdata import bdclient
import time

def safe_scrape(url, max_retries=3):
    """带重试机制的安全抓取"""
    client = bdclient(api_token="your_api_token")
    
    for attempt in range(max_retries):
        try:
            result = client.scrape(url)
            return result
            
        except Exception as e:
            error_type = type(e).__name__
            
            if "timeout" in str(e).lower():
                print(f"超时错误，重试 {attempt + 1}/{max_retries}")
                time.sleep(5 * (attempt + 1))  # 递增延迟
                
            elif "authentication" in str(e).lower():
                print("认证错误：请检查API令牌")
                raise
                
            elif "rate limit" in str(e).lower():
                print("速率限制，等待60秒...")
                time.sleep(60)
                
            else:
                print(f"未知错误: {error_type} - {e}")
                if attempt == max_retries - 1:
                    raise
    
    return None
```

## 最佳实践

### 1. API令牌安全

```python
import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# 从环境变量获取令牌
api_token = os.getenv("BRIGHTDATA_API_TOKEN")
if not api_token:
    raise ValueError("未设置BRIGHTDATA_API_TOKEN环境变量")

client = bdclient(api_token=api_token)
```

### 2. 日志记录

```python
import logging

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    filename='brightdata.log'
)

logger = logging.getLogger('brightdata_app')

def scrape_with_logging(url):
    """带日志的抓取"""
    logger.info(f"开始抓取: {url}")
    
    try:
        client = bdclient(api_token="your_api_token")
        result = client.scrape(url)
        logger.info(f"成功抓取: {url}")
        return result
        
    except Exception as e:
        logger.error(f"抓取失败 {url}: {e}")
        raise
```

### 3. 性能优化

```python
# 批量操作优化
def efficient_batch_scraping(urls, batch_size=10):
    """高效的批量抓取"""
    client = bdclient(api_token="your_api_token")
    
    all_results = []
    
    # 分批处理
    for i in range(0, len(urls), batch_size):
        batch = urls[i:i + batch_size]
        
        # 并发抓取当前批次
        results = client.scrape(
            url=batch,
            max_workers=min(batch_size, 10),  # 限制并发数
            timeout=60
        )
        
        all_results.extend(results)
        
        # 批次间延迟，避免触发限制
        if i + batch_size < len(urls):
            time.sleep(2)
    
    return all_results
```

## 总结

Bright Data Python SDK提供了强大而灵活的网页数据采集能力：

1. **简单易用** - 几行代码即可开始采集
2. **功能丰富** - 支持搜索、抓取、爬取、LinkedIn数据等
3. **高性能** - 自动并发处理，支持异步操作
4. **可靠稳定** - 内置重试机制和错误处理

记住始终遵守网站的使用条款和robots.txt文件，合理使用采集功能。

## 资源链接

- [官方文档](https://docs.brightdata.com/api-reference/SDK)
- [GitHub仓库](https://github.com/brightdata/bright-data-sdk-python)
- [API参考](https://brightdata.com/cp/api_reference)
- [技术支持](https://brightdata.com/support)