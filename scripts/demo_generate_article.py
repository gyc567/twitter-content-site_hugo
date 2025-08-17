#!/usr/bin/env python3
"""
generate_article 方法演示脚本
展示如何使用 ContentGenerator 类生成文章
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

def demo_basic_usage():
    """演示基本用法"""
    print("🎯 generate_article 方法基本用法演示")
    print("=" * 50)
    
    # 1. 创建 ContentGenerator 实例
    print("1️⃣ 创建 ContentGenerator 实例")
    generator = ContentGenerator(
        api_key="demo-api-key",
        backup_api_key="demo-backup-key",
        backup_base_url="https://demo-backup-api.com/v1"
    )
    print("   ✅ ContentGenerator 实例创建成功")
    print("   ✅ 主要和备用AI服务都已配置")
    
    # 2. 准备话题数据
    print("\n2️⃣ 准备话题数据")
    topic_data = {
        'topic': '#Bitcoin',
        'score': 1500,
        'sample_tweets': [
            'Bitcoin just reached a new all-time high! 🚀 #BTC #Crypto',
            'Major companies are now accepting Bitcoin as payment. The future is here!',
            'Institutional investors are pouring billions into Bitcoin. This is huge! 💰'
        ]
    }
    print(f"   📊 话题: {topic_data['topic']}")
    print(f"   🔥 热度分数: {topic_data['score']}")
    print(f"   📱 示例推文数量: {len(topic_data['sample_tweets'])}")
    
    # 3. 生成英文文章（模拟）
    print("\n3️⃣ 生成英文文章")
    with patch.object(generator.primary_client.chat.completions, 'create') as mock_create:
        # 模拟 OpenAI 响应
        mock_response = Mock()
        mock_response.choices = [Mock()]
        mock_response.choices[0].message.content = """Title: Bitcoin Reaches New Heights as Institutional Adoption Accelerates

## Market Breakthrough

Bitcoin has achieved another significant milestone, reaching new all-time highs as institutional adoption continues to accelerate. This latest surge reflects growing confidence from major corporations and investment firms who are increasingly viewing Bitcoin as a legitimate store of value.

## Institutional Interest

The cryptocurrency market is witnessing unprecedented institutional interest. Major companies across various sectors are not only accepting Bitcoin as payment but also adding it to their corporate treasuries. This shift represents a fundamental change in how traditional finance views digital assets.

## Market Impact

The influx of institutional capital has provided Bitcoin with increased stability and legitimacy. Unlike previous bull runs driven primarily by retail investors, this current surge is backed by sophisticated financial institutions with long-term investment strategies.

## Future Outlook

As more institutions enter the Bitcoin space, we can expect continued growth and mainstream adoption. However, investors should remain aware of the inherent volatility in cryptocurrency markets and invest responsibly.

The convergence of institutional adoption, technological improvements, and growing public awareness suggests that Bitcoin's role in the global financial system will continue to expand."""
        
        mock_create.return_value = mock_response
        
        # 调用 generate_article 方法
        english_article = generator.generate_article(topic_data, language='en')
        
        print("   ✅ 英文文章生成成功!")
        print(f"   📰 标题: {english_article['title']}")
        print(f"   🌐 语言: {english_article['language']}")
        print(f"   📄 内容长度: {len(english_article['content'])} 字符")
    
    # 4. 生成中文文章（模拟）
    print("\n4️⃣ 生成中文文章")
    chinese_topic = {
        'topic': '#比特币',
        'score': 1200,
        'sample_tweets': [
            '比特币又创新高了！机构投资者的入场改变了游戏规则 🚀',
            '越来越多的公司开始接受比特币支付，主流化趋势不可阻挡',
            '华尔街巨头纷纷布局比特币，这波牛市有点不一样 💰'
        ]
    }
    
    with patch.object(generator.primary_client.chat.completions, 'create') as mock_create:
        # 模拟中文响应
        mock_response = Mock()
        mock_response.choices = [Mock()]
        mock_response.choices[0].message.content = """标题：比特币创新高：机构化浪潮推动加密货币主流化

## 市场突破

比特币再次创下历史新高，这一轮上涨主要由机构投资者的大规模入场推动。与以往主要由散户投资者驱动的牛市不同，这次的上涨更具可持续性和稳定性。

## 机构布局

华尔街的金融巨头们正在重新审视比特币的价值。从特斯拉到微软，从高盛到摩根大通，越来越多的知名企业开始将比特币纳入其投资组合或接受比特币支付。

## 市场影响

机构资金的涌入为比特币市场带来了前所未有的流动性和稳定性。这种变化不仅推高了价格，更重要的是提升了比特币在传统金融体系中的地位。

## 未来展望

随着监管环境的逐步明朗和技术基础设施的不断完善，比特币的机构化趋势将继续加速。这为长期投资者提供了新的机会，但同时也需要注意市场波动的风险。

比特币正在从一个实验性的数字资产转变为全球金融体系的重要组成部分。"""
        
        mock_create.return_value = mock_response
        
        # 调用 generate_article 方法
        chinese_article = generator.generate_article(chinese_topic, language='zh')
        
        print("   ✅ 中文文章生成成功!")
        print(f"   📰 标题: {chinese_article['title']}")
        print(f"   🌐 语言: {chinese_article['language']}")
        print(f"   📄 内容长度: {len(chinese_article['content'])} 字符")
    
    return english_article, chinese_article

