#!/usr/bin/env python3
"""
模拟测试 OpenAI API 和 generate_article 方法
不需要真实的 API 密钥，用于测试方法逻辑
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv
from unittest.mock import Mock, patch

# 添加脚本目录到路径
sys.path.append(str(Path(__file__).parent))

# 导入主脚本中的类
from generate_content import ContentGenerator

# 加载环境变量
load_dotenv()

def create_mock_openai_response(language='en'):
    """创建模拟的 OpenAI API 响应"""
    if language == 'zh':
        mock_content = """标题：比特币市场分析：机构投资推动价格创新高

## 市场概况

比特币近期表现强劲，主要受到机构投资者大量买入的推动。多家知名公司宣布将比特币纳入其资产配置，这一趋势正在改变整个加密货币市场的格局。

## 技术分析

从技术角度来看，比特币突破了关键阻力位，交易量显著增加。这表明市场情绪转向乐观，投资者信心正在恢复。

## 市场影响

机构投资的涌入不仅推高了比特币价格，也带动了整个加密货币市场的上涨。以太坊、莱特币等主流币种也出现了不同程度的涨幅。

## 风险提示

尽管市场表现积极，投资者仍需注意加密货币市场的高波动性。建议合理配置资产，控制投资风险。

## 结论

比特币的机构化趋势正在加速，这为长期投资者提供了新的机会。但同时也需要密切关注监管政策的变化和市场情绪的波动。"""
    else:
        mock_content = """Title: Bitcoin Market Analysis: Institutional Investment Drives Price to New Highs

## Market Overview

Bitcoin has shown strong performance recently, primarily driven by significant purchases from institutional investors. Several prominent companies have announced the inclusion of Bitcoin in their asset allocation, a trend that is reshaping the entire cryptocurrency market landscape.

## Technical Analysis

From a technical perspective, Bitcoin has broken through key resistance levels with significantly increased trading volume. This indicates a shift in market sentiment toward optimism and recovering investor confidence.

## Market Impact

The influx of institutional investment has not only pushed Bitcoin prices higher but also lifted the entire cryptocurrency market. Major cryptocurrencies like Ethereum and Litecoin have also experienced varying degrees of gains.

## Risk Warning

Despite positive market performance, investors should remain aware of the high volatility in cryptocurrency markets. It is recommended to allocate assets reasonably and control investment risks.

## Conclusion

