/**
 * Bright Data MCP API Node.js 实战示例
 * 功能：展示如何在Node.js环境中集成MCP API
 */

const axios = require('axios');
const fs = require('fs').promises;
const path = require('path');

class BrightDataClient {
    constructor(apiToken) {
        this.apiToken = apiToken;
        this.baseURL = 'https://api.brightdata.com/mcp/v1';
        this.axiosInstance = axios.create({
            baseURL: this.baseURL,
            headers: {
                'Authorization': `Bearer ${apiToken}`,
                'Content-Type': 'application/json'
            },
            timeout: 30000
        });
    }

    /**
     * 抓取Google搜索结果 - Node.js异步实现
     */
    async scrapeGoogleSearch(query, options = {}) {
        const { 
            numResults = 10, 
            language = 'en',
            country = 'us',
            useBrowser = true 
        } = options;

        const searchUrl = `https://www.google.com/search?q=${encodeURIComponent(query)}&num=${numResults}&hl=${language}&gl=${country}`;
        
        const requestBody = {
            url: searchUrl,
            browser: useBrowser,
            unlocker: true,
            pro: 1,
            wait_for: {
                selector: 'div#search',
                timeout: 10000
            },
            extract: {
                results: {
                    selector: 'div.g',
                    multiple: true,
                    fields: {
                        title: 'h3',
                        url: {
                            selector: 'a',
                            attribute: 'href'
                        },
                        description: 'div.VwiC3b',
                        date: 'span.f'
                    }
                },
                relatedSearches: {
                    selector: 'div.k8XOCe',
                    multiple: true,
                    fields: {
                        query: 'div.s75CSd'
                    }
                },
                totalResults: '#result-stats'
            }
        };

        try {
            console.log(`[${new Date().toISOString()}] 开始抓取: "${query}"`);
            const response = await this.axiosInstance.post('/extract', requestBody);
            
            return {
                success: true,
                data: response.data,
                query: query,
                timestamp: new Date().toISOString()
            };
        } catch (error) {
            console.error(`[错误] 抓取失败:`, error.message);
            return {
                success: false,
                error: error.message,
                query: query,
                timestamp: new Date().toISOString()
            };
        }
    }

    /**
     * 批量抓取多个搜索查询
     */
    async batchScrape(queries, concurrency = 3) {
        const results = [];
        const batches = [];
        
        // 将查询分批处理
        for (let i = 0; i < queries.length; i += concurrency) {
            batches.push(queries.slice(i, i + concurrency));
        }

        for (const batch of batches) {
            const batchPromises = batch.map(query => 
                this.scrapeGoogleSearch(query)
                    .then(result => ({ query, result }))
            );
            
            const batchResults = await Promise.all(batchPromises);
            results.push(...batchResults);
            
            // 避免请求过快
            if (batches.indexOf(batch) < batches.length - 1) {
                await new Promise(resolve => setTimeout(resolve, 2000));
            }
        }

        return results;
    }

    /**
     * 处理动态内容 - 高级示例
     */
    async scrapeDynamicContent(url, customConfig = {}) {
        const defaultConfig = {
            browser: true,
            unlocker: true,
            pro: 1,
            viewport: {
                width: 1920,
                height: 1080
            },
            wait_for: {
                selector: 'body',
                timeout: 30000
            },
            execute_js: [
                // 滚动页面加载更多内容
                `
                const scrollToBottom = async () => {
                    const distance = 100;
                    const delay = 100;
                    const timer = setInterval(() => {
                        document.scrollingElement.scrollBy(0, distance);
                        if (document.scrollingElement.scrollTop + window.innerHeight >= document.scrollingElement.scrollHeight) {
                            clearInterval(timer);
                        }
                    }, delay);
                    await new Promise(resolve => setTimeout(resolve, 3000));
                };
                await scrollToBottom();
                `,
                // 点击"加载更多"按钮（如果存在）
                `
                const loadMoreButton = document.querySelector('.load-more-button');
                if (loadMoreButton) {
                    loadMoreButton.click();
                    await new Promise(resolve => setTimeout(resolve, 2000));
                }
                `
            ]
        };

        const requestBody = {
            url,
            ...defaultConfig,
            ...customConfig
        };

        try {
            const response = await this.axiosInstance.post('/extract', requestBody);
            return response.data;
        } catch (error) {
            throw new Error(`动态内容抓取失败: ${error.message}`);
        }
    }
}

/**
 * Express.js API端点示例
 */
const express = require('express');
const app = express();
app.use(express.json());

// 初始化Bright Data客户端
const brightDataClient = new BrightDataClient(process.env.BRIGHTDATA_API_TOKEN);

// API端点：搜索数据
app.post('/api/search', async (req, res) => {
    const { query, options } = req.body;
    
    if (!query) {
        return res.status(400).json({ error: '缺少搜索查询参数' });
    }

    try {
        const result = await brightDataClient.scrapeGoogleSearch(query, options);
        res.json(result);
    } catch (error) {
        res.status(500).json({ error: error.message });
    }
});

// API端点：批量搜索
app.post('/api/batch-search', async (req, res) => {
    const { queries } = req.body;
    
    if (!Array.isArray(queries) || queries.length === 0) {
        return res.status(400).json({ error: '请提供查询数组' });
    }

    try {
        const results = await brightDataClient.batchScrape(queries);
        res.json({ results });
    } catch (error) {
        res.status(500).json({ error: error.message });
    }
});

/**
 * 与自动化工具集成示例
 */

