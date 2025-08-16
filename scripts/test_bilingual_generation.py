#!/usr/bin/env python3
"""
测试双语文章生成功能
使用模拟的推文数据
"""

import os
from datetime import datetime
from pathlib import Path
import sys

# 添加父目录到路径以便导入
sys.path.append(str(Path(__file__).parent))

# 从主脚本导入需要的函数
from generate_content import (
    create_crypto_article_from_tweet_zh,
    create_crypto_article_from_tweet_en,
    HugoPublisher
)

# 模拟推文数据
MOCK_TWEETS = [
    {
        'text': 'Bitcoin just hit a new all-time high! 🚀 The institutional adoption is driving massive growth. #Bitcoin #BTC #cryptocurrency #bullish',
        'author': {
            'name': 'Crypto Analyst Pro',
            'userName': 'cryptoanalyst_pro'
        },
        'createdAt': 'Sat Aug 16 15:30:00 +0000 2025',
        'likeCount': 1250,
        'retweetCount': 340,
        'replyCount': 89
    },
    {
        'text': 'Ethereum 2.0 staking rewards are looking incredible! The DeFi ecosystem is thriving like never before. Time to HODL! #Ethereum #ETH #DeFi #Web3',
        'author': {
            'name': 'DeFi Researcher',
            'userName': 'defi_researcher'
        },
        'createdAt': 'Sat Aug 16 14:45:00 +0000 2025',
        'likeCount': 890,
        'retweetCount': 234,
        'replyCount': 67
    },
    {
        'text': 'NFT marketplace volume is exploding! 💎 New collections are selling out in minutes. The digital art revolution is here to stay. #NFT #digitalart #blockchain',
        'author': {
            'name': 'NFT Collector',
            'userName': 'nft_collector_2025'
        },
        'createdAt': 'Sat Aug 16 13:20:00 +0000 2025',
        'likeCount': 567,
        'retweetCount': 123,
        'replyCount': 45
    }
]

def test_bilingual_generation():
    """测试双语文章生成"""
    print("🚀 测试双语加密货币文章生成")
    print("=" * 50)
    
    # 初始化发布器
    content_dir = Path(__file__).parent.parent / 'content'
    publisher = HugoPublisher(content_dir)
    
    # 为每条模拟推文生成双语文章
    for i, tweet in enumerate(MOCK_TWEETS, 1):
        print(f"\n📝 处理第 {i} 条推文...")
        print(f"   内容: {tweet['text'][:80]}...")
        print(f"   互动: 👍{tweet['likeCount']} 🔄{tweet['retweetCount']} 💬{tweet['replyCount']}")
        
        # 生成中文文章
        print("  📄 生成中文文章...")
        zh_article = create_crypto_article_from_tweet_zh(tweet, i)
        publisher.publish_crypto_article(zh_article)
        
        # 生成英文文章
        print("  📄 生成英文文章...")
        en_article = create_crypto_article_from_tweet_en(tweet, i)
        publisher.publish_crypto_article(en_article)
    
    print("\n" + "=" * 50)
    print("✅ 双语文章生成测试完成！")
    print(f"📁 中文文章目录: {content_dir}/zh/posts/")
    print(f"📁 英文文章目录: {content_dir}/en/posts/")

if __name__ == "__main__":
    test_bilingual_generation()