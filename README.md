# Twitter Content Site - 自动化内容网站

这是一个基于Hugo框架的自动化内容网站，每天自动从Twitter抓取热门话题，使用AI生成双语文章（简体中文和英语），并通过Monetag广告实现变现。

## 功能特点

- 🔥 **自动抓取Twitter热门话题**：每天自动获取Twitter上最热门的3个话题
- 👥 **账号监控功能**：监控指定Twitter账号的最新推文，生成原始内容和AI分析文章
- 🛡️ **多重API兜底**：支持TwitterAPI.io + Twikit双重保障，确保服务稳定性
- 🤖 **AI内容生成**：使用OpenAI自动生成高质量文章
- 🌍 **双语支持**：支持简体中文和美国英语
- 💰 **广告变现**：集成Monetag广告系统
- ⚡ **自动化发布**：通过GitHub Actions每天自动更新
- 📱 **响应式设计**：适配各种设备

## 技术栈

- **静态网站生成器**：Hugo
- **内容生成**：Python + OpenAI API
- **数据源**：Twitter API v2
- **自动化**：GitHub Actions
- **部署**：GitHub Pages / Netlify / Vercel
- **广告**：Monetag

## 快速开始

### 1. 克隆仓库

```bash
git clone https://github.com/yourusername/twitter-content-site.git
cd twitter-content-site
```

### 2. 安装依赖

```bash
# 安装Hugo
brew install hugo  # macOS
# 或查看 https://gohugo.io/installation/

# 安装Python依赖
pip install -r requirements.txt
```

### 3. 配置API密钥

在GitHub仓库设置中添加以下Secrets：

**Twitter API配置（至少配置一种）：**
- `TWITTER_API_KEY`：TwitterAPI.io API密钥（主要方案）
- `TWITTER_USERNAME`：Twitter用户名（兜底方案）
- `TWITTER_PASSWORD`：Twitter密码（兜底方案）
- `TWITTER_EMAIL`：Twitter邮箱（兜底方案）

**AI服务配置：**
- `OPENAI_API_KEY`：OpenAI API密钥
- `AI_API_KEY`：备用AI服务API密钥（可选）
- `AI_BASE_URL`：备用AI服务地址（可选）

**监控配置：**
- `TWT_ACCOUNTS`：要监控的Twitter账号列表，用逗号分隔（如：elonmusk,a16z,lookonchain）

获取方式：
- TwitterAPI.io：访问 https://twitterapi.io/
- OpenAI API：访问 https://platform.openai.com/
- Twikit：使用真实的Twitter账号凭据

### 4. 配置Monetag

1. 注册Monetag账号：https://monetag.com/
2. 获取您的Publisher ID
3. 在`hugo.toml`中替换`YOUR_MONETAG_ID`

### 5. 本地测试

```bash
# 复制环境变量配置文件
cp .env.example .env

# 编辑.env文件，填入您的API密钥
# TWITTER_API_KEY=your_twitter_api_key
# OPENAI_API_KEY=your_openai_api_key
# TWT_ACCOUNTS=lookonchain,elonmusk,a16z

# 测试账号监控功能
python scripts/test_monitor_accounts.py

# 运行热门话题内容生成脚本
python scripts/generate_content.py

# 运行账号监控脚本
python scripts/monitor_accounts.py

# 启动Hugo服务器
hugo server -D
```

访问 http://localhost:1313 查看网站

## 新功能：账号监控

### 功能说明

账号监控功能可以：
1. **监控指定Twitter账号**：从`.env`文件中的`TWT_ACCOUNTS`配置获取要监控的账号列表
2. **生成原始推文文章**：将监控账号的最新推文原始内容整理成文章
3. **生成AI分析文章**：基于推文内容使用AI生成专业的市场分析文章
4. **双语支持**：同时生成中文和英文版本的文章
5. **自动化运行**：每天零晨12点通过GitHub Actions自动执行

### 配置监控账号

在`.env`文件中设置要监控的Twitter账号：

```bash
# 多个账号用逗号分隔，不需要@符号
TWT_ACCOUNTS=lookonchain,elonmusk,a16z,VitalikButerin,cz_binance
```

### 生成的文章类型

1. **原始推文汇总文章**：
   - 文件名格式：`YYYY-MM-DD-monitored-tweets-raw.md`
   - 包含所有监控账号的最新推文原始内容
   - 显示推文的互动数据（点赞、转发、评论）

2. **AI分析文章**：
   - 文件名格式：`YYYY-MM-DD-monitored-analysis.md`
   - 基于推文内容生成的专业市场分析
   - 包含趋势分析、投资建议等内容

### 手动运行

```bash
# 运行账号监控脚本
python scripts/monitor_accounts.py

# 测试功能
python scripts/test_monitor_accounts.py
```

