#!/usr/bin/env python3
"""
Twitter账号监控脚本
从配置的账号获取最新推文，生成原始内容文章和AI分析文章
"""

import os
import json
import requests
from datetime import datetime, timedelta
from typing import List, Dict
import openai
from pathlib import Path
import re
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# 配置
TWITTER_API_KEY = os.environ.get('TWITTER_API_KEY')
OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')
AI_API_KEY = os.environ.get('AI_API_KEY')
AI_BASE_URL = os.environ.get('AI_BASE_URL')
TWT_ACCOUNTS = os.environ.get('TWT_ACCOUNTS', '').split(',')
CONTENT_DIR = Path(__file__).parent.parent / 'content'

class TwitterAccountMonitor:
    """Twitter账号监控器"""
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.headers = {
            'X-API-Key': api_key,
            'User-Agent': 'TwitterAccountMonitor/1.0'
        }
    
    def get_user_tweets(self, username: str, max_results: int = 10) -> List[Dict]:
        """
        获取指定用户的最新推文
        """
        url = "https://api.twitterapi.io/twitter/user/tweets"
        
        params = {
            'username': username.replace('@', ''),
            'max_results': max_results,
            'exclude': 'retweets,replies'  # 排除转推和回复
        }
        
        try:
            print(f"🔍 获取 @{username} 的最新推文...")
            response = requests.get(url, headers=self.headers, params=params)
            response.raise_for_status()
            data = response.json()
            
            tweets = data.get('tweets', [])
            print(f"   找到 {len(tweets)} 条推文")
            return tweets
            
        except Exception as e:
            print(f"   获取失败: {e}")
            return []
    
    def get_all_monitored_tweets(self, accounts: List[str]) -> Dict[str, List[Dict]]:
        """
        获取所有监控账号的推文
        """
        all_tweets = {}
        
        for account in accounts:
            account = account.strip()
            if account:
                tweets = self.get_user_tweets(account)
                if tweets:
                    all_tweets[account] = tweets
        
        return all_tweets
    
    def filter_recent_tweets(self, tweets: List[Dict], hours: int = 24) -> List[Dict]:
        """
        过滤最近指定小时内的推文
        """
        cutoff_time = datetime.now() - timedelta(hours=hours)
        recent_tweets = []
        
        for tweet in tweets:
            created_at = tweet.get('createdAt', '')
            if created_at:
                try:
                    # 解析推文时间
                    tweet_time = datetime.fromisoformat(created_at.replace('Z', '+00:00'))
                    if tweet_time.replace(tzinfo=None) > cutoff_time:
                        recent_tweets.append(tweet)
                except:
                    # 如果时间解析失败，保留推文
                    recent_tweets.append(tweet)
        
        return recent_tweets

