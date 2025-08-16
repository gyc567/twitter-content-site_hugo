#!/usr/bin/env python3
"""
仅测试Twitter API部分，不需要OpenAI
"""

import os
import requests
from datetime import datetime
from typing import List, Dict
from pathlib import Path
import re
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# 配置
TWITTER_API_KEY = os.environ.get('TWITTER_API_KEY')

class TwitterTrendFetcher:
    """Twitter趋势获取器"""
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.headers = {
            'X-API-Key': api_key,
            'User-Agent': 'TwitterTrendBot/1.0'
        }
    
    def get_trending_topics(self, query: str = "trending", max_results: int = 100) -> List[Dict]:
        """
        获取趋势话题
        使用新的Twitter API接口
        """
        url = "https://api.twitterapi.io/twitter/tweet/advanced_search"
        
        # 构建查询参数
        params = {
            'query': query,
            'max_results': max_results,
            'sort_order': 'relevancy'
        }
        
        try:
            print(f"🔍 正在请求API: {url}")
            print(f"📊 查询参数: {params}")
            
            response = requests.get(url, headers=self.headers, params=params)
            
            print(f"📡 响应状态码: {response.status_code}")
            
            if response.status_code != 200:
                print(f"❌ API请求失败: {response.text}")
                return self._get_fallback_trends()
            
            response.raise_for_status()
            data = response.json()
            
            print(f"✅ API响应成功")
            print(f"📄 响应数据键: {list(data.keys()) if isinstance(data, dict) else 'Not a dict'}")
            
            # 分析数据并提取热门话题
            # API返回的数据在'tweets'键下，不是'data'
            tweets = data.get('tweets', data.get('data', []))
            trends = self._analyze_trends(tweets)
            return trends[:3]  # 返回前3个热门话题
            
        except Exception as e:
            print(f"❌ 获取Twitter趋势失败: {e}")
            print(f"错误详情: {response.text if 'response' in locals() else 'No response'}")
            # 返回备用热门话题
            return self._get_fallback_trends()
    
    def _analyze_trends(self, tweets: List[Dict]) -> List[Dict]:
        """分析推文提取趋势"""
        print(f"📝 分析 {len(tweets)} 条推文...")
        
        if not tweets:
            print("⚠️  没有推文数据，使用备用趋势")
            return self._get_fallback_trends()
        
        # 显示前几条推文示例
        for i, tweet in enumerate(tweets[:3], 1):
            text = tweet.get('text', 'No text')[:100]
            print(f"   推文 {i}: {text}...")
        
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
        
        print(f"🏆 找到 {len(sorted_topics)} 个话题")
        
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

def main():
    """主函数"""
    print("🚀 测试Twitter API集成")
    print("=" * 50)
    
    # 检查环境变量
    if not TWITTER_API_KEY:
        print("❌ 错误：请设置TWITTER_API_KEY环境变量")
        print("💡 在.env文件中添加: TWITTER_API_KEY=your_api_key_here")
        return
    
    print(f"✅ Twitter API Key已设置: {TWITTER_API_KEY[:10]}...")
    
    # 初始化组件
    fetcher = TwitterTrendFetcher(TWITTER_API_KEY)
    
    # 获取热门话题
    print("\n🔍 获取Twitter热门话题...")
    trends = fetcher.get_trending_topics()
    
    if not trends:
        print("❌ 未能获取到热门话题")
        return
    
    print(f"\n🎉 成功找到 {len(trends)} 个热门话题:")
    print("=" * 50)
    
    # 显示话题详情
    for i, trend in enumerate(trends, 1):
        print(f"\n📈 话题 {i}: {trend['topic']}")
        print(f"   评分: {trend['score']}")
        print(f"   示例推文:")
        for j, tweet in enumerate(trend.get('sample_tweets', []), 1):
            print(f"     {j}. {tweet[:100]}...")
    
    print("\n" + "=" * 50)
    print("✅ Twitter API测试完成！")

if __name__ == "__main__":
    main()