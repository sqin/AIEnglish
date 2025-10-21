#!/usr/bin/env python3
"""
快速启动脚本
自动检查环境并启动TTS服务
"""

import os
import sys
import subprocess
import time

def check_python_version():
    """检查Python版本"""
    if sys.version_info < (3, 7):
        print("错误: 需要Python 3.7或更高版本")
        return False
    print(f"✓ Python版本: {sys.version}")
    return True

def install_dependencies():
    """安装依赖"""
    print("安装依赖包...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✓ 依赖安装完成")
        return True
    except subprocess.CalledProcessError:
        print("✗ 依赖安装失败")
        return False

def setup_config():
    """设置配置文件"""
    if not os.path.exists('.env'):
        if os.path.exists('config.env.example'):
            print("创建配置文件...")
            with open('config.env.example', 'r', encoding='utf-8') as f:
                content = f.read()
            with open('.env', 'w', encoding='utf-8') as f:
                f.write(content)
            print("✓ 配置文件已创建")
            print("⚠️  请编辑.env文件设置您的API密钥")
            return False
        else:
            print("✗ 配置文件模板不存在")
            return False
    else:
        print("✓ 配置文件已存在")
        return True

def check_api_key():
    """检查API密钥"""
    from dotenv import load_dotenv
    load_dotenv()
    
    api_key = os.getenv('DASHSCOPE_API_KEY')
    if not api_key or api_key == 'your_api_key_here':
        print("⚠️  API密钥未设置")
        print("请在.env文件中设置DASHSCOPE_API_KEY")
        return False
    
    print("✓ API密钥已配置")
    return True

def start_service():
    """启动服务"""
    print("\n启动TTS服务...")
    print("服务地址: http://localhost:5000")
    print("按Ctrl+C停止服务")
    print("-" * 50)
    
    try:
        subprocess.run([sys.executable, "app.py"])
    except KeyboardInterrupt:
        print("\n服务已停止")

def main():
    """主函数"""
    print("=== 阿里云通义千问TTS服务启动器 ===\n")
    
    # 检查Python版本
    if not check_python_version():
        sys.exit(1)
    
    # 安装依赖
    if not install_dependencies():
        sys.exit(1)
    
    # 设置配置
    config_ready = setup_config()
    
    # 检查API密钥
    if config_ready and not check_api_key():
        print("\n请先配置API密钥，然后重新运行此脚本")
        sys.exit(1)
    
    # 启动服务
    start_service()

if __name__ == "__main__":
    main()