class ContentGenerator:
    """内容生成器"""
    
    def __init__(self, api_key: str, backup_api_key: str = None, backup_base_url: str = None):
        self.primary_client = openai.OpenAI(api_key=api_key) if api_key else None
        self.backup_client = None
        
        # 初始化备用客户端
        if backup_api_key and backup_base_url:
            try:
                self.backup_client = openai.OpenAI(
                    api_key=backup_api_key,
                    base_url=backup_base_url
                )
                print(f"✅ 备用AI服务已配置: {backup_base_url}")
            except Exception as e:
                print(f"⚠️  备用AI服务配置失败: {e}")
                self.backup_client = None
    
    def generate_analysis_article(self, tweets_data: Dict[str, List[Dict]], language: str = 'zh') -> Dict:
        """
        基于推文数据生成分析文章
        """
        if not self.primary_client and not self.backup_client:
            return self._get_fallback_analysis_article(tweets_data, language)
        
        prompt = self._create_analysis_prompt(tweets_data, language)
        
        # 尝试主要AI服务
        if self.primary_client:
            try:
                print("🤖 使用主要AI服务生成分析文章...")
                response = self.primary_client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": "You are a professional cryptocurrency and blockchain analyst."},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.7,
                    max_tokens=2000
                )
                
                content = response.choices[0].message.content
                return self._parse_generated_content(content, language)
                
            except Exception as e:
                print(f"❌ 主要AI服务失败: {e}")
        
        # 尝试备用AI服务
        if self.backup_client:
            try:
                print("🔄 使用备用AI服务生成分析文章...")
                response = self.backup_client.chat.completions.create(
                    model="deepseek-chat",
                    messages=[
                        {"role": "system", "content": "You are a professional cryptocurrency and blockchain analyst."},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.7,
                    max_tokens=2000
                )
                
                content = response.choices[0].message.content
                return self._parse_generated_content(content, language)
                
            except Exception as e:
                print(f"❌ 备用AI服务失败: {e}")
        
        # 使用备用文章
        return self._get_fallback_analysis_article(tweets_data, language)
    
    def _create_analysis_prompt(self, tweets_data: Dict[str, List[Dict]], language: str) -> str:
        """创建分析提示"""
        tweets_summary = []
        for account, tweets in tweets_data.items():
            tweets_summary.append(f"@{account}:")
            for tweet in tweets[:3]:  # 每个账号最多3条推文
                text = tweet.get('text', '')[:200]
                tweets_summary.append(f"  - {text}")
        
        tweets_text = '\n'.join(tweets_summary)
        
        if language == 'zh':
            return f"""
请基于以下监控账号的最新推文，撰写一篇专业的加密货币市场分析文章：

监控账号推文：
{tweets_text}

要求：
1. 文章长度800-1200字
2. 包含市场趋势分析、重要观点提取、投资建议
3. 使用专业的金融分析语言
4. 结构清晰，包含标题、摘要、正文、结论
5. 第一行输出"标题：[文章标题]"
6. 使用Markdown格式

请直接输出文章内容。
"""
        else:
            return f"""
Please write a professional cryptocurrency market analysis article based on the latest tweets from monitored accounts:

Monitored Account Tweets:
{tweets_text}

Requirements:
1. Article length: 800-1200 words
2. Include market trend analysis, key insights extraction, investment advice
3. Use professional financial analysis language
4. Clear structure with title, summary, body, conclusion
5. First line should be "Title: [Article Title]"
6. Use Markdown format

Please output the article directly.
"""
    
    def _parse_generated_content(self, content: str, language: str) -> Dict:
        """解析生成的内容"""
        lines = content.strip().split('\n')
        title_line = lines[0]
        
        if language == 'zh':
            title = title_line.replace('标题：', '').replace('标题:', '').strip()
        else:
            title = title_line.replace('Title:', '').replace('Title：', '').strip()
        
        article_content = '\n'.join(lines[1:]).strip()
        
        return {
            'title': title,
            'content': article_content,
            'language': language
        }
    
    def _get_fallback_analysis_article(self, tweets_data: Dict[str, List[Dict]], language: str) -> Dict:
        """获取备用分析文章"""
        accounts = list(tweets_data.keys())
        
        if language == 'zh':
            title = f"今日加密货币市场观察：{', '.join(['@' + acc for acc in accounts[:3]])}等账号动态分析"
            content = f"""
## 市场概览

今日我们监控了 {', '.join(['@' + acc for acc in accounts])} 等重要账号的最新动态。

## 重要推文摘要

"""
            for account, tweets in tweets_data.items():
                content += f"\n### @{account}\n\n"
                for i, tweet in enumerate(tweets[:3], 1):
                    text = tweet.get('text', '')
                    content += f"{i}. {text}\n\n"
            
            content += """
## 市场分析

基于以上推文内容，当前市场呈现出以下特点：

1. **市场情绪**: 需要进一步观察
2. **技术趋势**: 持续关注相关发展
3. **投资建议**: 保持谨慎，做好风险管理

*本文基于公开推文信息整理，不构成投资建议。*
"""
        else:
            title = f"Today's Crypto Market Watch: Analysis of {', '.join(['@' + acc for acc in accounts[:3]])} and Other Key Accounts"
            content = f"""
## Market Overview

Today we monitored the latest updates from key accounts including {', '.join(['@' + acc for acc in accounts])}.

## Important Tweet Summary

"""
            for account, tweets in tweets_data.items():
                content += f"\n### @{account}\n\n"
                for i, tweet in enumerate(tweets[:3], 1):
                    text = tweet.get('text', '')
                    content += f"{i}. {text}\n\n"
            
            content += """
## Market Analysis

Based on the above tweet content, the current market shows the following characteristics:

1. **Market Sentiment**: Requires further observation
2. **Technical Trends**: Continue monitoring related developments  
3. **Investment Advice**: Stay cautious and manage risks properly

*This article is compiled from public tweet information and does not constitute investment advice.*
"""
        
        return {
            'title': title,
            'content': content,
            'language': language
        }

class HugoPublisher:
    """Hugo发布器"""
    
    def __init__(self, content_dir: Path):
        self.content_dir = content_dir
        self.ensure_directories()
    
    def ensure_directories(self):
        """确保必要的目录存在"""
        for lang in ['en', 'zh']:
            posts_dir = self.content_dir / lang / 'posts'
            posts_dir.mkdir(parents=True, exist_ok=True)
    
    def publish_raw_tweets_article(self, tweets_data: Dict[str, List[Dict]], language: str):
        """发布原始推文内容文章"""
        date = datetime.now()
        
        if language == 'zh':
            title = f"今日监控账号推文汇总 - {date.strftime('%Y年%m月%d日')}"
            filename = f"{date.strftime('%Y-%m-%d')}-monitored-tweets-raw.md"
        else:
            title = f"Daily Monitored Account Tweets Summary - {date.strftime('%B %d, %Y')}"
            filename = f"{date.strftime('%Y-%m-%d')}-monitored-tweets-raw.md"
        
        filepath = self.content_dir / language / 'posts' / filename
        
        # 创建前置内容
        frontmatter = f"""+++
date = '{date.strftime('%Y-%m-%dT%H:%M:%S+08:00')}'
draft = false
title = '{title}'
description = '{"监控账号的最新推文原始内容汇总" if language == "zh" else "Raw content summary of latest tweets from monitored accounts"}'
tags = ['Twitter', '{"监控" if language == "zh" else "monitoring"}', '{"推文" if language == "zh" else "tweets"}']
categories = ['{"原始内容" if language == "zh" else "Raw Content"}']
+++

"""
        
        # 生成内容
        if language == 'zh':
            content = f"""## 📱 今日监控账号推文汇总

> 本文汇总了我们监控的重要Twitter账号在 {date.strftime('%Y年%m月%d日')} 的最新推文内容。

"""
        else:
            content = f"""## 📱 Daily Monitored Account Tweets Summary

> This article summarizes the latest tweets from important Twitter accounts we monitor on {date.strftime('%B %d, %Y')}.

"""
        
        # 添加每个账号的推文
        for account, tweets in tweets_data.items():
            if language == 'zh':
                content += f"\n### 🔍 @{account}\n\n"
            else:
                content += f"\n### 🔍 @{account}\n\n"
            
            for i, tweet in enumerate(tweets, 1):
                text = tweet.get('text', '')
                created_at = tweet.get('createdAt', '')
                like_count = tweet.get('likeCount', 0)
                retweet_count = tweet.get('retweetCount', 0)
                reply_count = tweet.get('replyCount', 0)
                
                content += f"""#### {i}. 推文内容

**发布时间**: {created_at}  
**互动数据**: 👍 {like_count} | 🔄 {retweet_count} | 💬 {reply_count}

> {text}

---

"""
        
        # 添加免责声明
        if language == 'zh':
            content += """
## ⚠️ 免责声明

本文仅汇总公开的Twitter推文内容，不代表本站观点，不构成任何投资建议。请读者自行判断信息的准确性和可靠性。

---

## 📞 关于作者

**ERIC** - 《区块链核心技术与应用》作者之一，前火币机构事业部|矿池技术主管，比特财商|Nxt Venture Capital 创始人

### 🔗 联系方式与平台

- **📧 邮箱**: [gyc567@gmail.com](mailto:gyc567@gmail.com)
- **🐦 Twitter**: [@EricBlock2100](https://twitter.com/EricBlock2100)
- **💬 微信**: 360369487
- **📱 Telegram**: [https://t.me/fatoshi_block](https://t.me/fatoshi_block)
- **📢 Telegram频道**: [https://t.me/cryptochanneleric](https://t.me/cryptochanneleric)
- **👥 加密情报TG群**: [https://t.me/btcgogopen](https://t.me/btcgogopen)
- **🎥 YouTube频道**: [https://www.youtube.com/@0XBitFinance](https://www.youtube.com/@0XBitFinance)

### 🌐 相关平台

- **📊 加密货币信息聚合网站**: [https://www.smartwallex.com/](https://www.smartwallex.com/)
- **📖 公众号**: 比特财商

*欢迎关注我的各个平台，获取最新的加密货币市场分析和投资洞察！*
"""
        else:
            content += """
## ⚠️ Disclaimer

This article only summarizes public Twitter tweet content and does not represent the views of this site or constitute any investment advice. Readers should judge the accuracy and reliability of the information themselves.

---

## 📞 About the Author

**ERIC** - Co-author of "Blockchain Core Technology and Applications", Former Huobi Institutional Business Department | Mining Pool Technical Director, Founder of BitCai Business | Nxt Venture Capital

### 🔗 Contact Information & Platforms

- **📧 Email**: [gyc567@gmail.com](mailto:gyc567@gmail.com)
- **🐦 Twitter**: [@EricBlock2100](https://twitter.com/EricBlock2100)
- **💬 WeChat**: 360369487
- **📱 Telegram**: [https://t.me/fatoshi_block](https://t.me/fatoshi_block)
- **📢 Telegram Channel**: [https://t.me/cryptochanneleric](https://t.me/cryptochanneleric)
- **👥 Crypto Intelligence TG Group**: [https://t.me/btcgogopen](https://t.me/btcgogopen)
- **🎥 YouTube Channel**: [https://www.youtube.com/@0XBitFinance](https://www.youtube.com/@0XBitFinance)

### 🌐 Related Platforms

- **📊 Cryptocurrency Information Aggregation Website**: [https://www.smartwallex.com/](https://www.smartwallex.com/)
- **📖 WeChat Official Account**: BitCai Business

*Follow my platforms for the latest cryptocurrency market analysis and investment insights!*
"""
        
        # 写入文件
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(frontmatter)
            f.write(content)
        
        print(f"✅ {language.upper()}原始推文文章已发布: {filepath}")
    
    def publish_analysis_article(self, article: Dict):
        """发布分析文章"""
        date = datetime.now()
        language = article['language']
        
        # 创建文件名
        if language == 'zh':
            filename = f"{date.strftime('%Y-%m-%d')}-monitored-analysis.md"
        else:
            filename = f"{date.strftime('%Y-%m-%d')}-monitored-analysis.md"
        
        filepath = self.content_dir / language / 'posts' / filename
        
        # 创建前置内容
        frontmatter = f"""+++
date = '{date.strftime('%Y-%m-%dT%H:%M:%S+08:00')}'
draft = false
title = '{article["title"]}'
description = '{"基于监控账号推文的专业市场分析" if language == "zh" else "Professional market analysis based on monitored account tweets"}'
tags = ['{"分析" if language == "zh" else "analysis"}', '{"市场" if language == "zh" else "market"}', 'Twitter']
categories = ['{"市场分析" if language == "zh" else "Market Analysis"}']
+++

"""
        
        # 添加作者信息到文章末尾
        content = article['content']
        
        if language == 'zh':
            content += """

---

## 📞 关于作者

**ERIC** - 《区块链核心技术与应用》作者之一，前火币机构事业部|矿池技术主管，比特财商|Nxt Venture Capital 创始人

### 🔗 联系方式与平台

- **📧 邮箱**: [gyc567@gmail.com](mailto:gyc567@gmail.com)
- **🐦 Twitter**: [@EricBlock2100](https://twitter.com/EricBlock2100)
- **💬 微信**: 360369487
- **📱 Telegram**: [https://t.me/fatoshi_block](https://t.me/fatoshi_block)
- **📢 Telegram频道**: [https://t.me/cryptochanneleric](https://t.me/cryptochanneleric)
- **👥 加密情报TG群**: [https://t.me/btcgogopen](https://t.me/btcgogopen)
- **🎥 YouTube频道**: [https://www.youtube.com/@0XBitFinance](https://www.youtube.com/@0XBitFinance)

### 🌐 相关平台

- **📊 加密货币信息聚合网站**: [https://www.smartwallex.com/](https://www.smartwallex.com/)
- **📖 公众号**: 比特财商

*欢迎关注我的各个平台，获取最新的加密货币市场分析和投资洞察！*
"""
        else:
            content += """

---

## 📞 About the Author

**ERIC** - Co-author of "Blockchain Core Technology and Applications", Former Huobi Institutional Business Department | Mining Pool Technical Director, Founder of BitCai Business | Nxt Venture Capital

### 🔗 Contact Information & Platforms

- **📧 Email**: [gyc567@gmail.com](mailto:gyc567@gmail.com)
- **🐦 Twitter**: [@EricBlock2100](https://twitter.com/EricBlock2100)
- **💬 WeChat**: 360369487
- **📱 Telegram**: [https://t.me/fatoshi_block](https://t.me/fatoshi_block)
- **📢 Telegram Channel**: [https://t.me/cryptochanneleric](https://t.me/cryptochanneleric)
- **👥 Crypto Intelligence TG Group**: [https://t.me/btcgogopen](https://t.me/btcgogopen)
- **🎥 YouTube Channel**: [https://www.youtube.com/@0XBitFinance](https://www.youtube.com/@0XBitFinance)

### 🌐 Related Platforms

- **📊 Cryptocurrency Information Aggregation Website**: [https://www.smartwallex.com/](https://www.smartwallex.com/)
- **📖 WeChat Official Account**: BitCai Business

*Follow my platforms for the latest cryptocurrency market analysis and investment insights!*
"""
        
        # 写入文件
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(frontmatter)
            f.write(content)
        
        print(f"✅ {language.upper()}分析文章已发布: {filepath}")

def main():
    """主函数"""
    print("🚀 开始监控账号推文...")
    
    # 检查环境变量
    if not TWITTER_API_KEY:
        print("❌ 错误：请设置TWITTER_API_KEY环境变量")
        return
    
    if not TWT_ACCOUNTS or TWT_ACCOUNTS == ['']:
        print("❌ 错误：请在.env文件中设置TWT_ACCOUNTS")
        return
    
    print(f"📋 监控账号列表: {', '.join(TWT_ACCOUNTS)}")
    
    # 初始化组件
    monitor = TwitterAccountMonitor(TWITTER_API_KEY)
    generator = ContentGenerator(
        api_key=OPENAI_API_KEY,
        backup_api_key=AI_API_KEY,
        backup_base_url=AI_BASE_URL
    )
    publisher = HugoPublisher(CONTENT_DIR)
    
    # 获取所有监控账号的推文
    print("\n🔍 获取监控账号推文...")
    all_tweets = monitor.get_all_monitored_tweets(TWT_ACCOUNTS)
    
    if not all_tweets:
        print("❌ 未能获取到任何推文")
        return
    
    # 过滤最近24小时的推文
    print("\n⏰ 过滤最近24小时的推文...")
    recent_tweets = {}
    for account, tweets in all_tweets.items():
        recent = monitor.filter_recent_tweets(tweets, hours=24)
        if recent:
            recent_tweets[account] = recent
            print(f"   @{account}: {len(recent)} 条最新推文")
    
    if not recent_tweets:
        print("⚠️  没有找到最近24小时的推文")
        # 使用所有推文
        recent_tweets = all_tweets
        print("🔄 使用所有获取到的推文")
    
    # 发布原始推文内容文章（双语）
    print("\n📝 生成原始推文内容文章...")
    publisher.publish_raw_tweets_article(recent_tweets, 'zh')
    publisher.publish_raw_tweets_article(recent_tweets, 'en')
    
    # 生成并发布分析文章（双语）
    print("\n🤖 生成AI分析文章...")
    
    # 中文分析文章
    zh_analysis = generator.generate_analysis_article(recent_tweets, 'zh')
    publisher.publish_analysis_article(zh_analysis)
    
    # 英文分析文章
    en_analysis = generator.generate_analysis_article(recent_tweets, 'en')
    publisher.publish_analysis_article(en_analysis)
    
    print("\n✅ 账号监控内容生成完成！")

if __name__ == "__main__":
    main()