// 1. GitHub Actions 集成
const githubActionsWorkflow = `
name: Daily Search Scraping

on:
  schedule:
    - cron: '0 9 * * *'  # 每天早上9点运行
  workflow_dispatch:

jobs:
  scrape:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      
      - name: Setup Node.js
        uses: actions/setup-node@v2
        with:
          node-version: '16'
      
      - name: Install dependencies
        run: npm install
      
      - name: Run scraping script
        env:
          BRIGHTDATA_API_TOKEN: \${{ secrets.BRIGHTDATA_API_TOKEN }}
        run: node scrape-daily.js
      
      - name: Upload results
        uses: actions/upload-artifact@v2
        with:
          name: scraping-results
          path: results/
`;

// 2. PM2 生态系统配置（用于生产部署）
const pm2Config = {
    apps: [{
        name: 'brightdata-scraper',
        script: './server.js',
        instances: 2,
        exec_mode: 'cluster',
        env: {
            NODE_ENV: 'production',
            BRIGHTDATA_API_TOKEN: 'your-api-token'
        },
        cron_restart: '0 */6 * * *',  // 每6小时重启
        error_file: './logs/err.log',
        out_file: './logs/out.log',
        log_file: './logs/combined.log',
        time: true
    }]
};

// 3. Docker容器化部署
const dockerfile = `
FROM node:16-alpine

WORKDIR /app

COPY package*.json ./
RUN npm ci --only=production

COPY . .

ENV BRIGHTDATA_API_TOKEN=""
ENV PORT=3000

EXPOSE 3000

CMD ["node", "server.js"]
`;

// 4. Kubernetes CronJob配置
const k8sCronJob = `
apiVersion: batch/v1
kind: CronJob
metadata:
  name: brightdata-scraper
spec:
  schedule: "0 */4 * * *"  # 每4小时运行
  jobTemplate:
    spec:
      template:
        spec:
          containers:
          - name: scraper
            image: your-registry/brightdata-scraper:latest
            env:
            - name: BRIGHTDATA_API_TOKEN
              valueFrom:
                secretKeyRef:
                  name: brightdata-secret
                  key: api-token
          restartPolicy: OnFailure
`;

/**
 * 数据处理和存储示例
 */
class DataProcessor {
    /**
     * 将搜索结果保存到文件
     */
    static async saveToFile(results, filename) {
        const outputDir = path.join(__dirname, 'results');
        await fs.mkdir(outputDir, { recursive: true });
        
        const filepath = path.join(outputDir, filename);
        await fs.writeFile(filepath, JSON.stringify(results, null, 2));
        
        console.log(`结果已保存到: ${filepath}`);
        return filepath;
    }

    /**
     * 将结果保存到数据库（示例使用MongoDB）
     */
    static async saveToMongoDB(results, mongoClient) {
        const db = mongoClient.db('brightdata');
        const collection = db.collection('search_results');
        
        const documents = results.map(({ query, result }) => ({
            query,
            results: result.data?.extract?.results || [],
            success: result.success,
            timestamp: new Date(result.timestamp),
            metadata: {
                totalResults: result.data?.extract?.totalResults,
                relatedSearches: result.data?.extract?.relatedSearches
            }
        }));

        const insertResult = await collection.insertMany(documents);
        console.log(`插入了 ${insertResult.insertedCount} 条记录到MongoDB`);
        
        return insertResult;
    }

    /**
     * 导出为CSV格式
     */
    static async exportToCSV(results, filename) {
        const csvRows = ['Query,Title,URL,Description'];
        
        results.forEach(({ query, result }) => {
            if (result.success && result.data?.extract?.results) {
                result.data.extract.results.forEach(item => {
                    const row = [
                        query,
                        item.title?.replace(/,/g, ';'),
                        item.url,
                        item.description?.replace(/,/g, ';').substring(0, 200)
                    ].join(',');
                    csvRows.push(row);
                });
            }
        });

        const csvContent = csvRows.join('\n');
        const outputPath = path.join(__dirname, 'results', filename);
        await fs.writeFile(outputPath, csvContent, 'utf8');
        
        return outputPath;
    }
}

/**
 * 主执行函数
 */
async function main() {
    // 设置API令牌
    const API_TOKEN = process.env.BRIGHTDATA_API_TOKEN || 'your-api-token-here';
    const client = new BrightDataClient(API_TOKEN);

    // 示例1：单个搜索
    console.log('=== 示例1：单个搜索 ===');
    const singleResult = await client.scrapeGoogleSearch('Node.js web scraping 2024');
    console.log(`获取到 ${singleResult.data?.extract?.results?.length || 0} 个结果`);

    // 示例2：批量搜索
    console.log('\n=== 示例2：批量搜索 ===');
    const queries = [
        'React best practices 2024',
        'Vue.js vs React performance',
        'Next.js tutorial'
    ];
    const batchResults = await client.batchScrape(queries, 2);
    
    // 保存结果
    const timestamp = new Date().toISOString().replace(/:/g, '-');
    await DataProcessor.saveToFile(batchResults, `results_${timestamp}.json`);
    await DataProcessor.exportToCSV(batchResults, `results_${timestamp}.csv`);

    // 示例3：动态内容抓取
    console.log('\n=== 示例3：动态内容抓取 ===');
    try {
        const dynamicResult = await client.scrapeDynamicContent(
            'https://example.com/infinite-scroll',
            {
                extract: {
                    items: {
                        selector: '.item',
                        multiple: true,
                        fields: {
                            title: '.item-title',
                            price: '.item-price',
                            image: {
                                selector: 'img',
                                attribute: 'src'
                            }
                        }
                    }
                }
            }
        );
        console.log('动态内容抓取成功');
    } catch (error) {
        console.error('动态内容抓取失败:', error.message);
    }
}

// 如果直接运行此文件
if (require.main === module) {
    main().catch(console.error);
}

// 导出模块
module.exports = {
    BrightDataClient,
    DataProcessor,
    app
};