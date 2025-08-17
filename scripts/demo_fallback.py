#!/usr/bin/env python3
"""
Twitter兜底方案演示脚本
展示TwitterAPI.io和Twikit的自动切换机制
"""

import os
import sys
import asyncio
from pathlib import Path
from dotenv import load_dotenv

# 添加脚本目录到Python路径
sys.path.append(str(Path(__file__).parent))

from twitter_client import UnifiedTwitterClient

# 加载环境变量
load_dotenv()

async def demo_fallback_mechanism():
    """演示兜底机制"""
    print("🎭 Twitter API兜底方案演示")
    print("="*50)
    
    # 创建统一客户端
    client = UnifiedTwitterClient()
    
    # 检查配置状态
    has_twitter_api = bool(os.environ.get('TWITTER_API_KEY'))
    has_twikit = bool(os.environ.get('TWITTER_USERNAME') and os.environ.get('TWITTER_PASSWORD'))
    
    print(f"📊 配置状态:")
    print(f"   TwitterAPI.io: {'✅ 已配置' if has_twitter_api else '❌ 未配置'}")
    print(f"   Twikit:        {'✅ 已配置' if has_twikit else '❌ 未配置'}")
    print()
    
    if not has_twitter_api and not has_twikit:
        print("❌ 没有可用的Twitter API配置，无法演示")
        return
    
    # 演示场景1：正常获取推文
    print("🎬 场景1：正常获取用户推文")
    print("-" * 30)
    
    try:
        tweets = await client.get_user_tweets('elonmusk', max_results=3)
        if tweets:
            print(f"✅ 成功获取 {len(tweets)} 条推文")
            for i, tweet in enumerate(tweets[:2], 1):
                print(f"   {i}. {tweet.get('text', '')[:80]}...")
                print(f"      来源: {tweet.get('source', 'twitterapi')}")
        else:
            print("❌ 未能获取推文")
    except Exception as e:
        print(f"❌ 获取推文异常: {e}")
    
    print()
    
    # 演示场景2：搜索功能
    print("🎬 场景2：搜索推文功能")
    print("-" * 30)
    
    try:
        tweets = await client.search_tweets('bitcoin', max_results=3)
        if tweets:
            print(f"✅ 成功搜索到 {len(tweets)} 条推文")
            for i, tweet in enumerate(tweets[:2], 1):
                print(f"   {i}. {tweet.get('text', '')[:80]}...")
                print(f"      来源: {tweet.get('source', 'twitterapi')}")
        else:
            print("❌ 未能搜索到推文")
    except Exception as e:
        print(f"❌ 搜索推文异常: {e}")
    
    print()
    
    # 演示场景3：批量获取
    print("🎬 场景3：批量获取多个账号")
    print("-" * 30)
    
    test_accounts = ['elonmusk', 'a16z']
    all_tweets = {}
    
    for account in test_accounts:
        try:
            tweets = await client.get_user_tweets(account, max_results=2)
            if tweets:
                all_tweets[account] = tweets
                print(f"✅ @{account}: {len(tweets)} 条推文")
            else:
                print(f"❌ @{account}: 获取失败")
        except Exception as e:
            print(f"❌ @{account}: 异常 - {e}")
    
    print(f"\n📊 批量获取结果: {len(all_tweets)} 个账号成功")
    
    print()
    
    # 演示场景4：时间过滤
    if all_tweets:
        print("🎬 场景4：时间过滤功能")
        print("-" * 30)
        
        for account, tweets in all_tweets.items():
            recent = client.filter_recent_tweets(tweets, hours=24)
            week = client.filter_recent_tweets(tweets, hours=24*7)
            
            print(f"@{account}:")
            print(f"   总推文: {len(tweets)}")
            print(f"   24小时内: {len(recent)}")
            print(f"   7天内: {len(week)}")
    
    print("\n" + "="*50)
    print("🎉 演示完成！")
    
    # 给出使用建议
    print("\n💡 使用建议:")
    if has_twitter_api and has_twikit:
        print("   ✅ 双重保障已配置，系统具备最高可靠性")
    elif has_twitter_api:
        print("   ⚠️  仅配置了TwitterAPI.io，建议添加Twikit作为兜底")
    elif has_twikit:
        print("   ⚠️  仅配置了Twikit，建议添加TwitterAPI.io提升性能")
    
    print("   📚 详细文档: TWITTER_FALLBACK.md")

def main():
    """主函数"""
    try:
        asyncio.run(demo_fallback_mechanism())
    except KeyboardInterrupt:
        print("\n👋 演示已取消")
    except Exception as e:
        print(f"\n❌ 演示异常: {e}")

if __name__ == "__main__":
    main()