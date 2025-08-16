#!/usr/bin/env python3
"""
测试脚本 - 生成示例内容（不需要API密钥）
"""

from pathlib import Path
from datetime import datetime
import random

CONTENT_DIR = Path(__file__).parent.parent / 'content'

# 示例话题
SAMPLE_TOPICS = [
    {
        'title_en': 'AI Revolution in 2024',
        'title_zh': '2024年AI革命',
        'content_en': """## The Rise of Artificial Intelligence

Artificial Intelligence continues to transform our world in unprecedented ways. From ChatGPT to autonomous vehicles, AI is becoming an integral part of our daily lives.

### Key Developments

1. **Large Language Models**: The evolution of GPT models has revolutionized natural language processing.
2. **Computer Vision**: Advanced image recognition is enabling new applications in healthcare and security.
3. **Robotics**: AI-powered robots are becoming more sophisticated and versatile.

### Impact on Society

The widespread adoption of AI is creating both opportunities and challenges:

- **Productivity Gains**: Businesses are seeing significant efficiency improvements
- **Job Market Changes**: New roles are emerging while others are being automated
- **Ethical Considerations**: Questions about bias, privacy, and control are becoming increasingly important

### Looking Forward

As we move forward, it's crucial to develop AI responsibly, ensuring that its benefits are distributed equitably while addressing potential risks.

The future of AI is bright, but it requires careful navigation to ensure positive outcomes for all of humanity.""",
        'content_zh': """## 人工智能的崛起

人工智能继续以前所未有的方式改变着我们的世界。从ChatGPT到自动驾驶汽车，AI正在成为我们日常生活中不可或缺的一部分。

### 关键发展

1. **大型语言模型**：GPT模型的演进彻底改变了自然语言处理领域。
2. **计算机视觉**：先进的图像识别技术正在医疗和安全领域开启新应用。
3. **机器人技术**：AI驱动的机器人变得更加复杂和多功能。

### 对社会的影响

AI的广泛应用既带来了机遇也带来了挑战：

- **生产力提升**：企业正在看到显著的效率改善
- **就业市场变化**：新的岗位正在出现，而其他岗位正在被自动化
- **伦理考量**：关于偏见、隐私和控制的问题变得越来越重要

### 展望未来

随着我们向前发展，负责任地开发AI至关重要，确保其利益得到公平分配，同时解决潜在风险。

AI的未来是光明的，但需要谨慎导航以确保为全人类带来积极成果。"""
    },
    {
        'title_en': 'Climate Action Now',
        'title_zh': '立即行动应对气候变化',
        'content_en': """## Global Climate Emergency

The urgency of climate action has never been more apparent. Recent extreme weather events worldwide underscore the need for immediate and decisive action.

### Current Situation

- Record-breaking temperatures across continents
- Unprecedented wildfires and floods
- Accelerating ice sheet melting

### Solutions in Progress

1. **Renewable Energy**: Solar and wind power are becoming increasingly cost-effective
2. **Electric Vehicles**: The transition to EVs is accelerating globally
3. **Carbon Capture**: New technologies are emerging to remove CO2 from the atmosphere

### What You Can Do

Every individual action counts in the fight against climate change:

- Reduce energy consumption
- Choose sustainable transportation
- Support climate-friendly policies and businesses

The time for action is now. Together, we can make a difference.""",
        'content_zh': """## 全球气候紧急状态

气候行动的紧迫性从未如此明显。最近世界各地的极端天气事件凸显了立即采取果断行动的必要性。

### 当前形势

- 各大洲创纪录的高温
- 前所未有的野火和洪水
- 冰盖融化加速

### 正在进行的解决方案

1. **可再生能源**：太阳能和风能正变得越来越具有成本效益
2. **电动汽车**：全球向电动汽车的转型正在加速
3. **碳捕获**：新技术正在出现，以从大气中去除二氧化碳

### 您能做什么

在应对气候变化的斗争中，每个人的行动都很重要：

- 减少能源消耗
- 选择可持续交通方式
- 支持气候友好的政策和企业

行动的时候到了。团结起来，我们可以创造改变。"""
    },
    {
        'title_en': 'The Future of Work',
        'title_zh': '工作的未来',
        'content_en': """## Reimagining the Workplace

The concept of work is undergoing a fundamental transformation. Remote work, automation, and changing employee expectations are reshaping how we think about careers.

### Key Trends

1. **Hybrid Work Models**: The blend of remote and office work is becoming the norm
2. **Skills Revolution**: Continuous learning is now essential for career success
3. **Gig Economy Growth**: Freelance and contract work continues to expand

### Challenges and Opportunities

The evolving workplace presents both challenges and opportunities:

- Work-life balance improvements
- Geographic flexibility
- Need for new management approaches
- Digital divide concerns

### Preparing for Tomorrow

To thrive in the future of work:

- Embrace lifelong learning
- Develop digital literacy
- Build adaptability and resilience
- Focus on uniquely human skills

The future of work is being written now, and we all have a role in shaping it.""",
        'content_zh': """## 重新构想工作场所

工作的概念正在经历根本性的转变。远程工作、自动化和不断变化的员工期望正在重塑我们对职业的看法。

### 主要趋势

1. **混合工作模式**：远程和办公室工作的结合正在成为常态
2. **技能革命**：持续学习现在对职业成功至关重要
3. **零工经济增长**：自由职业和合同工作继续扩大

### 挑战与机遇

不断发展的工作场所既带来挑战也带来机遇：

- 工作生活平衡的改善
- 地理灵活性
- 需要新的管理方法
- 数字鸿沟问题

### 为明天做准备

要在未来的工作中蓬勃发展：

- 拥抱终身学习
- 发展数字素养
- 建立适应性和韧性
- 专注于独特的人类技能

工作的未来正在书写中，我们都在塑造它的过程中扮演着角色。"""
    }
]

