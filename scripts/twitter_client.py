#!/usr/bin/env python3
"""
Twitter客户端 - 支持多种API方案
包含TwitterAPI.io和twikit作为兜底方案
"""

import os
import json
import requests
import asyncio
from datetime import datetime, timedelta
from typing import List, Dict, Optional
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

class TwitterAPIClient:
    """TwitterAPI.io客户端（主要方案）"""
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.headers = {
            'X-API-Key': api_key,
            'User-Agent': 'TwitterContentBot/1.0'
        }
        self.base_url = "https://api.twitterapi.io/twitter"
    
    def get_user_tweets(self, username: str, max_results: int = 10) -> List[Dict]:
        """获取用户推文"""
        url = f"{self.base_url}/user/tweets"
        params = {
            'username': username.replace('@', ''),
            'max_results': max_results,
            'exclude': 'retweets,replies'
        }
        
        try:
            print(f"🔍 [TwitterAPI] 获取 @{username} 的推文...")
            response = requests.get(url, headers=self.headers, params=params, timeout=30)
            response.raise_for_status()
            data = response.json()
            
            tweets = data.get('tweets', [])
            print(f"   ✅ 找到 {len(tweets)} 条推文")
            return tweets
            
        except Exception as e:
            print(f"   ❌ TwitterAPI失败: {e}")
            return []
    
    def search_tweets(self, query: str, max_results: int = 20) -> List[Dict]:
        """搜索推文"""
        url = f"{self.base_url}/tweet/advanced_search"
        params = {
            'query': query,
            'max_results': max_results,
            'sort_order': 'relevancy'
        }
        
        try:
            print(f"🔍 [TwitterAPI] 搜索: {query}")
            response = requests.get(url, headers=self.headers, params=params, timeout=30)
            response.raise_for_status()
            data = response.json()
            
            tweets = data.get('tweets', [])
            print(f"   ✅ 找到 {len(tweets)} 条推文")
            return tweets
            
        except Exception as e:
            print(f"   ❌ TwitterAPI搜索失败: {e}")
            return []

class TwikitClient:
    """Twikit客户端（兜底方案）"""
    
    def __init__(self, username: str = None, password: str = None, email: str = None):
        self.client = None
        self.username = username
        self.password = password
        self.email = email
        self.authenticated = False
        
        # 尝试导入twikit
        try:
            from twikit import Client
            self.Client = Client
            print("✅ Twikit库已加载")
        except ImportError:
            print("❌ Twikit库未安装，请运行: pip install twikit")
            self.Client = None
    
    async def authenticate(self) -> bool:
        """认证登录"""
        if not self.Client:
            return False
            
        try:
            self.client = self.Client('en-US')
            
            if self.username and self.password:
                print("🔐 [Twikit] 尝试登录...")
                await self.client.login(
                    auth_info_1=self.username,
                    auth_info_2=self.email or self.username,
                    password=self.password
                )
                self.authenticated = True
                print("✅ [Twikit] 登录成功")
                return True
            else:
                print("⚠️  [Twikit] 未提供登录凭据，使用访客模式")
                # 某些功能可能在访客模式下受限
                self.authenticated = False
                return True
                
        except Exception as e:
            print(f"❌ [Twikit] 认证失败: {e}")
            return False
    
    async def get_user_tweets(self, username: str, max_results: int = 10) -> List[Dict]:
        """获取用户推文"""
        if not self.client:
            return []
        
        try:
            print(f"🔍 [Twikit] 获取 @{username} 的推文...")
            
            # 获取用户信息
            user = await self.client.get_user_by_screen_name(username.replace('@', ''))
            if not user:
                print(f"   ❌ 用户 @{username} 不存在")
                return []
            
            # 获取用户推文
            tweets = await self.client.get_user_tweets(user.id, 'Tweets', count=max_results)
            
            # 转换为标准格式
            formatted_tweets = []
            for tweet in tweets:
                formatted_tweet = {
                    'id': tweet.id,
                    'text': tweet.text,
                    'createdAt': tweet.created_at,
                    'author': {
                        'name': tweet.user.name,
                        'userName': tweet.user.screen_name,
                        'id': tweet.user.id
                    },
                    'likeCount': getattr(tweet, 'favorite_count', 0),
                    'retweetCount': getattr(tweet, 'retweet_count', 0),
                    'replyCount': getattr(tweet, 'reply_count', 0),
                    'source': 'twikit'
                }
                formatted_tweets.append(formatted_tweet)
            
            print(f"   ✅ 找到 {len(formatted_tweets)} 条推文")
            return formatted_tweets
            
        except Exception as e:
            print(f"   ❌ [Twikit] 获取推文失败: {e}")
            return []
    
    async def search_tweets(self, query: str, max_results: int = 20) -> List[Dict]:
        """搜索推文"""
        if not self.client:
            return []
        
        try:
            print(f"🔍 [Twikit] 搜索: {query}")
            
            # 搜索推文
            tweets = await self.client.search_tweet(query, 'Latest', count=max_results)
            
            # 转换为标准格式
            formatted_tweets = []
            for tweet in tweets:
                formatted_tweet = {
                    'id': tweet.id,
                    'text': tweet.text,
                    'createdAt': tweet.created_at,
                    'author': {
                        'name': tweet.user.name,
                        'userName': tweet.user.screen_name,
                        'id': tweet.user.id
                    },
                    'likeCount': getattr(tweet, 'favorite_count', 0),
                    'retweetCount': getattr(tweet, 'retweet_count', 0),
                    'replyCount': getattr(tweet, 'reply_count', 0),
                    'source': 'twikit'
                }
                formatted_tweets.append(formatted_tweet)
            
            print(f"   ✅ 找到 {len(formatted_tweets)} 条推文")
            return formatted_tweets
            
        except Exception as e:
            print(f"   ❌ [Twikit] 搜索失败: {e}")
            return []

