#!/usr/bin/env python3
"""
测试 OpenAI API 和 generate_article 方法
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# 添加脚本目录到路径
sys.path.append(str(Path(__file__).parent))

# 导入主脚本中的类
from generate_content import ContentGenerator

# 加载环境变量
load_dotenv()

def test_openai_connection():
    """测试 OpenAI API 连接和备用AI服务配置"""
    print("🔍 测试 OpenAI API 连接和备用AI服务配置...")
    
    # 检查主要API密钥
    api_key = os.environ.get('OPENAI_API_KEY')
    backup_api_key = os.environ.get('AI_API_KEY')
    backup_base_url = os.environ.get('AI_BASE_URL')
    
    if not api_key or api_key.startswith('sk-1234') or api_key == "your_openai_api_key_here":
        print("⚠️  OpenAI API 密钥未设置或使用示例值")
        print("当前密钥:", api_key[:20] + "..." if api_key else "未设置")
        
        # 检查是否有备用服务配置
        if backup_api_key and backup_base_url and not backup_api_key.startswith('sk-backup-1234'):
            print("✅ 发现备用AI服务配置，将使用备用服务进行测试")
            print(f"备用服务URL: {backup_base_url}")
        else:
            print("❌ 主要和备用AI服务都未正确配置")
            print("请在 .env 文件中设置:")
            print("  OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx")
            print("  或者配置备用AI服务:")
            print("  AI_API_KEY=your_backup_api_key")
            print("  AI_BASE_URL=https://api.your-backup-service.com/v1")
            return False
    else:
        print("✅ OpenAI API 密钥已配置")
    
    # 检查备用服务配置
    if backup_api_key and backup_base_url:
        if not backup_api_key.startswith('sk-backup-1234'):
            print("✅ 备用AI服务已配置")
        else:
            print("⚠️  备用AI服务使用示例值")
    else:
        print("⚠️  未配置备用AI服务")
    
    try:
        generator = ContentGenerator(
            api_key=api_key,
            backup_api_key=backup_api_key,
            backup_base_url=backup_base_url
        )
        print("✅ ContentGenerator 初始化成功")
        return generator
    except Exception as e:
        print(f"❌ ContentGenerator 初始化失败: {e}")
        return False

def test_generate_article_english():
    """测试英文文章生成"""
    print("\n📝 测试英文文章生成...")
    
    generator = test_openai_connection()
    if not generator:
        return
    
    # 创建测试话题
    test_topic = {
        'topic': '#Bitcoin',
        'score': 1500,
        'sample_tweets': [
            'Bitcoin just hit a new milestone! The adoption is growing faster than ever. #BTC #Crypto',
            'Major institutions are now adding Bitcoin to their balance sheets. This is huge for mainstream adoption.'
        ]
    }
    
    try:
        print("  🤖 调用 OpenAI API 生成英文文章...")
        article = generator.generate_article(test_topic, language='en')
        
        print("✅ 英文文章生成成功!")
        print(f"  📰 标题: {article['title']}")
        print(f"  🏷️  话题: {article['topic']}")
        print(f"  🌐 语言: {article['language']}")
        print(f"  🔧 AI服务: {article.get('ai_service', '未知')}")
        print(f"  📄 内容长度: {len(article['content'])} 字符")
        print("\n📖 文章内容预览:")
        print("-" * 50)
        print(article['content'][:300] + "..." if len(article['content']) > 300 else article['content'])
        print("-" * 50)
        
        return article
        
    except Exception as e:
        print(f"❌ 英文文章生成失败: {e}")
        return None

def test_generate_article_chinese():
    """测试中文文章生成"""
    print("\n📝 测试中文文章生成...")
    
    generator = test_openai_connection()
    if not generator:
        return
    
    # 创建测试话题
    test_topic = {
        'topic': '#比特币',
        'score': 1200,
        'sample_tweets': [
            '比特币今天又创新高了！机构投资者的入场真的改变了整个市场格局 #比特币 #加密货币',
            '看到越来越多的公司开始接受比特币支付，这种主流化的趋势不可阻挡'
        ]
    }
    
    try:
        print("  🤖 调用 OpenAI API 生成中文文章...")
        article = generator.generate_article(test_topic, language='zh')
        
        print("✅ 中文文章生成成功!")
        print(f"  📰 标题: {article['title']}")
        print(f"  🏷️  话题: {article['topic']}")
        print(f"  🌐 语言: {article['language']}")
        print(f"  🔧 AI服务: {article.get('ai_service', '未知')}")
        print(f"  📄 内容长度: {len(article['content'])} 字符")
        print("\n📖 文章内容预览:")
        print("-" * 50)
        print(article['content'][:300] + "..." if len(article['content']) > 300 else article['content'])
        print("-" * 50)
        
        return article
        
    except Exception as e:
        print(f"❌ 中文文章生成失败: {e}")
        return None

def test_different_topics():
    """测试不同话题的文章生成"""
    print("\n🎯 测试不同话题的文章生成...")
    
    generator = test_openai_connection()
    if not generator:
        return
    
    test_topics = [
        {
            'topic': '#AI',
            'score': 800,
            'sample_tweets': ['AI is revolutionizing every industry. The future is here!']
        },
        {
            'topic': '#Climate',
            'score': 600,
            'sample_tweets': ['Climate change action is more urgent than ever. We need solutions now.']
        },
        {
            'topic': '#Technology',
            'score': 900,
            'sample_tweets': ['New tech innovations are changing how we work and live.']
        }
    ]
    
    for i, topic in enumerate(test_topics, 1):
        print(f"\n  📝 测试话题 {i}: {topic['topic']}")
        try:
            article = generator.generate_article(topic, language='en')
            print(f"    ✅ 成功生成文章: {article['title'][:50]}...")
            print(f"    🔧 使用的AI服务: {article.get('ai_service', '未知')}")
        except Exception as e:
            print(f"    ❌ 生成失败: {e}")

def main():
    """主测试函数"""
    print("🚀 开始测试 OpenAI generate_article 方法")
    print("=" * 60)
    
    # 测试 API 连接
    if not test_openai_connection():
        print("\n❌ 无法连接到 OpenAI API，测试终止")
        return
    
    # 测试英文文章生成
    en_article = test_generate_article_english()
    
    # 测试中文文章生成
    zh_article = test_generate_article_chinese()
    
    # 测试不同话题
    test_different_topics()
    
    print("\n" + "=" * 60)
    print("🎉 测试完成!")
    
    if en_article and zh_article:
        print("✅ 所有基本测试通过")
    else:
        print("⚠️  部分测试失败，请检查错误信息")

if __name__ == "__main__":
    main()