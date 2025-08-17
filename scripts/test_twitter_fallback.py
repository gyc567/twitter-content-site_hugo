#!/usr/bin/env python3
"""
测试Twitter兜底方案功能
测试TwitterAPI.io和Twikit的集成
"""

import os
import sys
import asyncio
from pathlib import Path
from dotenv import load_dotenv

# 添加脚本目录到Python路径
sys.path.append(str(Path(__file__).parent))

from twitter_client import UnifiedTwitterClient, TwitterAPIClient, TwikitClient

# 加载环境变量
load_dotenv()

async def test_twitter_api_client():
    """测试TwitterAPI.io客户端"""
    print("🧪 测试TwitterAPI.io客户端...")
    
    api_key = os.environ.get('TWITTER_API_KEY')
    if not api_key:
        print("⚠️  未配置TWITTER_API_KEY，跳过测试")
        return False
    
    client = TwitterAPIClient(api_key)
    
    # 测试获取用户推文
    print("📱 测试获取用户推文...")
    tweets = client.get_user_tweets('elonmusk', max_results=5)
    
    if tweets:
        print(f"✅ 成功获取 {len(tweets)} 条推文")
        print(f"   示例推文: {tweets[0].get('text', '')[:100]}...")
        return True
    else:
        print("❌ 获取推文失败")
        return False

async def test_twikit_client():
    """测试Twikit客户端"""
    print("\n🧪 测试Twikit客户端...")
    
    username = os.environ.get('TWITTER_USERNAME')
    password = os.environ.get('TWITTER_PASSWORD')
    email = os.environ.get('TWITTER_EMAIL')
    
    if not username or not password:
        print("⚠️  未配置Twikit登录凭据，跳过测试")
        return False
    
    client = TwikitClient(username, password, email)
    
    # 测试认证
    print("🔐 测试认证...")
    auth_success = await client.authenticate()
    
    if not auth_success:
        print("❌ 认证失败")
        return False
    
    print("✅ 认证成功")
    
    # 测试获取用户推文
    print("📱 测试获取用户推文...")
    tweets = await client.get_user_tweets('elonmusk', max_results=5)
    
    if tweets:
        print(f"✅ 成功获取 {len(tweets)} 条推文")
        print(f"   示例推文: {tweets[0].get('text', '')[:100]}...")
        return True
    else:
        print("❌ 获取推文失败")
        return False

async def test_unified_client():
    """测试统一客户端"""
    print("\n🧪 测试统一Twitter客户端...")
    
    client = UnifiedTwitterClient()
    
    # 测试获取用户推文（会自动尝试主要方案和兜底方案）
    print("📱 测试获取用户推文（自动兜底）...")
    tweets = await client.get_user_tweets('elonmusk', max_results=5)
    
    if tweets:
        print(f"✅ 成功获取 {len(tweets)} 条推文")
        print(f"   示例推文: {tweets[0].get('text', '')[:100]}...")
        print(f"   数据源: {tweets[0].get('source', 'twitterapi')}")
        return True
    else:
        print("❌ 所有方案都失败")
        return False

async def test_search_functionality():
    """测试搜索功能"""
    print("\n🧪 测试搜索功能...")
    
    client = UnifiedTwitterClient()
    
    # 测试搜索推文
    print("🔍 测试搜索推文...")
    tweets = await client.search_tweets('bitcoin', max_results=5)
    
    if tweets:
        print(f"✅ 成功搜索到 {len(tweets)} 条推文")
        print(f"   示例推文: {tweets[0].get('text', '')[:100]}...")
        return True
    else:
        print("❌ 搜索失败")
        return False

async def test_time_filtering():
    """测试时间过滤功能"""
    print("\n🧪 测试时间过滤功能...")
    
    client = UnifiedTwitterClient()
    
    # 获取一些推文
    tweets = await client.get_user_tweets('elonmusk', max_results=10)
    
    if not tweets:
        print("❌ 无法获取推文进行时间过滤测试")
        return False
    
    print(f"📊 原始推文数量: {len(tweets)}")
    
    # 过滤最近24小时的推文
    recent_tweets = client.filter_recent_tweets(tweets, hours=24)
    print(f"📊 最近24小时推文: {len(recent_tweets)}")
    
    # 过滤最近7天的推文
    week_tweets = client.filter_recent_tweets(tweets, hours=24*7)
    print(f"📊 最近7天推文: {len(week_tweets)}")
    
    print("✅ 时间过滤功能正常")
    return True

async def main():
    """主测试函数"""
    print("🚀 开始测试Twitter兜底方案功能...\n")
    
    test_results = []
    
    # 测试TwitterAPI.io客户端
    try:
        result = await test_twitter_api_client()
        test_results.append(('TwitterAPI.io客户端', result))
    except Exception as e:
        print(f"❌ TwitterAPI.io测试异常: {e}")
        test_results.append(('TwitterAPI.io客户端', False))
    
    # 测试Twikit客户端
    try:
        result = await test_twikit_client()
        test_results.append(('Twikit客户端', result))
    except Exception as e:
        print(f"❌ Twikit测试异常: {e}")
        test_results.append(('Twikit客户端', False))
    
    # 测试统一客户端
    try:
        result = await test_unified_client()
        test_results.append(('统一客户端', result))
    except Exception as e:
        print(f"❌ 统一客户端测试异常: {e}")
        test_results.append(('统一客户端', False))
    
    # 测试搜索功能
    try:
        result = await test_search_functionality()
        test_results.append(('搜索功能', result))
    except Exception as e:
        print(f"❌ 搜索功能测试异常: {e}")
        test_results.append(('搜索功能', False))
    
    # 测试时间过滤
    try:
        result = await test_time_filtering()
        test_results.append(('时间过滤', result))
    except Exception as e:
        print(f"❌ 时间过滤测试异常: {e}")
        test_results.append(('时间过滤', False))
    
    # 输出测试结果
    print("\n" + "="*50)
    print("📊 测试结果汇总:")
    print("="*50)
    
    passed = 0
    total = len(test_results)
    
    for test_name, result in test_results:
        status = "✅ 通过" if result else "❌ 失败"
        print(f"{test_name:<20} {status}")
        if result:
            passed += 1
    
    print("="*50)
    print(f"总计: {passed}/{total} 通过")
    
    if passed == total:
        print("🎉 所有测试通过！Twitter兜底方案功能正常。")
    elif passed > 0:
        print("⚠️  部分测试通过，请检查失败的功能。")
    else:
        print("❌ 所有测试失败，请检查配置和网络连接。")
    
    # 配置建议
    print("\n💡 配置建议:")
    if not os.environ.get('TWITTER_API_KEY'):
        print("   - 配置 TWITTER_API_KEY 以启用TwitterAPI.io")
    if not os.environ.get('TWITTER_USERNAME'):
        print("   - 配置 TWITTER_USERNAME, TWITTER_PASSWORD, TWITTER_EMAIL 以启用Twikit兜底")
    
    return passed == total

if __name__ == "__main__":
    asyncio.run(main())