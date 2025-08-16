#!/usr/bin/env python3
"""
测试新的Twitter API接口
"""

import os
import requests

# 尝试加载dotenv，如果没有安装就跳过
try:
    from dotenv import load_dotenv
    load_dotenv()
    print("✅ 已加载 .env 文件")
except ImportError:
    print("⚠️  python-dotenv 未安装，直接使用环境变量")

def test_twitter_api():
    """测试Twitter API连接"""
    
    api_key = os.environ.get('TWITTER_API_KEY')
    
    if not api_key:
        print("❌ 错误：请设置TWITTER_API_KEY环境变量")
        print("   在.env文件中添加: TWITTER_API_KEY=your_api_key_here")
        return False
    
    print("🔍 测试Twitter API连接...")
    
    url = "https://api.twitterapi.io/twitter/tweet/advanced_search"
    headers = {"X-API-Key": api_key}
    
    # 测试参数
    params = {
        'query': 'trending',
        'max_results': 10
    }
    
    try:
        response = requests.get(url, headers=headers, params=params)
        
        print(f"📡 API响应状态码: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print("✅ API连接成功！")
            
            # 显示响应数据结构
            if 'data' in data:
                tweets = data['data']
                print(f"📊 获取到 {len(tweets)} 条推文")
                
                if tweets:
                    print("\n📝 示例推文:")
                    for i, tweet in enumerate(tweets[:3], 1):
                        text = tweet.get('text', 'No text')[:100]
                        print(f"   {i}. {text}...")
                else:
                    print("⚠️  未获取到推文数据")
            else:
                print("⚠️  响应中没有'data'字段")
                print(f"   响应内容: {data}")
            
            return True
            
        elif response.status_code == 401:
            print("❌ API密钥无效或未授权")
            print("   请检查TWITTER_API_KEY是否正确")
            
        elif response.status_code == 429:
            print("❌ API请求频率限制")
            print("   请稍后再试")
            
        else:
            print(f"❌ API请求失败: {response.status_code}")
            print(f"   错误信息: {response.text}")
        
        return False
        
    except requests.exceptions.RequestException as e:
        print(f"❌ 网络请求失败: {e}")
        return False
    except Exception as e:
        print(f"❌ 未知错误: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Twitter API 测试工具")
    print("=" * 40)
    
    success = test_twitter_api()
    
    print("\n" + "=" * 40)
    if success:
        print("✅ 测试完成！API工作正常")
        print("💡 现在可以运行: python scripts/generate_content.py")
    else:
        print("❌ 测试失败！请检查API配置")
        print("💡 确保在.env文件中正确设置了TWITTER_API_KEY")