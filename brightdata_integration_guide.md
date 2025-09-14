# Bright Data MCP API 实战指南：Google搜索结果抓取

## 实战演示：使用Python调用MCP API实时抓取Google搜索结果

### 1. API请求结构详解

#### 基础请求格式
```json
{
  "url": "https://www.google.com/search?q=Python+tutorial&num=10",
  "browser": true,      // 使用浏览器模式处理JavaScript
  "unlocker": true,     // 自动解锁反爬虫机制
  "pro": 1,            // 使用Pro模式提高成功率
  "wait_for": {        // 等待页面元素加载
    "selector": "div#search",
    "timeout": 10000
  },
  "extract": {         // 数据提取规则
    "results": {
      "selector": "div.g",
      "multiple": true,
      "fields": {
        "title": "h3",
        "url": {
          "selector": "a",
          "attribute": "href"
        },
        "description": "div.VwiC3b"
      }
    }
  }
}
```

#### 请求头配置
```json
{
  "Authorization": "Bearer YOUR_API_TOKEN",
  "Content-Type": "application/json"
}
```

### 2. 返回数据格式（JSON示例）

```json
{
  "status": "success",
  "data": {
    "url": "https://www.google.com/search?q=Python+tutorial",
    "extract": {
      "results": [
        {
          "title": "Python Tutorial - W3Schools",
          "url": "https://www.w3schools.com/python/",
          "description": "Well organized and easy to understand Web building tutorials with lots of examples of how to use HTML, CSS, JavaScript, SQL, Python..."
        },
        {
          "title": "The Python Tutorial — Python 3.12 documentation",
          "url": "https://docs.python.org/3/tutorial/",
          "description": "This tutorial introduces the reader informally to the basic concepts and features of the Python language and system..."
        }
      ],
      "total_results": "About 2,340,000,000 results"
    }
  },
  "metadata": {
    "request_id": "req_abc123",
    "timestamp": "2024-01-15T10:30:45Z",
    "credits_used": 1
  }
}
```

### 3. 处理动态网页的关键参数

#### 使用browser参数
```python
# 启用浏览器模式来处理JavaScript渲染的内容
request_body = {
    "url": target_url,
    "browser": True,  # 关键：启用浏览器模式
    "unlocker": True, # 自动处理验证码和反爬虫
}
```

#### 高级动态内容处理
```python
# 处理复杂的单页应用(SPA)
advanced_request = {
    "url": "https://example.com/spa",
    "browser": True,
    "unlocker": True,
    "pro": 1,  # Pro模式：更高成功率
    "wait_for": {
        "selector": ".content-loaded",  # 等待特定元素
        "timeout": 15000
    },
    "execute_js": [  # 执行自定义JavaScript
        "window.scrollTo(0, document.body.scrollHeight);",
        "await new Promise(r => setTimeout(r, 2000));"
    ],
    "viewport": {  # 设置浏览器视口
        "width": 1920,
        "height": 1080
    }
}
```

### 4. 自动化工具集成方案

#### 4.1 n8n 集成

**n8n工作流配置：**
```json
{
  "nodes": [{
    "name": "Bright Data MCP",
    "type": "n8n-nodes-base.httpRequest",
    "parameters": {
      "method": "POST",
      "url": "https://api.brightdata.com/mcp/v1/extract",
      "authentication": "genericCredentialType",
      "genericAuthType": "httpHeaderAuth",
      "sendHeaders": true,
      "headerParameters": {
        "parameters": [{
          "name": "Authorization",
          "value": "Bearer {{$credentials.brightDataApiToken}}"
        }]
      },
      "sendBody": true,
      "bodyParameters": {
        "parameters": [{
          "name": "url",
          "value": "={{$json[\"search_url\"]}}"
        }, {
          "name": "browser",
          "value": true
        }, {
          "name": "unlocker",
          "value": true
        }]
      }
    }
  }]
}
```

#### 4.2 Zapier 集成

**Zapier Zap配置步骤：**
1. **触发器**: Schedule by Zapier（定时触发）
2. **动作**: Webhooks by Zapier
   - URL: `https://api.brightdata.com/mcp/v1/extract`
   - Method: POST
   - Headers:
     ```
     Authorization: Bearer YOUR_API_TOKEN
     Content-Type: application/json
     ```
   - Data:
     ```json
     {
       "url": "https://www.google.com/search?q={{search_term}}",
       "browser": true,
       "unlocker": true
     }
     ```

#### 4.3 Apache Airflow 集成

**Airflow DAG示例：**
```python
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.http.operators.http import SimpleHttpOperator
from datetime import datetime, timedelta

default_args = {
    'owner': 'data_team',
    'depends_on_past': False,
    'start_date': datetime(2024, 1, 1),
    'email_on_failure': True,
    'email_on_retry': False,
    'retries': 2,
    'retry_delay': timedelta(minutes=5)
}

dag = DAG(
    'brightdata_scraping_pipeline',
    default_args=default_args,
    description='定期抓取搜索结果',
    schedule_interval='0 */6 * * *',  # 每6小时运行一次
    catchup=False
)

# 使用HTTP操作符调用Bright Data API
scrape_task = SimpleHttpOperator(
    task_id='scrape_google_results',
    http_conn_id='brightdata_api',  # 在Airflow中配置的连接
    endpoint='/mcp/v1/extract',
    method='POST',
    headers={
        "Authorization": "Bearer {{ var.value.BRIGHTDATA_API_TOKEN }}",
        "Content-Type": "application/json"
    },
    data={
        "url": "https://www.google.com/search?q=AI+news+{{ ds }}",
        "browser": True,
        "unlocker": True,
        "pro": 1
    },
    dag=dag
)
```

#### 4.4 Make (Integromat) 集成

**Make场景配置：**
1. 添加 HTTP 模块
2. 配置请求：
   - URL: `https://api.brightdata.com/mcp/v1/extract`
   - Method: POST
   - Headers: 添加Authorization头
   - Body: JSON格式的请求数据

### 5. 最佳实践建议

1. **错误处理**：始终实现重试机制和错误日志
2. **速率限制**：遵守API限制，避免过度请求
3. **数据验证**：验证返回数据的完整性
4. **成本优化**：合理使用browser和pro参数
5. **监控告警**：设置自动化监控和告警机制

### 6. 完整Python实现示例

请参考 `brightdata_mcp_demo.py` 文件，其中包含：
- 完整的API客户端实现
- 错误处理和重试逻辑
- 数据解析和格式化
- 多种集成方案示例

### 7. 配置MCP Server

在您的应用配置文件中添加：
```json
{
    "mcpServers": {
        "Bright Data": {
            "command": "npx",
            "args": ["@brightdata/mcp"],
            "env": {
                "API_TOKEN": "YOUR_API_TOKEN_HERE"
            }
        }
    }
}
```

## 总结

Bright Data MCP API提供了强大的网页数据抓取能力，通过合理配置browser、unlocker等参数，可以轻松处理各种复杂的动态网页。结合各种自动化工具，能够构建稳定高效的数据采集管道。