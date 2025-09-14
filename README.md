# Bright Data Python SDK 完整教程

本项目包含了Bright Data Python SDK的完整使用教程和实战示例。

## 📁 项目结构

```
brightdata-mcp-tutorial/
├── README.md                              # 项目说明文档
├── brightdata_sdk_guide.md                # SDK完整使用指南 ⭐
├── brightdata_sdk_demo.py                 # SDK功能演示代码
├── test_sdk_simple.py                     # SDK简单测试脚本
├── brightdata_mcp_demo.py                 # 原始API演示代码
├── brightdata_integration_guide.md        # 集成指南
├── brightdata_nodejs_example.js           # Node.js示例
└── brightdata_automation_templates.yaml   # 自动化模板
```

## 🚀 快速开始

### 1. 安装Python SDK（推荐）

```bash
# 安装SDK
pip install brightdata-sdk

# 运行SDK演示
python3 brightdata_sdk_demo.py

# 或运行简单测试
python3 test_sdk_simple.py
```

### 2. SDK基础使用

```python
from brightdata import bdclient

# 初始化客户端
client = bdclient(api_token="your_api_token")

# 搜索网页
results = client.search("Python web scraping")
print(client.parse_content(results))

# 抓取网页
data = client.scrape("https://example.com")
client.download_content(data, filename="results.json")
```

### 3. Node.js示例

```bash
# 安装依赖
npm install

# 运行服务
node brightdata_nodejs_example.js
```

## 📖 核心文档

### 🌟 brightdata_sdk_guide.md - SDK完整使用指南
- SDK安装与配置
- 核心功能详解（search、scrape、crawl）
- LinkedIn数据采集
- ChatGPT集成
- 浏览器连接
- 实战示例（电商监控、新闻聚合、竞品分析）
- 错误处理和最佳实践

### 其他文档
- **brightdata_integration_guide.md** - API集成指南
- **brightdata_automation_templates.yaml** - 12种自动化平台配置模板

## 🔑 API配置

### 方式1：代码中直接配置
```python
client = bdclient(api_token="your_api_token_here")
```

### 方式2：环境变量配置
创建 `.env` 文件：
```env
BRIGHTDATA_API_TOKEN=your_api_token
```

然后在代码中：
```python
client = bdclient()  # 自动从.env读取
```

## 🛠️ 主要功能

- ✅ **网页搜索** - Google、Bing、Yandex搜索
- ✅ **网页抓取** - 单个或批量URL抓取
- ✅ **网站爬取** - 深度爬取整个网站
- ✅ **LinkedIn数据** - 职位、公司、个人资料、帖子
- ✅ **ChatGPT集成** - AI对话和问答
- ✅ **浏览器连接** - Playwright/Selenium集成
- ✅ **异步操作** - 高性能并发处理
- ✅ **数据导出** - JSON/CSV格式

## 💡 使用技巧

1. **批量操作优化**
   ```python
   # SDK自动处理并发
   results = client.scrape(url=["url1", "url2", "url3"])
   ```

2. **错误处理**
   ```python
   try:
       result = client.search("query")
   except Exception as e:
       print(f"错误: {e}")
   ```

3. **异步请求**
   ```python
   result = client.scrape(url="https://example.com", async_request=True)
   ```

## 📚 相关资源

- [Bright Data官网](https://brightdata.com)
- [SDK文档](https://docs.brightdata.com/api-reference/SDK)
- [GitHub仓库](https://github.com/brightdata/bright-data-sdk-python)
- [技术支持](https://brightdata.com/support)

## 📝 注意事项

- API令牌需要管理员权限
- 前3个月免费，每月5000次请求额度
- 遵守网站使用条款和robots.txt
- 合理控制请求频率避免触发限制

## 🤝 技术支持

如有问题：
1. 查看 `brightdata_sdk_guide.md` 中的详细说明
2. 运行 `test_sdk_simple.py` 进行基础测试
3. 参考官方文档或联系Bright Data技术支持

## 🎯 快速测试

```bash
# 测试SDK是否正常工作
python3 test_sdk_simple.py
```

成功输出示例：
```
✅ 客户端初始化成功
✅ 搜索完成
✅ 解析成功
✅ 找到 2 个zones
```