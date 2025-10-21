"""
使用示例 - 英文语音合成服务
演示如何使用TTS服务进行英文文本转语音
"""

import requests
import json
import base64
import os
from datetime import datetime


class TTSClient:
    """TTS客户端类"""
    
    def __init__(self, base_url="http://localhost:5000"):
        self.base_url = base_url
    
    def health_check(self):
        """健康检查"""
        try:
            response = requests.get(f"{self.base_url}/api/health")
            return response.json()
        except Exception as e:
            return {"error": str(e)}
    
    def get_voices(self):
        """获取可用音色"""
        try:
            response = requests.get(f"{self.base_url}/api/voices")
            return response.json()
        except Exception as e:
            return {"error": str(e)}
    
    def synthesize(self, text, voice="Jennifer", format="wav", save_file=False):
        """语音合成"""
        try:
            data = {
                "text": text,
                "voice": voice,
                "format": format,
                "save_file": save_file
            }
            response = requests.post(f"{self.base_url}/api/synthesize", json=data)
            return response.json()
        except Exception as e:
            return {"error": str(e)}
    
    def synthesize_and_download(self, text, voice="Jennifer", format="wav"):
        """语音合成并下载文件"""
        try:
            data = {
                "text": text,
                "voice": voice,
                "format": format
            }
            response = requests.post(f"{self.base_url}/api/synthesize/file", json=data)
            
            if response.headers.get('content-type', '').startswith('audio/'):
                # 保存下载的文件
                filename = f"downloaded_speech_{datetime.now().strftime('%Y%m%d_%H%M%S')}.{format}"
                with open(filename, 'wb') as f:
                    f.write(response.content)
                return {"success": True, "filename": filename}
            else:
                return response.json()
        except Exception as e:
            return {"error": str(e)}
    
    def calculate_cost(self, text):
        """计算成本"""
        try:
            data = {"text": text}
            response = requests.post(f"{self.base_url}/api/cost", json=data)
            return response.json()
        except Exception as e:
            return {"error": str(e)}


def demo_basic_usage():
    """基础使用演示"""
    print("=== 英文语音合成服务演示 ===\n")
    
    # 创建客户端
    client = TTSClient()
    
    # 1. 健康检查
    print("1. 健康检查:")
    health = client.health_check()
    print(json.dumps(health, indent=2, ensure_ascii=False))
    print()
    
    # 2. 获取可用音色
    print("2. 获取可用音色:")
    voices = client.get_voices()
    print(json.dumps(voices, indent=2, ensure_ascii=False))
    print()
    
    # 3. 计算成本
    sample_text = "Hello, this is a demonstration of English text-to-speech service using Qwen TTS."
    print("3. 计算成本:")
    cost_info = client.calculate_cost(sample_text)
    print(json.dumps(cost_info, indent=2, ensure_ascii=False))
    print()
    
    # 4. 语音合成
    print("4. 语音合成:")
    result = client.synthesize(sample_text, voice="Jennifer", save_file=True)
    print(f"合成结果: {result.get('success', False)}")
    if result.get('success'):
        print(f"音频格式: {result.get('format')}")
        print(f"采样率: {result.get('sample_rate')}")
        print(f"音色: {result.get('voice')}")
        print(f"成本: {result.get('cost')} 元")
        if result.get('saved_file'):
            print(f"保存文件: {result.get('saved_file')}")
    else:
        print(f"错误: {result.get('error')}")
    print()


def demo_different_voices():
    """不同音色演示"""
    print("=== 不同音色演示 ===\n")
    
    client = TTSClient()
    text = "Welcome to the world of artificial intelligence and text-to-speech technology."
    
    # 获取可用音色
    voices_response = client.get_voices()
    if voices_response.get('success'):
        voices = voices_response['voices']
        
        print("测试不同音色:")
        for voice_key, voice_name in voices.items():
            print(f"\n音色: {voice_name}")
            result = client.synthesize(text, voice=voice_name)
            if result.get('success'):
                print(f"✓ 合成成功 - 成本: {result.get('cost')} 元")
            else:
                print(f"✗ 合成失败 - {result.get('error')}")
    else:
        print("获取音色列表失败")