### 时间过滤

- 默认只处理最近24小时内的推文
- 如果没有最近推文，会使用所有获取到的推文
- 可以在脚本中修改时间范围

## Twitter API兜底方案

### 双重保障机制

本项目实现了Twitter API的双重保障机制：

1. **主要方案：TwitterAPI.io**
   - 商业API服务，稳定可靠
   - 需要付费API密钥
   - 速度快，限制少

2. **兜底方案：Twikit**
   - 开源Python库，模拟浏览器行为
   - 使用真实Twitter账号登录
   - 免费使用，但可能受到限制

### 工作原理

```
尝试TwitterAPI.io → 失败 → 自动切换到Twikit → 成功获取数据
```

### 配置方式

**方案一：仅使用TwitterAPI.io**
```bash
TWITTER_API_KEY=your_api_key
```

**方案二：仅使用Twikit**
```bash
TWITTER_USERNAME=your_username
TWITTER_PASSWORD=your_password
TWITTER_EMAIL=your_email
```

**方案三：双重保障（推荐）**
```bash
# 主要方案
TWITTER_API_KEY=your_api_key

# 兜底方案
TWITTER_USERNAME=your_username
TWITTER_PASSWORD=your_password
TWITTER_EMAIL=your_email
```

### 测试兜底功能

```bash
# 测试所有Twitter API方案
python scripts/test_twitter_fallback.py
```

### 注意事项

- Twikit使用真实账号登录，请确保账号安全
- 建议使用专门的测试账号，避免影响主账号
- Twikit可能受到Twitter的反爬虫限制
- 建议优先配置TwitterAPI.io，Twikit作为备用

## 部署

### GitHub Pages部署

1. 在GitHub仓库设置中启用GitHub Pages
2. 选择`gh-pages`分支作为源
3. GitHub Actions会自动构建和部署

### 自定义域名

1. 在`.github/workflows/daily-content.yml`中更新`cname`字段
2. 在域名提供商处配置DNS指向GitHub Pages

## 自定义

### 修改发布时间

编辑`.github/workflows/daily-content.yml`中的cron表达式：

```yaml
schedule:
  - cron: '0 16 * * *'  # UTC时间16:00（中国时间24:00）
```

### 修改文章数量

编辑`scripts/generate_content.py`中的：

```python
return trends[:3]  # 修改数字以改变每日文章数量
```

### 更换主题

```bash
# 添加新主题
git submodule add https://github.com/theme-author/theme-name themes/theme-name

# 更新hugo.toml
theme = 'theme-name'
```

## 项目结构

```
twitter-content-site/
├── .github/
│   └── workflows/
│       └── daily-content.yml    # GitHub Actions工作流
├── content/                     # 内容目录
│   ├── en/                     # 英文内容
│   └── zh/                     # 中文内容
├── layouts/                     # 自定义布局
│   └── partials/
│       ├── monetag.html        # Monetag广告集成
│       └── ads.html            # 广告展示组件
├── scripts/
│   ├── generate_content.py     # 热门话题内容生成脚本
│   ├── monitor_accounts.py     # 账号监控脚本
│   └── test_monitor_accounts.py # 账号监控测试脚本
├── themes/
│   └── paper/                  # Hugo主题
├── .env.example                # 环境变量配置示例
├── hugo.toml                   # Hugo配置
├── md-template.md              # 文章模板参考
├── requirements.txt            # Python依赖
└── README.md                   # 项目文档
```

## 注意事项

1. **API限制**：
   - Twitter API有速率限制，请确保不要过度使用
   - OpenAI API按使用量计费，请监控使用情况

2. **内容质量**：
   - 定期检查生成的内容质量
   - 必要时手动调整或删除不当内容

3. **法律合规**：
   - 遵守Twitter的服务条款
   - 确保内容符合当地法律法规
   - 合理使用他人推文内容

4. **广告合规**：
   - 遵守Monetag的发布政策
   - 确保广告展示符合用户体验要求

## 故障排除

### GitHub Actions失败

1. 检查Secrets是否正确配置
2. 查看Actions日志了解详细错误
3. 确保API密钥有效且未过期

### 内容生成失败

1. 验证API密钥
2. 检查API配额
3. 查看`scripts/generate_content.py`日志

### Hugo构建失败

1. 确保主题正确安装
2. 检查Markdown文件格式
3. 运行`hugo --verbose`查看详细错误

## 贡献

欢迎提交Issue和Pull Request！

## 许可证

MIT License

## 联系方式

如有问题，请提交Issue或联系项目维护者。

---

**免责声明**：本项目仅用于学习和研究目的。使用者需自行承担使用本项目的所有风险和责任。
