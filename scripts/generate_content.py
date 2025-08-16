#!/usr/bin/env python3
"""
Twitter热门内容抓取和文章生成脚本
每天自动抓取Twitter热门话题，使用AI生成双语文章
"""

import os
import json
import requests
from datetime import datetime
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
CONTENT_DIR = Path(__file__).parent.parent / 'content'

# 初始化OpenAI
openai.api_key = OPENAI_API_KEY

class TwitterTrendFetcher:
    """Twitter趋势获取器"""
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.headers = {
            'X-API-Key': api_key,
            'User-Agent': 'TwitterTrendBot/1.0'
        }
    
    def get_crypto_trending_topics(self, max_results: int = 100) -> List[Dict]:
        """
        获取区块链和加密货币相关的热门话题
        """
        url = "https://api.twitterapi.io/twitter/tweet/advanced_search"
        
        # 区块链和加密货币相关的搜索关键词
        crypto_queries = [
            "bitcoin OR BTC OR 比特币",
            "ethereum OR ETH OR 以太坊", 
            "blockchain OR 区块链",
            "cryptocurrency OR 加密货币",
            "DeFi OR 去中心化金融",
            "NFT OR 非同质化代币",
            "Web3 OR 元宇宙"
        ]
        
        all_tweets = []
        
        for query in crypto_queries:
            params = {
                'query': query,
                'max_results': 20,  # 每个查询获取20条
                'sort_order': 'relevancy'
            }
            
            try:
                print(f"🔍 搜索关键词: {query}")
                response = requests.get(url, headers=self.headers, params=params)
                response.raise_for_status()
                data = response.json()
                
                tweets = data.get('tweets', [])
                print(f"   找到 {len(tweets)} 条相关推文")
                all_tweets.extend(tweets)
                
            except Exception as e:
                print(f"   搜索失败: {e}")
                continue
        
        print(f"📊 总共收集到 {len(all_tweets)} 条加密货币相关推文")
        return self._get_top_tweets_by_engagement(all_tweets)
        
        return all_tweets
    
    def _get_top_tweets_by_engagement(self, tweets: List[Dict]) -> List[Dict]:
        """
        根据点赞和转发数量选择最热门的推文
        """
        if not tweets:
            print("⚠️  没有推文数据")
            return []
        
        # 计算每条推文的参与度分数
        scored_tweets = []
        for tweet in tweets:
            # 获取互动数据
            like_count = tweet.get('likeCount', 0)
            retweet_count = tweet.get('retweetCount', 0)
            reply_count = tweet.get('replyCount', 0)
            
            # 计算参与度分数 (点赞 + 转发*2 + 回复*1.5)
            engagement_score = like_count + (retweet_count * 2) + (reply_count * 1.5)
            
            scored_tweets.append({
                'tweet': tweet,
                'engagement_score': engagement_score,
                'like_count': like_count,
                'retweet_count': retweet_count,
                'reply_count': reply_count
            })
        
        # 按参与度分数排序
        scored_tweets.sort(key=lambda x: x['engagement_score'], reverse=True)
        
        # 返回前3个最热门的推文
        top_tweets = scored_tweets[:3]
        
        print("🏆 最热门的3条推文:")
        for i, item in enumerate(top_tweets, 1):
            tweet = item['tweet']
            text = tweet.get('text', '')[:100]
            print(f"   {i}. 👍{item['like_count']} 🔄{item['retweet_count']} 💬{item['reply_count']} - {text}...")
        
        return [item['tweet'] for item in top_tweets]
    
    def _analyze_trends(self, tweets: List[Dict]) -> List[Dict]:
        """分析推文提取趋势"""
        topic_scores = {}
        
        for tweet in tweets:
            # 提取话题标签和上下文
            text = tweet.get('text', '')
            
            # 根据新API结构获取互动数据
            # 如果API返回的数据结构不同，需要相应调整
            metrics = tweet.get('public_metrics', {})
            if not metrics:
                # 尝试其他可能的字段名
                metrics = {
                    'retweet_count': tweet.get('retweet_count', 0),
                    'like_count': tweet.get('favorite_count', 0) or tweet.get('like_count', 0),
                    'reply_count': tweet.get('reply_count', 0)
                }
            
            score = (
                metrics.get('retweet_count', 0) * 2 +
                metrics.get('like_count', 0) +
                metrics.get('reply_count', 0) * 1.5
            )
            
            # 提取hashtags
            hashtags = re.findall(r'#\w+', text)
            if not hashtags:
                # 如果没有hashtag，使用关键词作为话题
                words = re.findall(r'\b[A-Za-z]{3,}\b', text)
                hashtags = [f"#{word}" for word in words[:2]]
            
            for tag in hashtags:
                if tag not in topic_scores:
                    topic_scores[tag] = {'score': 0, 'tweets': []}
                topic_scores[tag]['score'] += score
                topic_scores[tag]['tweets'].append(text[:200])
        
        # 如果没有找到话题，创建一些通用话题
        if not topic_scores:
            return self._create_generic_trends(tweets)
        
        # 排序并返回
        sorted_topics = sorted(
            topic_scores.items(),
            key=lambda x: x[1]['score'],
            reverse=True
        )
        
        return [
            {
                'topic': topic[0],
                'score': topic[1]['score'],
                'sample_tweets': topic[1]['tweets'][:3]
            }
            for topic in sorted_topics[:10]
        ]
    
    def _create_generic_trends(self, tweets: List[Dict]) -> List[Dict]:
        """从推文中创建通用趋势话题"""
        if not tweets:
            return []
        
        # 提取最常见的词汇作为话题
        all_words = []
        for tweet in tweets[:10]:  # 只分析前10条推文
            text = tweet.get('text', '')
            words = re.findall(r'\b[A-Za-z]{4,}\b', text.lower())
            all_words.extend(words)
        
        # 统计词频
        word_count = {}
        for word in all_words:
            if word not in ['this', 'that', 'with', 'have', 'will', 'from', 'they', 'been', 'said']:
                word_count[word] = word_count.get(word, 0) + 1
        
        # 创建话题
        trends = []
        for word, count in sorted(word_count.items(), key=lambda x: x[1], reverse=True)[:5]:
            trends.append({
                'topic': f"#{word.capitalize()}",
                'score': count * 100,
                'sample_tweets': [tweet.get('text', '')[:200] for tweet in tweets[:3]]
            })
        
        return trends
    
    def _get_fallback_trends(self) -> List[Dict]:
        """获取备用趋势（用于API失败时）"""
        return [
            {
                'topic': '#Technology',
                'score': 1000,
                'sample_tweets': ['Latest tech innovations...']
            },
            {
                'topic': '#AI',
                'score': 900,
                'sample_tweets': ['AI developments today...']
            },
            {
                'topic': '#Climate',
                'score': 800,
                'sample_tweets': ['Climate change updates...']
            }
        ]