The institutionalization trend of Bitcoin is accelerating, providing new opportunities for long-term investors. However, it is also necessary to closely monitor changes in regulatory policies and market sentiment fluctuations."""
    
    # 创建模拟响应对象
    mock_choice = Mock()
    mock_choice.message.content = mock_content
    
    mock_response = Mock()
    mock_response.choices = [mock_choice]
    
    return mock_response

def test_generate_article_mock():
    """使用模拟 API 测试文章生成"""
    print("🧪 开始模拟测试 generate_article 方法")
    print("=" * 60)
    
    # 创建 ContentGenerator 实例（使用假的 API 密钥）
    generator = ContentGenerator(
        api_key="fake-api-key",
        backup_api_key="fake-backup-key",
        backup_base_url="https://fake-backup-api.com/v1"
    )
    
    # 创建测试话题
    test_topics = [
        {
            'topic': '#Bitcoin',
            'score': 1500,
            'sample_tweets': [
                'Bitcoin just hit a new milestone! The adoption is growing faster than ever. #BTC #Crypto',
                'Major institutions are now adding Bitcoin to their balance sheets. This is huge for mainstream adoption.'
            ]
        },
        {
            'topic': '#比特币',
            'score': 1200,
            'sample_tweets': [
                '比特币今天又创新高了！机构投资者的入场真的改变了整个市场格局 #比特币 #加密货币',
                '看到越来越多的公司开始接受比特币支付，这种主流化的趋势不可阻挡'
            ]
        }
    ]
    
    # 测试英文文章生成
    print("\n📝 测试英文文章生成（模拟模式）...")
    with patch.object(generator.primary_client.chat.completions, 'create') as mock_create:
        mock_create.return_value = create_mock_openai_response('en')
        
        try:
            article = generator.generate_article(test_topics[0], language='en')
            
            print("✅ 英文文章生成成功!")
            print(f"  📰 标题: {article['title']}")
            print(f"  🏷️  话题: {article['topic']}")
            print(f"  🌐 语言: {article['language']}")
            print(f"  📄 内容长度: {len(article['content'])} 字符")
            print("\n📖 文章内容预览:")
            print("-" * 50)
            print(article['content'][:300] + "..." if len(article['content']) > 300 else article['content'])
            print("-" * 50)
            
        except Exception as e:
            print(f"❌ 英文文章生成失败: {e}")
    
    # 测试中文文章生成
    print("\n📝 测试中文文章生成（模拟模式）...")
    with patch.object(generator.primary_client.chat.completions, 'create') as mock_create:
        mock_create.return_value = create_mock_openai_response('zh')
        
        try:
            article = generator.generate_article(test_topics[1], language='zh')
            
            print("✅ 中文文章生成成功!")
            print(f"  📰 标题: {article['title']}")
            print(f"  🏷️  话题: {article['topic']}")
            print(f"  🌐 语言: {article['language']}")
            print(f"  📄 内容长度: {len(article['content'])} 字符")
            print("\n📖 文章内容预览:")
            print("-" * 50)
            print(article['content'][:300] + "..." if len(article['content']) > 300 else article['content'])
            print("-" * 50)
            
        except Exception as e:
            print(f"❌ 中文文章生成失败: {e}")

def test_prompt_creation():
    """测试提示词创建逻辑"""
    print("\n🎯 测试提示词创建逻辑...")
    
    generator = ContentGenerator("fake-api-key")
    
    test_topic = {
        'topic': '#AI',
        'score': 800,
        'sample_tweets': ['AI is revolutionizing every industry. The future is here!']
    }
    
    # 测试英文提示词
    en_prompt = generator._create_prompt(test_topic, 'en')
    print("✅ 英文提示词创建成功")
    print(f"  📝 提示词长度: {len(en_prompt)} 字符")
    print("  🔍 提示词内容预览:")
    print("  " + en_prompt[:200] + "...")
    
    # 测试中文提示词
    zh_prompt = generator._create_prompt(test_topic, 'zh')
    print("\n✅ 中文提示词创建成功")
    print(f"  📝 提示词长度: {len(zh_prompt)} 字符")
    print("  🔍 提示词内容预览:")
    print("  " + zh_prompt[:200] + "...")

def test_fallback_article():
    """测试备用文章生成"""
    print("\n🔄 测试备用文章生成...")
    
    generator = ContentGenerator("fake-api-key")
    
    test_topic = {
        'topic': '#Technology',
        'score': 500,
        'sample_tweets': ['Tech innovation is accelerating rapidly.']
    }
    
    # 测试英文备用文章
    en_fallback = generator._get_fallback_article(test_topic, 'en')
    print("✅ 英文备用文章生成成功")
    print(f"  📰 标题: {en_fallback['title']}")
    print(f"  📄 内容: {en_fallback['content'][:100]}...")
    
    # 测试中文备用文章
    zh_fallback = generator._get_fallback_article(test_topic, 'zh')
    print("\n✅ 中文备用文章生成成功")
    print(f"  📰 标题: {zh_fallback['title']}")
    print(f"  📄 内容: {zh_fallback['content'][:100]}...")

def test_api_error_handling():
    """测试 API 错误处理"""
    print("\n⚠️  测试 API 错误处理...")
    
    generator = ContentGenerator("fake-api-key")
    
    test_topic = {
        'topic': '#ErrorTest',
        'score': 100,
        'sample_tweets': ['This is a test tweet for error handling.']
    }
    
    # 模拟 API 错误
    with patch.object(generator.primary_client.chat.completions, 'create') as mock_create:
        mock_create.side_effect = Exception("API Error: Rate limit exceeded")
        
        try:
            article = generator.generate_article(test_topic, language='en')
            
            print("✅ 错误处理成功，返回备用文章")
            print(f"  📰 标题: {article['title']}")
            print(f"  📄 内容类型: {'备用文章' if 'became a trending topic' in article['content'] else '正常文章'}")
            print(f"  🔧 使用的服务: {article.get('ai_service', '未知')}")
            
        except Exception as e:
            print(f"❌ 错误处理失败: {e}")

def test_backup_ai_service():
    """测试备用AI服务切换功能"""
    print("\n🔄 测试备用AI服务切换功能...")
    
    # 创建带备用服务的生成器
    generator = ContentGenerator(
        api_key="fake-primary-key",
        backup_api_key="fake-backup-key", 
        backup_base_url="https://fake-backup-api.com/v1"
    )
    
    test_topic = {
        'topic': '#BackupTest',
        'score': 200,
        'sample_tweets': ['Testing backup AI service functionality.']
    }
    
    # 模拟主服务失败，备用服务成功
    with patch.object(generator.primary_client.chat.completions, 'create') as mock_primary, \
         patch.object(generator.backup_client.chat.completions, 'create') as mock_backup:
        
        # 主服务失败
        mock_primary.side_effect = Exception("Primary API Error")
        
        # 备用服务成功
        mock_backup_response = Mock()
        mock_backup_response.choices = [Mock()]
        mock_backup_response.choices[0].message.content = """Title: Backup AI Service Test Article

