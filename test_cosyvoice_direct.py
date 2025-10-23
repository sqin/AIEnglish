#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
from dotenv import load_dotenv
import dashscope
from dashscope import SpeechSynthesizer

# 加载环境变量
load_dotenv('config.env')

# 设置API密钥
dashscope.api_key = os.getenv('DASHSCOPE_API_KEY')

def test_cosyvoice_api():
    """测试CosyVoice API调用"""
    
    text = "hello, today we are going to learn something about jarring"
    
    print(f"测试文本: {text}")
    print(f"API Key: {os.getenv('DASHSCOPE_API_KEY')[:10]}...")
    
    try:
        # 尝试最简单的CosyVoice调用
        print("尝试CosyVoice v3调用...")
        response = SpeechSynthesizer.call(
            model='cosyvoice-v3',
            text=text,
            voice='longjielidou'
        )
        
        print(f"响应状态码: {response.get_response().status_code}")
        print(f"响应内容: {response.get_response().text}")
        
        if response.get_response().status_code == 200:
            print("成功!")
            audio_data = response.get_audio_data()
            print(f"音频数据长度: {len(audio_data)} 字节")
        else:
            print("失败!")
            
    except Exception as e:
        print(f"异常: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_cosyvoice_api()