class UnifiedTwitterClient:
    """统一Twitter客户端 - 支持多种API方案"""
    
    def __init__(self):
        # 从环境变量获取配置
        self.twitter_api_key = os.environ.get('TWITTER_API_KEY')
        self.twitter_username = os.environ.get('TWITTER_USERNAME')
        self.twitter_password = os.environ.get('TWITTER_PASSWORD')
        self.twitter_email = os.environ.get('TWITTER_EMAIL')
        
        # 初始化客户端
        self.api_client = None
        self.twikit_client = None
        
        # 初始化TwitterAPI客户端
        if self.twitter_api_key:
            self.api_client = TwitterAPIClient(self.twitter_api_key)
            print("✅ TwitterAPI.io客户端已初始化")
        
        # 初始化Twikit客户端
        self.twikit_client = TwikitClient(
            username=self.twitter_username,
            password=self.twitter_password,
            email=self.twitter_email
        )
    
    async def authenticate_twikit(self) -> bool:
        """认证Twikit客户端"""
        if self.twikit_client:
            return await self.twikit_client.authenticate()
        return False
    
    async def get_user_tweets(self, username: str, max_results: int = 10) -> List[Dict]:
        """获取用户推文 - 优先使用TwitterAPI，失败时使用Twikit"""
        
        # 首先尝试TwitterAPI
        if self.api_client:
            tweets = self.api_client.get_user_tweets(username, max_results)
            if tweets:
                return tweets
            print("🔄 TwitterAPI失败，尝试Twikit兜底方案...")
        
        # 使用Twikit兜底
        if self.twikit_client:
            if not self.twikit_client.authenticated:
                await self.authenticate_twikit()
            
            tweets = await self.twikit_client.get_user_tweets(username, max_results)
            if tweets:
                return tweets
        
        print(f"❌ 所有方案都失败，无法获取 @{username} 的推文")
        return []
    
    async def search_tweets(self, query: str, max_results: int = 20) -> List[Dict]:
        """搜索推文 - 优先使用TwitterAPI，失败时使用Twikit"""
        
        # 首先尝试TwitterAPI
        if self.api_client:
            tweets = self.api_client.search_tweets(query, max_results)
            if tweets:
                return tweets
            print("🔄 TwitterAPI搜索失败，尝试Twikit兜底方案...")
        
        # 使用Twikit兜底
        if self.twikit_client:
            if not self.twikit_client.authenticated:
                await self.authenticate_twikit()
            
            tweets = await self.twikit_client.search_tweets(query, max_results)
            if tweets:
                return tweets
        
        print(f"❌ 所有方案都失败，无法搜索: {query}")
        return []
    
    def filter_recent_tweets(self, tweets: List[Dict], hours: int = 24) -> List[Dict]:
        """过滤最近指定小时内的推文"""
        if not tweets:
            return []
        
        cutoff_time = datetime.now() - timedelta(hours=hours)
        recent_tweets = []
        
        for tweet in tweets:
            created_at = tweet.get('createdAt', '')
            if created_at:
                try:
                    # 处理不同的时间格式
                    if isinstance(created_at, str):
                        # ISO格式
                        if 'T' in created_at:
                            tweet_time = datetime.fromisoformat(created_at.replace('Z', '+00:00'))
                        else:
                            # 其他格式，尝试解析
                            tweet_time = datetime.strptime(created_at, '%a %b %d %H:%M:%S %z %Y')
                    else:
                        # 如果是datetime对象
                        tweet_time = created_at
                    
                    # 移除时区信息进行比较
                    if hasattr(tweet_time, 'replace'):
                        tweet_time = tweet_time.replace(tzinfo=None)
                    
                    if tweet_time > cutoff_time:
                        recent_tweets.append(tweet)
                        
                except Exception as e:
                    print(f"⚠️  时间解析失败: {e}, 保留推文")
                    recent_tweets.append(tweet)
        
        return recent_tweets

# 同步包装器函数
def create_twitter_client() -> UnifiedTwitterClient:
    """创建Twitter客户端"""
    return UnifiedTwitterClient()

def get_user_tweets_sync(client: UnifiedTwitterClient, username: str, max_results: int = 10) -> List[Dict]:
    """同步获取用户推文"""
    return asyncio.run(client.get_user_tweets(username, max_results))

def search_tweets_sync(client: UnifiedTwitterClient, query: str, max_results: int = 20) -> List[Dict]:
    """同步搜索推文"""
    return asyncio.run(client.search_tweets(query, max_results))

async def get_all_monitored_tweets_async(client: UnifiedTwitterClient, accounts: List[str]) -> Dict[str, List[Dict]]:
    """异步获取所有监控账号的推文"""
    all_tweets = {}
    
    for account in accounts:
        account = account.strip()
        if account:
            tweets = await client.get_user_tweets(account)
            if tweets:
                all_tweets[account] = tweets
    
    return all_tweets

def get_all_monitored_tweets_sync(client: UnifiedTwitterClient, accounts: List[str]) -> Dict[str, List[Dict]]:
    """同步获取所有监控账号的推文"""
    return asyncio.run(get_all_monitored_tweets_async(client, accounts))