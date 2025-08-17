#!/usr/bin/env python3
"""
测试账号监控功能
"""

import os
import sys
from pathlib import Path

# 添加脚本目录到Python路径
sys.path.append(str(Path(__file__).parent))

from monitor_accounts import TwitterAccountMonitor, ContentGenerator, HugoPublisher
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

def test_twitter_monitor():
    """测试Twitter监控功能"""
    print("🧪 测试Twitter账号监控功能...")
    
    api_key = os.environ.get('TWITTER_API_KEY')
    if not api_key:
        print("❌ 请设置TWITTER_API_KEY环境变量")
        return False
    
    # 测试账号列表
    test_accounts = ['elonmusk', 'a16z']  # 使用知名账号进行测试
    
    monitor = TwitterAccountMonitor(api_key)
    
    # 测试获取单个用户推文
    print("\n📱 测试获取单个用户推文...")
    tweets = monitor.get_user_tweets('elonmusk', max_results=5)
    
    if tweets:
        print(f"✅ 成功获取 {len(tweets)} 条推文")
        print(f"   第一条推文: {tweets[0].get('text', '')[:100]}...")
    else:
        print("❌ 未能获取推文")
        return False
    
    # 测试获取所有监控账号推文
    print("\n📋 测试获取所有监控账号推文...")
    all_tweets = monitor.get_all_monitored_tweets(test_accounts)
    
    if all_tweets:
        print(f"✅ 成功获取 {len(all_tweets)} 个账号的推文")
        for account, tweets in all_tweets.items():
            print(f"   @{account}: {len(tweets)} 条推文")
    else:
        print("❌ 未能获取任何账号的推文")
        return False
    
    # 测试时间过滤
    print("\n⏰ 测试时间过滤...")
    for account, tweets in all_tweets.items():
        recent = monitor.filter_recent_tweets(tweets, hours=24)
        print(f"   @{account}: {len(recent)} 条最近24小时推文")
    
    return True

def test_content_generator():
    """测试内容生成器"""
    print("\n🤖 测试内容生成器...")
    
    # 模拟推文数据
    mock_tweets_data = {
        'elonmusk': [
            {
                'text': 'The future of sustainable transport is electric vehicles and renewable energy.',
                'createdAt': '2025-08-17T10:00:00Z',
                'likeCount': 1000,
                'retweetCount': 500,
                'replyCount': 200
            }
        ],
        'a16z': [
            {
                'text': 'Web3 infrastructure is evolving rapidly. The next wave of innovation is coming.',
                'createdAt': '2025-08-17T11:00:00Z',
                'likeCount': 800,
                'retweetCount': 300,
                'replyCount': 150
            }
        ]
    }
    
    generator = ContentGenerator(
        api_key=os.environ.get('OPENAI_API_KEY'),
        backup_api_key=os.environ.get('AI_API_KEY'),
        backup_base_url=os.environ.get('AI_BASE_URL')
    )
    
    # 测试生成中文分析文章
    print("   生成中文分析文章...")
    zh_article = generator.generate_analysis_article(mock_tweets_data, 'zh')
    
    if zh_article and zh_article.get('title') and zh_article.get('content'):
        print(f"   ✅ 中文文章标题: {zh_article['title'][:50]}...")
        print(f"   ✅ 中文文章长度: {len(zh_article['content'])} 字符")
    else:
        print("   ❌ 中文文章生成失败")
        return False
    
    # 测试生成英文分析文章
    print("   生成英文分析文章...")
    en_article = generator.generate_analysis_article(mock_tweets_data, 'en')
    
    if en_article and en_article.get('title') and en_article.get('content'):
        print(f"   ✅ 英文文章标题: {en_article['title'][:50]}...")
        print(f"   ✅ 英文文章长度: {len(en_article['content'])} 字符")
    else:
        print("   ❌ 英文文章生成失败")
        return False
    
    return True

def test_hugo_publisher():
    """测试Hugo发布器"""
    print("\n📝 测试Hugo发布器...")
    
    content_dir = Path(__file__).parent.parent / 'content'
    publisher = HugoPublisher(content_dir)
    
    # 模拟推文数据
    mock_tweets_data = {
        'testuser': [
            {
                'text': 'This is a test tweet for monitoring functionality.',
                'createdAt': '2025-08-17T12:00:00Z',
                'likeCount': 10,
                'retweetCount': 5,
                'replyCount': 2
            }
        ]
    }
    
    # 测试发布原始推文文章
    print("   测试发布原始推文文章...")
    try:
        publisher.publish_raw_tweets_article(mock_tweets_data, 'zh')
        publisher.publish_raw_tweets_article(mock_tweets_data, 'en')
        print("   ✅ 原始推文文章发布成功")
    except Exception as e:
        print(f"   ❌ 原始推文文章发布失败: {e}")
        return False
    
    # 测试发布分析文章
    print("   测试发布分析文章...")
    mock_analysis = {
        'title': '测试分析文章标题',
        'content': '这是一篇测试分析文章的内容...',
        'language': 'zh'
    }
    
    try:
        publisher.publish_analysis_article(mock_analysis)
        print("   ✅ 分析文章发布成功")
    except Exception as e:
        print(f"   ❌ 分析文章发布失败: {e}")
        return False
    
    return True

def main():
    """主测试函数"""
    print("🚀 开始测试账号监控功能...\n")
    
    success_count = 0
    total_tests = 3
    
    # 测试Twitter监控
    if test_twitter_monitor():
        success_count += 1
    
    # 测试内容生成器
    if test_content_generator():
        success_count += 1
    
    # 测试Hugo发布器
    if test_hugo_publisher():
        success_count += 1
    
    # 输出测试结果
    print(f"\n📊 测试结果: {success_count}/{total_tests} 通过")
    
    if success_count == total_tests:
        print("🎉 所有测试通过！账号监控功能可以正常使用。")
    else:
        print("⚠️  部分测试失败，请检查配置和网络连接。")
    
    return success_count == total_tests

if __name__ == "__main__":
    main()