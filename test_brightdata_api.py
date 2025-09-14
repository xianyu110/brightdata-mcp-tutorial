#!/usr/bin/env python3
"""
Bright Data API 连接测试脚本
用于测试不同的API端点和请求格式
"""

import requests
import json
from datetime import datetime

# API令牌
API_TOKEN = "your_api_token_here"

# 测试不同的端点和请求格式
test_configs = [
    {
        "name": "SERP API - Google搜索",
        "url": "https://api.brightdata.com/serp/req",
        "headers": {
            "Authorization": f"Bearer {API_TOKEN}",
            "Content-Type": "application/json"
        },
        "body": {
            "country": "us",
            "domain": "google",
            "keyword": "Python web scraping",
            "num": 10
        }
    },
    {
        "name": "Data Collector API",
        "url": "https://api.brightdata.com/dca/trigger",
        "headers": {
            "Authorization": f"Bearer {API_TOKEN}",
            "Content-Type": "application/json"
        },
        "body": {
            "collector": "google_search",
            "input": {
                "search": "Python tutorial"
            }
        }
    },
    {
        "name": "Web Unlocker API",
        "url": f"https://api.brightdata.com/request",
        "headers": {
            "Authorization": f"Bearer {API_TOKEN}",
            "Content-Type": "application/json"
        },
        "body": {
            "url": "https://www.google.com/search?q=test",
            "render": True
        }
    },
    {
        "name": "使用API密钥作为查询参数",
        "url": f"https://api.brightdata.com/serp/req?customer={API_TOKEN}",
        "headers": {
            "Content-Type": "application/json"
        },
        "body": {
            "country": "us",
            "domain": "google",
            "keyword": "test"
        }
    },
    {
        "name": "使用基础认证",
        "url": "https://api.brightdata.com/serp/req",
        "auth": (API_TOKEN, ""),  # 使用基础认证
        "headers": {
            "Content-Type": "application/json"
        },
        "body": {
            "country": "us",
            "domain": "google",
            "keyword": "test"
        }
    }
]

def test_endpoint(config):
    """测试单个端点配置"""
    print(f"\n{'='*60}")
    print(f"测试: {config['name']}")
    print(f"URL: {config['url']}")
    print(f"请求体: {json.dumps(config['body'], indent=2)}")
    
    try:
        # 准备请求参数
        kwargs = {
            "timeout": 10,
            "json": config["body"]
        }
        
        if "headers" in config:
            kwargs["headers"] = config["headers"]
        
        if "auth" in config:
            kwargs["auth"] = config["auth"]
        
        # 发送请求
        response = requests.post(config["url"], **kwargs)
        
        print(f"状态码: {response.status_code}")
        print(f"响应头: {dict(response.headers)}")
        
        # 尝试解析JSON
        try:
            response_data = response.json()
            print(f"响应内容: {json.dumps(response_data, indent=2, ensure_ascii=False)[:500]}")
        except:
            print(f"响应内容 (文本): {response.text[:500]}")
            
        if response.status_code == 200:
            print("✅ 成功!")
            return True
            
    except requests.exceptions.RequestException as e:
        print(f"❌ 错误: {e}")
    
    return False

def main():
    """运行所有测试"""
    print(f"Bright Data API 连接测试")
    print(f"时间: {datetime.now()}")
    print(f"API令牌: {API_TOKEN[:20]}...")
    
    success_count = 0
    for config in test_configs:
        if test_endpoint(config):
            success_count += 1
    
    print(f"\n{'='*60}")
    print(f"测试完成: {success_count}/{len(test_configs)} 成功")
    
    # 额外测试：检查API令牌格式
    print(f"\nAPI令牌信息:")
    print(f"- 长度: {len(API_TOKEN)} 字符")
    print(f"- 格式: {'有效' if len(API_TOKEN) == 64 else '可能无效'}")

if __name__ == "__main__":
    main()