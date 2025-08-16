# Twitter Content Site - 自动化内容网站

这是一个基于Hugo框架的自动化内容网站，每天自动从Twitter抓取热门话题，使用AI生成双语文章（简体中文和英语），并通过Monetag广告实现变现。

## 功能特点

- 🔥 **自动抓取Twitter热门话题**：每天自动获取Twitter上最热门的3个话题
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

- `TWITTER_BEARER_TOKEN`：Twitter API Bearer Token
- `OPENAI_API_KEY`：OpenAI API密钥

获取方式：
- Twitter API：访问 https://developer.twitter.com/
- OpenAI API：访问 https://platform.openai.com/

### 4. 配置Monetag

1. 注册Monetag账号：https://monetag.com/
2. 获取您的Publisher ID
3. 在`hugo.toml`中替换`YOUR_MONETAG_ID`

### 5. 本地测试

```bash
# 设置环境变量
export TWITTER_BEARER_TOKEN="your_token"
export OPENAI_API_KEY="your_key"

# 运行内容生成脚本
python scripts/generate_content.py

# 启动Hugo服务器
hugo server -D
```

访问 http://localhost:1313 查看网站

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
│   └── generate_content.py     # 内容生成脚本
├── themes/
│   └── paper/                  # Hugo主题
├── hugo.toml                   # Hugo配置
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
