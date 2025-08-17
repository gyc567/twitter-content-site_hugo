#!/usr/bin/env python3
"""
测试总结报告
汇总所有测试结果并提供建议
"""

import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

def check_environment():
    """检查环境配置"""
    print("🔍 环境配置检查")
    print("-" * 30)
    
    # 检查 Python 依赖
    try:
        import openai
        print("✅ OpenAI 库已安装 (版本: {})".format(openai.__version__))
    except ImportError:
        print("❌ OpenAI 库未安装")
        return False
    
    try:
        import requests
        print("✅ Requests 库已安装")
    except ImportError:
        print("❌ Requests 库未安装")
        return False
    
    try:
        from dotenv import load_dotenv
        print("✅ Python-dotenv 库已安装")
    except ImportError:
        print("❌ Python-dotenv 库未安装")
        return False
    
    # 检查环境变量
    twitter_key = os.environ.get('TWITTER_API_KEY')
    openai_key = os.environ.get('OPENAI_API_KEY')
    ai_key = os.environ.get('AI_API_KEY')
    ai_base_url = os.environ.get('AI_BASE_URL')
    
    print(f"\n🔑 API 密钥状态:")
    if twitter_key and not twitter_key.startswith('your_'):
        print(f"✅ Twitter API 密钥已设置 ({twitter_key[:10]}...)")
    else:
        print("⚠️  Twitter API 密钥未设置或使用示例值")
    
    if openai_key and not openai_key.startswith('sk-1234') and openai_key != "your_openai_api_key_here":
        print(f"✅ OpenAI API 密钥已设置 ({openai_key[:10]}...)")
    else:
        print("⚠️  OpenAI API 密钥未设置或使用示例值")
    
    if ai_key and ai_base_url and not ai_key.startswith('sk-backup-1234'):
        print(f"✅ 备用AI API 密钥已设置 ({ai_key[:10]}...)")
        print(f"✅ 备用AI服务地址: {ai_base_url}")
    else:
        print("⚠️  备用AI API 密钥未设置或使用示例值")
    
    return True

def test_generate_article_method():
    """测试 generate_article 方法"""
    print("\n📝 generate_article 方法测试")
    print("-" * 30)
    
    try:
        # 导入并测试方法存在性
        import sys
        from pathlib import Path
        sys.path.append(str(Path(__file__).parent))
        
        from generate_content import ContentGenerator
        
        # 检查方法是否存在
        generator = ContentGenerator("fake-key")
        
        if hasattr(generator, 'generate_article'):
            print("✅ generate_article 方法存在")
        else:
            print("❌ generate_article 方法不存在")
            return False
        
        if hasattr(generator, '_create_prompt'):
            print("✅ _create_prompt 方法存在")
        else:
            print("❌ _create_prompt 方法不存在")
        
        if hasattr(generator, '_get_fallback_article'):
            print("✅ _get_fallback_article 方法存在")
        else:
            print("❌ _get_fallback_article 方法不存在")
        
        print("✅ ContentGenerator 类结构完整")
        return True
        
    except ImportError as e:
        print(f"❌ 导入失败: {e}")
        return False
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        return False

def check_file_structure():
    """检查文件结构"""
    print("\n📁 文件结构检查")
    print("-" * 30)
    
    required_files = [
        'scripts/generate_content.py',
        'scripts/test_openai_generate.py',
        'scripts/test_openai_mock.py',
        'scripts/test_openai_simple.py',
        '.env',
        'requirements.txt',
        'content/en/posts',
        'content/zh/posts'
    ]
    
    all_exist = True
    for file_path in required_files:
        if os.path.exists(file_path):
            print(f"✅ {file_path}")
        else:
            print(f"❌ {file_path} (缺失)")
            all_exist = False
    
    return all_exist

def provide_recommendations():
    """提供使用建议"""
    print("\n💡 使用建议")
    print("-" * 30)
    
    openai_key = os.environ.get('OPENAI_API_KEY')
    twitter_key = os.environ.get('TWITTER_API_KEY')
    ai_key = os.environ.get('AI_API_KEY')
    ai_base_url = os.environ.get('AI_BASE_URL')
    
    # 检查AI服务配置状态
    openai_available = openai_key and not openai_key.startswith('sk-1234') and openai_key != "your_openai_api_key_here"
    backup_available = ai_key and ai_base_url and not ai_key.startswith('sk-backup-1234')
    
    if openai_available or backup_available:
        print("🚀 您可以运行真实的 AI API 测试:")
        print("   python scripts/test_openai_generate.py")
        print("   python scripts/test_openai_simple.py")
        
        if openai_available and backup_available:
            print("✅ 主要和备用AI服务都已配置，具备完整的兜底能力")
        elif openai_available:
            print("⚠️  仅配置了OpenAI服务，建议配置备用AI服务")
        else:
            print("⚠️  仅配置了备用AI服务，建议配置OpenAI服务")
    else:
        print("🎭 建议先运行模拟测试:")
        print("   python scripts/test_openai_mock.py")
        print("\n🔑 要使用真实 AI API，请配置以下之一:")
        print("   OpenAI:")
        print("     1. 访问 https://platform.openai.com/api-keys")
        print("     2. 创建 API 密钥")
        print("     3. 在 .env 文件中设置 OPENAI_API_KEY")
        print("   备用AI服务 (如 DeepSeek, 通义千问等):")
        print("     1. 获取兼容OpenAI格式的API密钥")
        print("     2. 在 .env 文件中设置 AI_API_KEY 和 AI_BASE_URL")
    
    if twitter_key and not twitter_key.startswith('your_'):
        print("\n📱 Twitter API 已配置，可以测试:")
        print("   python scripts/test_twitter_api.py")
    else:
        print("\n📱 要使用 Twitter API，请:")
        print("   1. 访问 https://twitterapi.io/")
        print("   2. 获取 API 密钥")
        print("   3. 在 .env 文件中设置 TWITTER_API_KEY")
    
    print("\n🎯 完整内容生成流程:")
    print("   python scripts/generate_content.py")

def main():
    """主函数"""
    print("📊 generate_article 方法和 OpenAI 接口测试总结")
    print("=" * 60)
    
    # 环境检查
    env_ok = check_environment()
    
    # 方法测试
    method_ok = test_generate_article_method()
    
    # 文件结构检查
    files_ok = check_file_structure()
    
    # 总结
    print("\n📋 测试总结")
    print("=" * 60)
    
    if env_ok and method_ok and files_ok:
        print("🎉 所有基础测试通过!")
        print("✅ 环境配置正确")
        print("✅ generate_article 方法结构完整")
        print("✅ 文件结构完整")
    else:
        print("⚠️  部分测试未通过，请检查上述问题")
    
    # 提供建议
    provide_recommendations()
    
    print("\n🔧 可用的测试脚本:")
    print("   📝 scripts/test_openai_mock.py     - 模拟测试（无需真实API）")
    print("   🔑 scripts/test_openai_simple.py   - 简单API测试")
    print("   🚀 scripts/test_openai_generate.py - 完整功能测试")
    print("   📊 scripts/test_summary.py         - 本测试总结")

if __name__ == "__main__":
    main()