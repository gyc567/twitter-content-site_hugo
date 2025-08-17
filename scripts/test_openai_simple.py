#!/usr/bin/env python3
"""
简单的 OpenAI API 测试脚本
测试基本的 API 连接和文本生成功能
"""

import os
from dotenv import load_dotenv
import openai

# 加载环境变量
load_dotenv()

def test_simple_openai():
    """简单测试 OpenAI API 和备用AI服务"""
    print("🔍 测试 OpenAI API 和备用AI服务基本功能...")
    
    api_key = os.environ.get('OPENAI_API_KEY')
    backup_api_key = os.environ.get('AI_API_KEY')
    backup_base_url = os.environ.get('AI_BASE_URL')
    
    # 检查主要 API 密钥
    primary_available = api_key and not api_key.startswith('sk-1234') and api_key != "your_openai_api_key_here"
    backup_available = backup_api_key and backup_base_url and not backup_api_key.startswith('sk-backup-1234')
    
    if not primary_available and not backup_available:
        print("❌ 主要和备用AI服务都未正确配置")
        print(f"OpenAI密钥: {api_key[:20] + '...' if api_key else '未设置'}")
        print(f"备用AI密钥: {backup_api_key[:20] + '...' if backup_api_key else '未设置'}")
        print(f"备用AI地址: {backup_base_url or '未设置'}")
        print("\n💡 请配置至少一个AI服务:")
        print("   OpenAI: 访问 https://platform.openai.com/api-keys")
        print("   或配置备用AI服务 (如 DeepSeek, 通义千问等)")
        print("\n🎭 您可以运行 'python scripts/test_openai_mock.py' 进行模拟测试")
        return False
    
    if primary_available:
        print("✅ OpenAI API 密钥已配置")
    else:
        print("⚠️  OpenAI API 密钥未配置或使用示例值")
    
    if backup_available:
        print(f"✅ 备用AI服务已配置: {backup_base_url}")
    else:
        print("⚠️  备用AI服务未配置或使用示例值")
    
    # 尝试测试主要服务
    if primary_available:
        try:
            print("\n🤖 测试主要OpenAI服务...")
            client = openai.OpenAI(api_key=api_key)
            print("✅ OpenAI 客户端初始化成功")
        
            # 测试简单的文本生成
            print("  🤖 测试文本生成...")
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": "Write a short paragraph about Bitcoin in exactly 50 words."}
                ],
                temperature=0.7,
                max_tokens=100
            )
            
            generated_text = response.choices[0].message.content
            print("  ✅ 主要OpenAI服务测试成功!")
            print(f"  📝 生成的内容: {generated_text}")
            print(f"  📊 使用的模型: gpt-3.5-turbo")
            print(f"  🔢 Token 使用情况: {response.usage.total_tokens if hasattr(response, 'usage') else '未知'}")
            
            return True
        
        except openai.AuthenticationError:
            print("  ❌ OpenAI API 密钥认证失败")
            print("  请检查您的 OpenAI API 密钥是否正确")
        except openai.RateLimitError:
            print("  ❌ OpenAI API 调用频率限制")
            print("  请稍后再试或检查您的 API 配额")
        except openai.APIError as e:
            print(f"  ❌ OpenAI API 错误: {e}")
        except Exception as e:
            print(f"  ❌ OpenAI 测试未知错误: {e}")
    
    # 尝试测试备用服务
    if backup_available:
        try:
            print(f"\n🔄 测试备用AI服务 ({backup_base_url})...")
            backup_client = openai.OpenAI(
                api_key=backup_api_key,
                base_url=backup_base_url
            )
            print("  ✅ 备用AI客户端初始化成功")
            
            # 测试备用服务的文本生成
            print("  🤖 测试备用服务文本生成...")
            response = backup_client.chat.completions.create(
                model="deepseek-chat",  # 常见的备用模型名
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": "Write a short paragraph about Bitcoin in exactly 50 words."}
                ],
                temperature=0.7,
                max_tokens=100
            )
            
            generated_text = response.choices[0].message.content
            print("  ✅ 备用AI服务测试成功!")
            print(f"  📝 生成的内容: {generated_text}")
            print(f"  📊 使用的模型: deepseek-chat")
            print(f"  🔢 Token 使用情况: {response.usage.total_tokens if hasattr(response, 'usage') else '未知'}")
            
            return True
            
        except Exception as e:
            print(f"  ❌ 备用AI服务测试失败: {e}")
    
    return False

def test_chinese_generation():
    """测试中文内容生成"""
    print("\n🇨🇳 测试中文内容生成...")
    
    api_key = os.environ.get('OPENAI_API_KEY')
    backup_api_key = os.environ.get('AI_API_KEY')
    backup_base_url = os.environ.get('AI_BASE_URL')
    
    # 尝试主要服务
    if api_key and not api_key.startswith('sk-1234'):
        try:
            print("  🤖 使用主要OpenAI服务测试中文生成...")
            client = openai.OpenAI(api_key=api_key)
            
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "你是一个专业的中文内容创作助手。"},
                    {"role": "user", "content": "请用50个字简单介绍一下比特币。"}
                ],
                temperature=0.7,
                max_tokens=100
            )
            
            generated_text = response.choices[0].message.content
            print("  ✅ 主要服务中文内容生成成功!")
            print(f"  📝 生成的内容: {generated_text}")
            return
            
        except Exception as e:
            print(f"  ❌ 主要服务中文生成失败: {e}")
    
    # 尝试备用服务
    if backup_api_key and backup_base_url and not backup_api_key.startswith('sk-backup-1234'):
        try:
            print("  🔄 使用备用AI服务测试中文生成...")
            backup_client = openai.OpenAI(
                api_key=backup_api_key,
                base_url=backup_base_url
            )
            
            response = backup_client.chat.completions.create(
                model="deepseek-chat",
                messages=[
                    {"role": "system", "content": "你是一个专业的中文内容创作助手。"},
                    {"role": "user", "content": "请用50个字简单介绍一下比特币。"}
                ],
                temperature=0.7,
                max_tokens=100
            )
            
            generated_text = response.choices[0].message.content
            print("  ✅ 备用服务中文内容生成成功!")
            print(f"  📝 生成的内容: {generated_text}")
            return
            
        except Exception as e:
            print(f"  ❌ 备用服务中文生成失败: {e}")
    
    print("  ⏭️  跳过中文测试（需要有效的 API 密钥）")

def main():
    """主函数"""
    print("🚀 OpenAI API 简单测试")
    print("=" * 50)
    
    # 基本 API 测试
    success = test_simple_openai()
    
    if success:
        # 中文生成测试
        test_chinese_generation()
        
        print("\n" + "=" * 50)
        print("🎉 OpenAI API 测试完成!")
        print("✅ API 连接正常，可以进行内容生成")
        print("\n💡 现在您可以运行完整的内容生成脚本:")
        print("   python scripts/generate_content.py")
    else:
        print("\n" + "=" * 50)
        print("⚠️  OpenAI API 测试未通过")
        print("🎭 建议运行模拟测试: python scripts/test_openai_mock.py")

if __name__ == "__main__":
    main()