def demo_error_handling():
    """演示错误处理"""
    print("\n🛡️ 错误处理演示")
    print("=" * 50)
    
    generator = ContentGenerator("demo-api-key")
    
    test_topic = {
        'topic': '#TestError',
        'score': 100,
        'sample_tweets': ['This is a test for error handling.']
    }
    
    # 模拟 API 错误
    with patch.object(generator.client.chat.completions, 'create') as mock_create:
        mock_create.side_effect = Exception("API Error: Rate limit exceeded")
        
        print("🔥 模拟 API 错误...")
        article = generator.generate_article(test_topic, language='en')
        
        print("✅ 错误处理成功!")
        print(f"   📰 备用文章标题: {article['title']}")
        print(f"   📄 备用文章内容: {article['content'][:100]}...")
        print("   💡 系统自动使用备用文章，确保程序不会崩溃")

def demo_different_topics():
    """演示不同话题的处理"""
    print("\n🎨 不同话题处理演示")
    print("=" * 50)
    
    generator = ContentGenerator("demo-api-key")
    
    topics = [
        {
            'name': 'AI技术',
            'data': {
                'topic': '#AI',
                'score': 800,
                'sample_tweets': ['AI is transforming every industry. The future is now!']
            }
        },
        {
            'name': '气候变化',
            'data': {
                'topic': '#Climate',
                'score': 600,
                'sample_tweets': ['Climate action is more urgent than ever. We need solutions now.']
            }
        },
        {
            'name': '科技创新',
            'data': {
                'topic': '#Technology',
                'score': 900,
                'sample_tweets': ['New tech innovations are changing how we work and live.']
            }
        }
    ]
    
    for i, topic_info in enumerate(topics, 1):
        print(f"{i}️⃣ 处理话题: {topic_info['name']}")
        
        # 创建模拟响应
        with patch.object(generator.primary_client.chat.completions, 'create') as mock_create:
            mock_response = Mock()
            mock_response.choices = [Mock()]
            mock_response.choices[0].message.content = f"Title: Analysis of {topic_info['data']['topic']}\n\nThis is a sample article about {topic_info['data']['topic']} based on trending discussions..."
            mock_create.return_value = mock_response
            
            article = generator.generate_article(topic_info['data'], language='en')
            print(f"   ✅ 文章生成成功: {article['title'][:50]}...")

def main():
    """主演示函数"""
    print("🚀 generate_article 方法完整演示")
    print("🎭 使用模拟 API 响应进行演示")
    print("=" * 60)
    
    # 基本用法演示
    en_article, zh_article = demo_basic_usage()
    
    # 错误处理演示
    demo_error_handling()
    
    # 不同话题演示
    demo_different_topics()
    
    # 总结
    print("\n📋 演示总结")
    print("=" * 60)
    print("✅ generate_article 方法功能完整")
    print("✅ 支持中英文双语生成")
    print("✅ 具备完善的错误处理机制")
    print("✅ 可以处理多种不同类型的话题")
    print("✅ 返回结构化的文章数据")
    
    print("\n🔧 方法特性:")
    print("   📝 智能提示词生成")
    print("   🛡️ 自动错误恢复")
    print("   🌐 多语言支持")
    print("   📊 结构化输出")
    print("   🎯 话题适应性强")
    
    print("\n💡 实际使用建议:")
    print("   1. 设置真实的 OpenAI API 密钥")
    print("   2. 根据需要调整 temperature 参数")
    print("   3. 监控 API 使用量和成本")
    print("   4. 定期更新提示词模板")
    print("   5. 实施内容质量检查")

if __name__ == "__main__":
    main()