def create_sample_content():
    """创建示例内容"""
    
    # 确保目录存在
    for lang in ['en', 'zh']:
        posts_dir = CONTENT_DIR / lang / 'posts'
        posts_dir.mkdir(parents=True, exist_ok=True)
    
    date = datetime.now()
    
    for i, topic in enumerate(SAMPLE_TOPICS):
        # 创建英文文章
        en_filename = f"{date.strftime('%Y-%m-%d')}-sample-{i+1}.md"
        en_filepath = CONTENT_DIR / 'en' / 'posts' / en_filename
        
        en_frontmatter = f"""---
title: "{topic['title_en']}"
date: {date.isoformat()}
draft: false
tags: ["trending", "sample", "demo"]
categories: ["Sample Content"]
---"""
        
        with open(en_filepath, 'w', encoding='utf-8') as f:
            f.write(en_frontmatter)
            f.write('\n\n')
            f.write(topic['content_en'])
            f.write('\n\n')
            f.write("""
<!-- Ad Placeholder -->
<div style="background: #f0f0f0; padding: 20px; text-align: center; margin: 20px 0;">
    [Monetag Ad Space]
</div>
""")
        
        print(f"✅ 创建英文文章: {en_filepath}")
        
        # 创建中文文章
        zh_filename = f"{date.strftime('%Y-%m-%d')}-sample-{i+1}.md"
        zh_filepath = CONTENT_DIR / 'zh' / 'posts' / zh_filename
        
        zh_frontmatter = f"""---
title: "{topic['title_zh']}"
date: {date.isoformat()}
draft: false
tags: ["热门", "示例", "演示"]
categories: ["示例内容"]
---"""
        
        with open(zh_filepath, 'w', encoding='utf-8') as f:
            f.write(zh_frontmatter)
            f.write('\n\n')
            f.write(topic['content_zh'])
            f.write('\n\n')
            f.write("""
<!-- 广告占位符 -->
<div style="background: #f0f0f0; padding: 20px; text-align: center; margin: 20px 0;">
    [Monetag 广告位]
</div>
""")
        
        print(f"✅ 创建中文文章: {zh_filepath}")
    
    print(f"\n✨ 成功创建 {len(SAMPLE_TOPICS)} 篇双语示例文章！")
    print("\n现在可以运行 'hugo server' 查看网站效果")

if __name__ == "__main__":
    create_sample_content()
