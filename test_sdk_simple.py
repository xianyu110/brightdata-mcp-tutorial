#!/usr/bin/env python3
"""
Bright Data SDK 简单测试
测试基本功能是否正常工作
"""

from brightdata import bdclient
import json
from datetime import datetime

# API令牌
API_TOKEN = "your_api_token_here"

def test_basic():
    """基础功能测试"""
    print("Bright Data SDK 简单测试")
    print(f"时间: {datetime.now()}")
    print("="*60)
    
    try:
        # 初始化客户端
        print("\n1. 初始化客户端...")
        client = bdclient(api_token=API_TOKEN)
        print("✅ 客户端初始化成功")
        
        # 简单搜索测试
        print("\n2. 执行简单搜索...")
        query = "test"
        results = client.search(query=query)
        
        print(f"✅ 搜索完成")
        print(f"结果类型: {type(results)}")
        
        # 显示部分结果
        if isinstance(results, str):
            print(f"结果预览: {results[:200]}...")
        elif isinstance(results, dict):
            print(f"结果预览: {json.dumps(results, indent=2)[:200]}...")
        elif isinstance(results, list):
            print(f"结果数量: {len(results)}")
            
        # 测试解析功能
        try:
            print("\n3. 测试解析功能...")
            parsed = client.parse_content(results)
            print(f"✅ 解析成功")
            print(f"解析结果预览: {str(parsed)[:200]}...")
        except Exception as e:
            print(f"❌ 解析失败: {e}")
            
        # 列出zones
        print("\n4. 列出可用zones...")
        try:
            zones = client.list_zones()
            if zones:
                print(f"✅ 找到 {len(zones)} 个zones")
                for zone in zones[:3]:
                    print(f"   - {zone}")
            else:
                print("⚠️  未找到zones")
        except Exception as e:
            print(f"❌ 获取zones失败: {e}")
            
    except Exception as e:
        print(f"\n❌ 错误: {type(e).__name__}")
        print(f"详情: {e}")
        
        # 尝试获取更多错误信息
        if hasattr(e, 'response'):
            print(f"响应状态码: {getattr(e.response, 'status_code', 'N/A')}")
            print(f"响应内容: {getattr(e.response, 'text', 'N/A')[:500]}")

if __name__ == "__main__":
    test_basic()