class ContentGenerator:
    """内容生成器"""
    
    def __init__(self, api_key: str):
        self.client = openai.OpenAI(api_key=api_key)
    
    def generate_article(self, topic: Dict, language: str = 'en') -> Dict:
        """
        基于话题生成文章
        返回包含标题和内容的字典
        """
        prompt = self._create_prompt(topic, language)
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a professional content writer specializing in social media trends."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=1500
            )
            
            content = response.choices[0].message.content
            
            # 解析生成的内容
            lines = content.strip().split('\n')
            title = lines[0].replace('Title:', '').replace('标题：', '').strip()
            article_content = '\n'.join(lines[2:])  # 跳过标题和空行
            
            return {
                'title': title,
                'content': article_content,
                'topic': topic['topic'],
                'language': language
            }
            
        except Exception as e:
            print(f"生成文章失败: {e}")
            return self._get_fallback_article(topic, language)
    
    def _create_prompt(self, topic: Dict, language: str) -> str:
        """创建生成提示"""
        if language == 'zh':
            return f"""
请基于以下Twitter热门话题 {topic['topic']} 撰写一篇中文文章。

参考推文示例：
{chr(10).join(topic.get('sample_tweets', [])[:2])}

要求：
1. 文章长度500-800字
2. 语言通俗易懂，适合中文读者
3. 包含话题背景、当前发展、影响分析
4. 使用Markdown格式
5. 第一行输出"标题：[文章标题]"

请直接输出文章内容。
"""
        else:
            return f"""
Write an article based on the trending Twitter topic {topic['topic']}.

Sample tweets:
{chr(10).join(topic.get('sample_tweets', [])[:2])}

Requirements:
1. Article length: 500-800 words
2. Clear and engaging writing for general audience
3. Include background, current developments, and impact analysis
4. Use Markdown format
5. First line should be "Title: [Article Title]"

Please output the article directly.
"""
    
    def _get_fallback_article(self, topic: Dict, language: str) -> Dict:
        """获取备用文章"""
        if language == 'zh':
            return {
                'title': f"关于{topic['topic']}的最新动态",
                'content': f"今天，{topic['topic']}成为了Twitter上的热门话题...",
                'topic': topic['topic'],
                'language': language
            }
        else:
            return {
                'title': f"Latest Updates on {topic['topic']}",
                'content': f"Today, {topic['topic']} became a trending topic on Twitter...",
                'topic': topic['topic'],
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
    
    def publish_article(self, article: Dict):
        """发布文章到Hugo"""
        date = datetime.now()
        slug = self._create_slug(article['title'])
        
        # 确定文件路径
        language = article['language']
        filename = f"{date.strftime('%Y-%m-%d')}-{slug}.md"
        filepath = self.content_dir / language / 'posts' / filename
        
        # 创建前置内容
        frontmatter = self._create_frontmatter(article, date)
        
        # 写入文件
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(frontmatter)
            f.write('\n\n')
            f.write(article['content'])
            f.write('\n\n')
            f.write(self._add_monetag_ad())
        
        print(f"文章已发布: {filepath}")
    
    def publish_crypto_article(self, article: Dict):
        """发布加密货币文章到对应语言目录"""
        date = datetime.now()
        
        # 根据语言确定目录
        language = article['language']
        
        # 使用自定义文件名
        filename = f"{date.strftime('%Y-%m-%d')}-{article['filename']}.md"
        filepath = self.content_dir / language / 'posts' / filename
        
        # 直接写入文章内容（已包含frontmatter）
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(article['content'])
        
        print(f"✅ {language.upper()}加密货币文章已发布: {filepath}")
    
    def _create_slug(self, title: str) -> str:
        """创建URL友好的slug"""
        # 移除特殊字符，转换为小写
        slug = re.sub(r'[^\w\s-]', '', title.lower())
        slug = re.sub(r'[-\s]+', '-', slug)
        return slug[:50]  # 限制长度
    
    def _create_frontmatter(self, article: Dict, date: datetime) -> str:
        """创建Hugo前置内容"""
        return f"""---
title: "{article['title']}"
date: {date.isoformat()}
draft: false
tags: ["{article['topic'].replace('#', '')}", "trending", "twitter"]
categories: ["Social Media Trends"]
---"""
    
    def _add_monetag_ad(self) -> str:
        """添加Monetag广告代码"""
        return """
<!-- Monetag Ad -->
<div class="monetag-ad">
<script async src="//js.monetag.com/showads.js"></script>
<!-- 请替换为您的Monetag广告代码 -->
</div>
"""

def create_crypto_article_from_tweet_zh(tweet: Dict, index: int) -> Dict:
    """
    根据推文内容创建加密货币相关的markdown文章
    按照md-template.md的格式
    """
    from datetime import datetime
    import re
    
    # 获取推文信息
    text = tweet.get('text', '')
    author = tweet.get('author', {})
    author_name = author.get('name', '匿名用户')
    author_username = author.get('userName', 'anonymous')
    created_at = tweet.get('createdAt', '')
    like_count = tweet.get('likeCount', 0)
    retweet_count = tweet.get('retweetCount', 0)
    reply_count = tweet.get('replyCount', 0)
    
    # 提取hashtags作为标签
    hashtags = re.findall(r'#\w+', text)
    crypto_tags = ['区块链', '加密货币', '比特币', '以太坊', 'DeFi', 'Web3', 'NFT']
    
    # 生成文章标题
    title_keywords = []
    if 'bitcoin' in text.lower() or 'btc' in text.lower() or '比特币' in text:
        title_keywords.append('比特币')
    if 'ethereum' in text.lower() or 'eth' in text.lower() or '以太坊' in text:
        title_keywords.append('以太坊')
    if 'defi' in text.lower() or '去中心化' in text:
        title_keywords.append('DeFi')
    if 'nft' in text.lower():
        title_keywords.append('NFT')
    if 'web3' in text.lower():
        title_keywords.append('Web3')
    
    if not title_keywords:
        title_keywords = ['加密货币']
    
    title = f"{title_keywords[0]}市场动态分析：来自Twitter的热门观点第{index}期"
    
    # 生成文章内容
    current_time = datetime.now().strftime('%Y-%m-%dT%H:%M:%S+08:00')
    
    # 清理推文文本，移除链接
    clean_text = re.sub(r'https?://\S+', '', text).strip()
    
    content = f"""+++
date = '{current_time}'
draft = false
title = '{title}'
description = '基于Twitter热门推文的{title_keywords[0]}市场分析，包含用户观点、市场趋势和投资洞察。'
tags = {crypto_tags + title_keywords}
categories = ['市场分析']
keywords = ['{title_keywords[0]}分析', '加密货币市场', 'Twitter观点', '区块链趋势', '投资分析']
+++

## 🔥 热门推文分析

**推文作者**: @{author_username} ({author_name})  
**发布时间**: {created_at}  
**互动数据**: 👍 {like_count} | 🔄 {retweet_count} | 💬 {reply_count}

### 📝 原文内容

> {clean_text}

## 📊 市场观点解读

### 🎯 核心观点提取

基于这条热门推文，我们可以提取出以下几个关键市场观点：

1. **市场情绪分析**: 从推文的语调和用词可以看出当前市场参与者的情绪倾向
2. **技术趋势**: 推文中提到的技术发展和创新方向
3. **投资机会**: 隐含的投资机会和风险提示

### 💡 深度分析

#### 市场背景
当前{title_keywords[0]}市场正处于快速发展阶段，社交媒体上的讨论往往能够反映市场的真实情绪和趋势。这条获得{like_count + retweet_count + reply_count}次互动的推文，代表了相当一部分市场参与者的观点。

#### 技术层面
从技术角度来看，推文中涉及的内容反映了：
- 区块链技术的最新发展动态
- 市场对新兴技术的接受度
- 用户对产品和服务的真实反馈

#### 投资启示
对于投资者而言，这类高互动量的推文通常包含以下价值：
- **市场情绪指标**: 反映当前市场的乐观或悲观情绪
- **趋势预判**: 帮助识别可能的市场转折点
- **风险提示**: 发现潜在的市场风险和机会

## 🔍 相关市场数据

### 互动分析
- **点赞数**: {like_count} - 反映内容的受欢迎程度
- **转发数**: {retweet_count} - 显示信息传播的广度
- **评论数**: {reply_count} - 表明讨论的活跃程度

### 影响力评估
总互动数达到 **{like_count + retweet_count + reply_count}**，在加密货币相关推文中属于{"高" if (like_count + retweet_count + reply_count) > 100 else "中等" if (like_count + retweet_count + reply_count) > 10 else "一般"}影响力水平。

## 💭 市场展望

### 短期趋势
基于当前的社交媒体讨论热度和市场情绪，预计短期内{title_keywords[0]}市场将：
- 继续保持较高的关注度
- 可能出现相关概念的炒作
- 需要关注市场情绪的变化

### 长期价值
从长期投资角度来看：
- 关注技术基本面的发展
- 重视实际应用场景的落地
- 保持理性的投资态度

## ⚠️ 风险提示

1. **信息风险**: 社交媒体信息存在不准确或误导性的可能
2. **市场风险**: 加密货币市场波动性较大，投资需谨慎
3. **情绪风险**: 避免被短期市场情绪影响长期投资决策

## 📚 相关阅读

- 区块链技术发展趋势分析
- 加密货币投资策略指南
- DeFi生态系统深度解析
- NFT市场现状与未来展望

---

*本文基于公开的Twitter数据进行分析，不构成投资建议。加密货币投资存在高风险，请根据自身情况谨慎决策。*

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

*欢迎关注我的各个平台，获取最新的加密货币市场分析和投资洞察！*"""

    return {
        'title': title,
        'content': content,
        'language': 'zh',
        'filename': f"crypto-analysis-{index}"
    }

def create_crypto_article_from_tweet_en(tweet: Dict, index: int) -> Dict:
    """
    Create English cryptocurrency article based on tweet content
    Following the md-template.md format
    """
    from datetime import datetime
    import re
    
    # Get tweet information
    text = tweet.get('text', '')
    author = tweet.get('author', {})
    author_name = author.get('name', 'Anonymous User')
    author_username = author.get('userName', 'anonymous')
    created_at = tweet.get('createdAt', '')
    like_count = tweet.get('likeCount', 0)
    retweet_count = tweet.get('retweetCount', 0)
    reply_count = tweet.get('replyCount', 0)
    
    # Extract hashtags as tags
    hashtags = re.findall(r'#\w+', text)
    crypto_tags = ['blockchain', 'cryptocurrency', 'bitcoin', 'ethereum', 'DeFi', 'Web3', 'NFT']
    
    # Generate article title
    title_keywords = []
    if 'bitcoin' in text.lower() or 'btc' in text.lower():
        title_keywords.append('Bitcoin')
    if 'ethereum' in text.lower() or 'eth' in text.lower():
        title_keywords.append('Ethereum')
    if 'defi' in text.lower():
        title_keywords.append('DeFi')
    if 'nft' in text.lower():
        title_keywords.append('NFT')
    if 'web3' in text.lower():
        title_keywords.append('Web3')
    
    if not title_keywords:
        title_keywords = ['Cryptocurrency']
    
    title = f"{title_keywords[0]} Market Analysis: Hot Twitter Insights Episode {index}"
    
    # Generate article content
    current_time = datetime.now().strftime('%Y-%m-%dT%H:%M:%S+08:00')
    
    # Clean tweet text, remove links
    clean_text = re.sub(r'https?://\S+', '', text).strip()
    
    content = f"""+++
date = '{current_time}'
draft = false
title = '{title}'
description = 'Cryptocurrency market analysis based on trending Twitter posts, including user insights, market trends and investment perspectives.'
tags = {crypto_tags + [kw.lower() for kw in title_keywords]}
categories = ['Market Analysis']
keywords = ['{title_keywords[0].lower()} analysis', 'cryptocurrency market', 'Twitter insights', 'blockchain trends', 'investment analysis']
+++

## 🔥 Hot Tweet Analysis

**Tweet Author**: @{author_username} ({author_name})  
**Published**: {created_at}  
**Engagement Data**: 👍 {like_count} | 🔄 {retweet_count} | 💬 {reply_count}

### 📝 Original Content

> {clean_text}

## 📊 Market Insight Analysis

### 🎯 Key Viewpoint Extraction

Based on this trending tweet, we can extract the following key market perspectives:

1. **Market Sentiment Analysis**: The tone and wording reveal current market participants' emotional tendencies
2. **Technical Trends**: Technology developments and innovation directions mentioned in the tweet
3. **Investment Opportunities**: Implied investment opportunities and risk alerts

### 💡 In-Depth Analysis

#### Market Background
The current {title_keywords[0].lower()} market is in a rapid development phase, and social media discussions often reflect real market sentiment and trends. This tweet with {like_count + retweet_count + reply_count} interactions represents the views of a considerable portion of market participants.

#### Technical Perspective
From a technical standpoint, the content mentioned in the tweet reflects:
- Latest developments in blockchain technology
- Market acceptance of emerging technologies
- Real user feedback on products and services

#### Investment Insights
For investors, high-engagement tweets like this typically contain the following value:
- **Market Sentiment Indicators**: Reflect current market optimism or pessimism
- **Trend Prediction**: Help identify potential market turning points
- **Risk Alerts**: Discover potential market risks and opportunities

## 🔍 Related Market Data

### Engagement Analysis
- **Likes**: {like_count} - Reflects content popularity
- **Retweets**: {retweet_count} - Shows information spread breadth
- **Comments**: {reply_count} - Indicates discussion activity level

### Impact Assessment
Total engagement reached **{like_count + retweet_count + reply_count}**, which is {"high" if (like_count + retweet_count + reply_count) > 100 else "moderate" if (like_count + retweet_count + reply_count) > 10 else "low"} influence level among cryptocurrency-related tweets.

## 💭 Market Outlook

### Short-term Trends
Based on current social media discussion heat and market sentiment, the {title_keywords[0].lower()} market is expected to:
- Continue maintaining high attention levels
- Potentially see related concept speculation
- Require monitoring of market sentiment changes

### Long-term Value
From a long-term investment perspective:
- Focus on fundamental technology development
- Emphasize practical application scenario implementation
- Maintain rational investment attitudes

## ⚠️ Risk Warnings

1. **Information Risk**: Social media information may be inaccurate or misleading
2. **Market Risk**: Cryptocurrency markets are highly volatile, invest cautiously
3. **Emotional Risk**: Avoid letting short-term market emotions affect long-term investment decisions

## 📚 Related Reading

- Blockchain Technology Development Trend Analysis
- Cryptocurrency Investment Strategy Guide
- DeFi Ecosystem In-Depth Analysis
- NFT Market Current Status and Future Outlook

---

*This article is based on public Twitter data analysis and does not constitute investment advice. Cryptocurrency investment involves high risks, please make cautious decisions based on your own circumstances.*

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

*Follow my platforms for the latest cryptocurrency market analysis and investment insights!*"""

    return {
        'title': title,
        'content': content,
        'language': 'en',
        'filename': f"crypto-analysis-{index}"
    }

def main():
    """主函数"""
    print("开始生成今日内容...")
    
    # 检查环境变量
    if not TWITTER_API_KEY:
        print("错误：请设置TWITTER_API_KEY环境变量")
        return
    
    if not OPENAI_API_KEY or OPENAI_API_KEY == "your_openai_api_key_here":
        print("⚠️  警告：OpenAI API密钥未设置，将使用演示模式")
        demo_mode = True
    else:
        demo_mode = False
    
    # 初始化组件
    fetcher = TwitterTrendFetcher(TWITTER_API_KEY)
    if not demo_mode:
        generator = ContentGenerator(OPENAI_API_KEY)
    publisher = HugoPublisher(CONTENT_DIR)
    
    # 获取加密货币相关的热门推文
    print("🔍 搜索加密货币相关热门推文...")
    top_tweets = fetcher.get_crypto_trending_topics()
    
    if not top_tweets:
        print("❌ 未能获取到相关推文")
        return
    
    print(f"✅ 找到 {len(top_tweets)} 条热门推文")
    
    # 为每条热门推文生成双语文章
    for i, tweet in enumerate(top_tweets, 1):
        print(f"\n📝 处理第 {i} 条推文...")
        
        # 生成中文文章
        print("  📄 生成中文文章...")
        zh_article = create_crypto_article_from_tweet_zh(tweet, i)
        publisher.publish_crypto_article(zh_article)
        
        # 生成英文文章
        print("  📄 生成英文文章...")
        en_article = create_crypto_article_from_tweet_en(tweet, i)
        publisher.publish_crypto_article(en_article)
    
    print("\n内容生成完成！")

if __name__ == "__main__":
    main()
