#!/usr/bin/env python3
"""
模型切换工具
用于快速切换TTS模型
"""

import json
import sys
import os

def load_config():
    """加载配置文件"""
    try:
        with open('model_config.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print("❌ 配置文件 model_config.json 不存在")
        return None
    except json.JSONDecodeError as e:
        print(f"❌ 配置文件格式错误: {e}")
        return None

def save_config(config):
    """保存配置文件"""
    try:
        with open('model_config.json', 'w', encoding='utf-8') as f:
            json.dump(config, f, ensure_ascii=False, indent=2)
        return True
    except Exception as e:
        print(f"❌ 保存配置文件失败: {e}")
        return False

def list_models():
    """列出所有可用模型"""
    config = load_config()
    if not config:
        return
    
    print("📋 可用模型列表:")
    print("-" * 50)
    
    for model_name, model_info in config['models'].items():
        current = " (当前)" if model_name == config['current_model'] else ""
        print(f"🔹 {model_name}{current}")
        print(f"   显示名称: {model_info['display_name']}")
        print(f"   描述: {model_info['description']}")
        print(f"   价格: {model_info['price_per_10k_chars']}元/万字符")
        print(f"   最大文本长度: {model_info['max_text_length']}字符")
        print(f"   默认音色: {model_info['default_voice']}")
        print()

def switch_model(model_name):
    """切换模型"""
    config = load_config()
    if not config:
        return False
    
    if model_name not in config['models']:
        print(f"❌ 不支持的模型: {model_name}")
        print("💡 使用 'python switch_model.py list' 查看可用模型")
        return False
    
    old_model = config['current_model']
    config['current_model'] = model_name
    
    if save_config(config):
        print(f"✅ 已成功从 {old_model} 切换到 {model_name}")
        print(f"📝 新模型信息:")
        model_info = config['models'][model_name]
        print(f"   显示名称: {model_info['display_name']}")
        print(f"   描述: {model_info['description']}")
        print(f"   默认音色: {model_info['default_voice']}")
        return True
    else:
        return False

def show_current():
    """显示当前模型信息"""
    config = load_config()
    if not config:
        return
    
    current_model = config['current_model']
    model_info = config['models'][current_model]
    
    print(f"🎯 当前模型: {current_model}")
    print(f"📝 显示名称: {model_info['display_name']}")
    print(f"📄 描述: {model_info['description']}")
    print(f"💰 价格: {model_info['price_per_10k_chars']}元/万字符")
    print(f"📏 最大文本长度: {model_info['max_text_length']}字符")
    print(f"🎵 默认音色: {model_info['default_voice']}")
    print(f"🎨 可用音色: {', '.join(model_info['voices'].keys())}")

def main():
    """主函数"""
    if len(sys.argv) < 2:
        print("🔧 TTS模型切换工具")
        print("=" * 30)
        print("用法:")
        print("  python switch_model.py list          # 列出所有可用模型")
        print("  python switch_model.py current       # 显示当前模型信息")
        print("  python switch_model.py switch <模型名> # 切换到指定模型")
        print()
        print("示例:")
        print("  python switch_model.py switch sambert-zhichu-v1")
        print("  python switch_model.py switch cosyvoice-v3")
        return
    
    command = sys.argv[1].lower()
    
    if command == 'list':
        list_models()
    elif command == 'current':
        show_current()
    elif command == 'switch':
        if len(sys.argv) < 3:
            print("❌ 请指定要切换的模型名称")
            print("💡 使用 'python switch_model.py list' 查看可用模型")
            return
        model_name = sys.argv[2]
        switch_model(model_name)
    else:
        print(f"❌ 未知命令: {command}")
        print("💡 使用 'python switch_model.py' 查看帮助")

if __name__ == "__main__":
    main()