def demo_advanced_features():
    """高级功能演示"""
    print("=== 高级功能演示 ===\n")
    
    client = TTSClient()
    text = "This is a demonstration of advanced TTS features including speed, volume, and pitch control."
    
    # 测试不同参数
    test_cases = [
        {"speed": 0.8, "volume": 1.2, "pitch": 1.1, "description": "慢速+高音量+高音调"},
        {"speed": 1.2, "volume": 0.8, "pitch": 0.9, "description": "快速+低音量+低音调"},
        {"speed": 1.0, "volume": 1.0, "pitch": 1.0, "description": "默认参数"},
    ]
    
    for i, params in enumerate(test_cases, 1):
        print(f"{i}. {params['description']}:")
        result = client.synthesize(
            text, 
            voice="Jennifer",
            **{k: v for k, v in params.items() if k != 'description'}
        )
        
        if result.get('success'):
            print(f"✓ 合成成功 - 成本: {result.get('cost')} 元")
        else:
            print(f"✗ 合成失败 - {result.get('error')}")
        print()


def demo_file_download():
    """文件下载演示"""
    print("=== 文件下载演示 ===\n")
    
    client = TTSClient()
    text = "This audio file will be downloaded directly to your local directory."
    
    print("下载音频文件:")
    result = client.synthesize_and_download(text, voice="Jennifer", format="wav")
    
    if result.get('success'):
        print(f"✓ 文件下载成功: {result.get('filename')}")
    else:
        print(f"✗ 下载失败: {result.get('error')}")


def interactive_demo():
    """交互式演示"""
    print("=== 交互式演示 ===\n")
    
    client = TTSClient()
    
    while True:
        print("\n请选择操作:")
        print("1. 语音合成")
        print("2. 计算成本")
        print("3. 查看可用音色")
        print("4. 下载音频文件")
        print("0. 退出")
        
        choice = input("\n请输入选择 (0-4): ").strip()
        
        if choice == "0":
            print("再见!")
            break
        elif choice == "1":
            text = input("请输入要转换的英文文本: ").strip()
            if text:
                voice = input("请输入音色名称 (默认Jennifer): ").strip() or "Jennifer"
                result = client.synthesize(text, voice=voice, save_file=True)
                if result.get('success'):
                    print(f"✓ 合成成功! 成本: {result.get('cost')} 元")
                    if result.get('saved_file'):
                        print(f"文件已保存: {result.get('saved_file')}")
                else:
                    print(f"✗ 合成失败: {result.get('error')}")
        elif choice == "2":
            text = input("请输入要计算成本的文本: ").strip()
            if text:
                cost_info = client.calculate_cost(text)
                if cost_info.get('success'):
                    print(f"文本长度: {cost_info.get('text_length')} 字符")
                    print(f"预估成本: {cost_info.get('cost')} 元")
                else:
                    print(f"✗ 计算失败: {cost_info.get('error')}")
        elif choice == "3":
            voices = client.get_voices()
            if voices.get('success'):
                print("可用音色:")
                for key, name in voices['voices'].items():
                    print(f"  {key}: {name}")
            else:
                print(f"✗ 获取失败: {voices.get('error')}")
        elif choice == "4":
            text = input("请输入要转换的英文文本: ").strip()
            if text:
                voice = input("请输入音色名称 (默认Jennifer): ").strip() or "Jennifer"
                result = client.synthesize_and_download(text, voice=voice)
                if result.get('success'):
                    print(f"✓ 文件下载成功: {result.get('filename')}")
                else:
                    print(f"✗ 下载失败: {result.get('error')}")
        else:
            print("无效选择，请重试")


if __name__ == "__main__":
    print("英文语音合成服务演示程序")
    print("请确保TTS服务已启动 (python app.py)")
    print()
    
    try:
        # 运行各种演示
        demo_basic_usage()
        demo_different_voices()
        demo_advanced_features()
        demo_file_download()
        
        # 交互式演示
        interactive_demo()
        
    except KeyboardInterrupt:
        print("\n程序已退出")
    except Exception as e:
        print(f"程序运行错误: {str(e)}")
