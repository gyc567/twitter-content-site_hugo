# Twitter账号监控功能使用指南

## 概述

Twitter账号监控功能是本项目的新增功能，可以自动监控指定的Twitter账号，获取他们的最新推文，并生成两种类型的文章：

1. **原始推文汇总文章** - 直接展示推文原始内容
2. **AI分析文章** - 基于推文内容生成的专业分析

## 功能特点

- ✅ 支持监控多个Twitter账号
- ✅ 自动过滤最近24小时的推文
- ✅ 生成双语文章（中文/英文）
- ✅ 集成AI分析功能
- ✅ 自动化运行（每天零晨12点）
- ✅ 遵循md-template.md的文章格式

## 配置步骤

### 1. 设置监控账号

在`.env`文件中配置要监控的Twitter账号：

```bash
# 示例配置
TWT_ACCOUNTS=lookonchain,elonmusk,a16z,VitalikButerin,cz_binance
```

**注意事项**：
- 账号名不需要包含@符号
- 多个账号用英文逗号分隔
- 不要有空格（除非账号名本身包含空格）

### 2. 配置API密钥

确保在GitHub Secrets中设置了以下密钥：

```
TWITTER_API_KEY=your_twitterapi_io_key
OPENAI_API_KEY=your_openai_key
AI_API_KEY=your_backup_ai_key (可选)
AI_BASE_URL=your_backup_ai_url (可选)
TWT_ACCOUNTS=lookonchain,elonmusk,a16z
```

## 生成的文章格式

### 原始推文汇总文章

**文件命名**：
- 中文：`YYYY-MM-DD-monitored-tweets-raw.md`
- 英文：`YYYY-MM-DD-monitored-tweets-raw.md`

**内容结构**：
```markdown
+++
date = '2025-08-17T12:00:00+08:00'
draft = false
title = '今日监控账号推文汇总 - 2025年08月17日'
description = '监控账号的最新推文原始内容汇总'
tags = ['Twitter', '监控', '推文']
categories = ['原始内容']
+++

## 📱 今日监控账号推文汇总

### 🔍 @lookonchain

#### 1. 推文内容
**发布时间**: 2025-08-17T10:00:00Z
**互动数据**: 👍 1000 | 🔄 500 | 💬 200

> 推文原始内容...

---
```

### AI分析文章

**文件命名**：
- 中文：`YYYY-MM-DD-monitored-analysis.md`
- 英文：`YYYY-MM-DD-monitored-analysis.md`

**内容结构**：
```markdown
+++
date = '2025-08-17T12:00:00+08:00'
draft = false
title = 'AI生成的分析标题'
description = '基于监控账号推文的专业市场分析'
tags = ['分析', '市场', 'Twitter']
categories = ['市场分析']
+++

## 市场概览
...

## 重要推文摘要
...

## 深度分析
...
```

## 自动化运行

### GitHub Actions配置

账号监控功能已集成到`.github/workflows/daily-content.yml`中：

```yaml
- name: Monitor accounts and generate content
  env:
    TWITTER_API_KEY: ${{ secrets.TWITTER_API_KEY }}
    OPENAI_API_KEY: ${{ secrets.OPENAI_API_KEY }}
    AI_API_KEY: ${{ secrets.AI_API_KEY }}
    AI_BASE_URL: ${{ secrets.AI_BASE_URL }}
    TWT_ACCOUNTS: ${{ secrets.TWT_ACCOUNTS }}
  run: |
    python scripts/monitor_accounts.py
```

### 运行时间

- **自动运行**：每天UTC时间16:00（中国时间24:00）
- **手动触发**：可以在GitHub Actions页面手动运行

## 本地测试

### 测试脚本

```bash
# 运行完整测试
python scripts/test_monitor_accounts.py

# 直接运行监控脚本
python scripts/monitor_accounts.py
```

### 测试输出示例

```
🚀 开始监控账号推文...
📋 监控账号列表: lookonchain, elonmusk, a16z

🔍 获取监控账号推文...
🔍 获取 @lookonchain 的最新推文...
   找到 10 条推文
🔍 获取 @elonmusk 的最新推文...
   找到 8 条推文

⏰ 过滤最近24小时的推文...
   @lookonchain: 3 条最新推文
   @elonmusk: 2 条最新推文

📝 生成原始推文内容文章...
✅ ZH原始推文文章已发布: content/zh/posts/2025-08-17-monitored-tweets-raw.md
✅ EN原始推文文章已发布: content/en/posts/2025-08-17-monitored-tweets-raw.md

🤖 生成AI分析文章...
🤖 使用主要AI服务生成分析文章...
✅ ZH分析文章已发布: content/zh/posts/2025-08-17-monitored-analysis.md
✅ EN分析文章已发布: content/en/posts/2025-08-17-monitored-analysis.md

✅ 账号监控内容生成完成！
```

## 高级配置

### 修改时间过滤

在`scripts/monitor_accounts.py`中修改：

```python
# 修改过滤时间范围（默认24小时）
recent_tweets = monitor.filter_recent_tweets(tweets, hours=48)  # 改为48小时
```

### 修改推文数量

```python
# 修改每个账号获取的推文数量
tweets = monitor.get_user_tweets(account, max_results=20)  # 默认10条
```

### 自定义文章模板

参考`md-template.md`文件，可以在生成函数中自定义文章格式。

## 故障排除

### 常见问题

1. **获取不到推文**
   - 检查TWITTER_API_KEY是否正确
   - 确认账号名拼写正确
   - 检查API配额是否用完

2. **AI生成失败**
   - 检查OPENAI_API_KEY是否有效
   - 确认API配额充足
   - 查看是否配置了备用AI服务

3. **文章发布失败**
   - 检查content目录权限
   - 确认Hugo目录结构正确

### 调试模式

在脚本中添加更多调试信息：

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## 最佳实践

1. **账号选择**：选择活跃度高、内容质量好的账号
2. **数量控制**：建议监控5-10个账号，避免内容过多
3. **定期检查**：定期检查生成的文章质量
4. **备份配置**：配置备用AI服务以提高稳定性

## 更新日志

- **v1.0** (2025-08-17): 初始版本发布
  - 支持多账号监控
  - 双语文章生成
  - AI分析功能
  - 自动化运行

---

如有问题，请查看项目的Issue页面或提交新的Issue。