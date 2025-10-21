"""
简单测试脚本 - 验证TTS服务功能
"""

import os
import sys

def check_dependencies():
    """检查依赖是否安装"""
    print("检查依赖...")
    
    required_packages = [
        'dashscope',
        'flask', 
        'requests',
        'python-dotenv'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
            print(f"✓ {package}")
        except ImportError:
            print(f"✗ {package}")
            missing_packages.append(package)
    
    if missing_packages:
        print(f"\n缺少依赖: {', '.join(missing_packages)}")
        print("请运行: pip install -r requirements.txt")
        return False
    
    print("所有依赖已安装!")
    return True

def check_config():
    """检查配置文件"""
    print("\n检查配置...")
    
    # 检查.env文件
    if os.path.exists('.env'):
        print("✓ .env文件存在")
        
        # 检查API密钥
        from dotenv import load_dotenv
        load_dotenv()
        
        api_key = os.getenv('DASHSCOPE_API_KEY')
        if api_key and api_key != 'your_api_key_here':
            print("✓ API密钥已配置")
            return True
        else:
            print("✗ API密钥未正确配置")
            print("请在.env文件中设置DASHSCOPE_API_KEY")
            return False
    else:
        print("✗ .env文件不存在")
        print("请复制config.env.example为.env并配置API密钥")
        return False

def test_tts_service():
    """测试TTS服务"""
    print("\n测试TTS服务...")
    
    try:
        from tts_service import QwenTTSService
        
        # 创建服务实例
        tts = QwenTTSService()
        print("✓ TTS服务初始化成功")
        
        # 测试音色列表
        voices = tts.get_available_voices()
        print(f"✓ 可用音色: {len(voices)}个")
        
        # 测试文本验证
        test_text = "Hello, this is a test."
        if tts.validate_text(test_text):
            print("✓ 文本验证功能正常")
        else:
            print("✗ 文本验证功能异常")
            return False
        
        # 测试成本计算
        cost = tts.calculate_cost(test_text)
        print(f"✓ 成本计算功能正常: {cost}元")
        
        print("TTS服务测试通过!")
        return True
        
    except Exception as e:
        print(f"✗ TTS服务测试失败: {str(e)}")
        return False

def test_api_endpoints():
    """测试API端点"""
    print("\n测试API端点...")
    
    try:
        import requests
        
        base_url = "http://localhost:5000"
        
        # 测试健康检查
        try:
            response = requests.get(f"{base_url}/api/health", timeout=5)
            if response.status_code == 200:
                print("✓ 健康检查端点正常")
            else:
                print(f"✗ 健康检查端点异常: {response.status_code}")
                return False
        except requests.exceptions.ConnectionError:
            print("✗ 无法连接到API服务")
            print("请先启动服务: python app.py")
            return False
        
        # 测试音色列表端点
        response = requests.get(f"{base_url}/api/voices")
        if response.status_code == 200:
            print("✓ 音色列表端点正常")
        else:
            print(f"✗ 音色列表端点异常: {response.status_code}")
            return False
        
        print("API端点测试通过!")
        return True
        
    except Exception as e:
        print(f"✗ API端点测试失败: {str(e)}")
        return False

def main():
    """主函数"""
    print("=== TTS服务测试程序 ===\n")
    
    # 检查依赖
    if not check_dependencies():
        sys.exit(1)
    
    # 检查配置
    if not check_config():
        sys.exit(1)
    
    # 测试TTS服务
    if not test_tts_service():
        sys.exit(1)
    
    # 测试API端点
    if not test_api_endpoints():
        print("\n注意: API服务可能未启动")
        print("请运行: python app.py")
    
    print("\n=== 测试完成 ===")
    print("服务已准备就绪!")
    print("\n使用方法:")
    print("1. 启动服务: python app.py")
    print("2. 运行演示: python demo.py")
    print("3. 查看文档: README.md")

if __name__ == "__main__":
    main()