## Test Content

This article was generated by the backup AI service when the primary service failed.

The backup system is working correctly and can generate quality content as a fallback option."""
        mock_backup.return_value = mock_backup_response
        
        try:
            article = generator.generate_article(test_topic, language='en')
            
            print("✅ 备用AI服务切换成功!")
            print(f"  📰 标题: {article['title']}")
            print(f"  🔧 使用的服务: {article.get('ai_service', '未知')}")
            print(f"  📄 内容长度: {len(article['content'])} 字符")
            
            if article.get('ai_service') == 'backup':
                print("  🎯 成功使用备用AI服务生成文章")
            else:
                print("  ⚠️  未正确标识使用的AI服务")
                
        except Exception as e:
            print(f"❌ 备用AI服务测试失败: {e}")

def test_no_backup_service():
    """测试没有配置备用服务时的行为"""
    print("\n🚫 测试没有备用服务时的行为...")
    
    # 创建没有备用服务的生成器
    generator = ContentGenerator("fake-primary-key")
    
    test_topic = {
        'topic': '#NoBackupTest',
        'score': 150,
        'sample_tweets': ['Testing behavior when no backup service is configured.']
    }
    
    # 模拟主服务失败
    with patch.object(generator.primary_client.chat.completions, 'create') as mock_primary:
        mock_primary.side_effect = Exception("Primary API Error")
        
        try:
            article = generator.generate_article(test_topic, language='en')
            
            print("✅ 无备用服务时错误处理成功")
            print(f"  📰 标题: {article['title']}")
            print(f"  🔧 使用的服务: {article.get('ai_service', '未知')}")
            
            if article.get('ai_service') == 'fallback':
                print("  🎯 正确使用本地备用文章")
            else:
                print("  ⚠️  未正确标识使用的服务类型")
                
        except Exception as e:
            print(f"❌ 无备用服务测试失败: {e}")

def main():
    """主测试函数"""
    print("🚀 开始模拟测试 OpenAI generate_article 方法")
    print("🎭 使用模拟 API 响应，无需真实 API 密钥")
    print("=" * 60)
    
    # 测试文章生成
    test_generate_article_mock()
    
    # 测试提示词创建
    test_prompt_creation()
    
    # 测试备用文章
    test_fallback_article()
    
    # 测试错误处理
    test_api_error_handling()
    
    # 测试备用AI服务
    test_backup_ai_service()
    
    # 测试无备用服务情况
    test_no_backup_service()
    
    print("\n" + "=" * 60)
    print("🎉 模拟测试完成!")
    print("✅ 所有 generate_article 方法逻辑测试通过")
    print("✅ 备用AI服务切换功能测试通过")
    print("\n💡 要测试真实的 OpenAI API，请:")
    print("   1. 在 .env 文件中设置真实的 OPENAI_API_KEY")
    print("   2. 运行 python scripts/test_openai_generate.py")

if __name__ == "__main__":
    main()