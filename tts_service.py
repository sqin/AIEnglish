"""
阿里云通义千问TTS英文语音合成服务
基于Qwen3-TTS模型实现英文文本转语音功能
"""

import os
import logging
from typing import Optional, Dict, Any
from dotenv import load_dotenv
from dashscope import SpeechSynthesizer
import base64
import io

# 加载环境变量
load_dotenv('config.env.example')

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class QwenTTSService:
    """通义千问TTS服务类"""
    
    def __init__(self):
        """初始化TTS服务"""
        self.api_key = os.getenv('DASHSCOPE_API_KEY')
        if not self.api_key:
            raise ValueError("请设置DASHSCOPE_API_KEY环境变量")
        
        # Qwen3-TTS支持的英文音色
        self.english_voices = {
            'jennifer': 'Jennifer',  # 品牌级、电影质感般美语女声
            'ryan': 'Ryan',          # 节奏拉满，戏感炸裂
            'katerina': 'Katerina',  # 御姐音色，韵律回味十足
            'elias': 'Elias',        # 学科严谨性，叙事技巧
            'cherry': 'Cherry',      # 阳光积极、亲切自然小姐姐
            'serena': 'Serena',      # 温柔小姐姐
            'ethan': 'Ethan',        # 标准普通话，带部分北方口音
            'chelsie': 'Chelsie',    # 二次元虚拟女友
        }
        
        # 默认配置
        self.default_config = {
            'model': 'qwen3-tts-flash',
            'format': 'wav',
            'sample_rate': 22050,
            'voice': 'Jennifer',  # 默认使用Jennifer音色
            'speed': 1.0,
            'volume': 1.0,
            'pitch': 1.0
        }
    
    def get_available_voices(self) -> Dict[str, str]:
        """获取可用的英文音色列表"""
        return self.english_voices.copy()
    
    def validate_text(self, text: str) -> bool:
        """验证输入文本"""
        if not text or not text.strip():
            return False
        
        # 检查文本长度（Qwen3-TTS最大600字符）
        if len(text) > 600:
            logger.warning(f"文本长度超过限制: {len(text)} > 600")
            return False
        
        return True
    
    def calculate_cost(self, text: str) -> float:
        """计算文本转语音成本（按字符数计费）"""
        # 英文字母、标点符号、空格 = 1个字符
        char_count = len(text)
        # Qwen3-TTS价格：0.8元/万字符
        cost = (char_count / 10000) * 0.8
        return round(cost, 4)
    
    def synthesize_speech(self, 
                         text: str, 
                         voice: str = 'Jennifer',
                         format: str = 'wav',
                         sample_rate: int = 22050,
                         speed: float = 1.0,
                         volume: float = 1.0,
                         pitch: float = 1.0) -> Dict[str, Any]:
        """
        将英文文本转换为语音
        
        Args:
            text: 要转换的英文文本
            voice: 音色名称
            format: 音频格式 (wav, mp3)
            sample_rate: 采样率
            speed: 语速 (0.5-2.0)
            volume: 音量 (0.1-2.0)
            pitch: 音调 (0.5-2.0)
        
        Returns:
            包含音频数据和元信息的字典
        """
        try:
            # 验证输入
            if not self.validate_text(text):
                raise ValueError("文本验证失败")
            
            # 验证音色
            if voice not in self.english_voices.values():
                raise ValueError(f"不支持的音色: {voice}")
            
            # 计算成本
            cost = self.calculate_cost(text)
            
            logger.info(f"开始合成语音: 文本长度={len(text)}, 音色={voice}, 预估成本={cost}元")
            
            # 调用TTS API
            response = TextToSpeech.call(
                model=self.default_config['model'],
                text=text,
                voice=voice,
                format=format,
                sample_rate=sample_rate,
                speed=speed,
                volume=volume,
                pitch=pitch
            )
            
            if response.status_code == 200:
                # 获取音频数据
                audio_data = response.get_audio_data()
                
                # 将音频数据转换为base64编码
                audio_base64 = base64.b64encode(audio_data).decode('utf-8')
                
                result = {
                    'success': True,
                    'audio_data': audio_base64,
                    'format': format,
                    'sample_rate': sample_rate,
                    'text_length': len(text),
                    'voice': voice,
                    'cost': cost,
                    'message': '语音合成成功'
                }
                
                logger.info("语音合成成功")
                return result
                
            else:
                error_msg = f"TTS API调用失败: {response.status_code} - {response.message}"
                logger.error(error_msg)
                return {
                    'success': False,
                    'error': error_msg,
                    'message': '语音合成失败'
                }
                
        except Exception as e:
            error_msg = f"语音合成过程中发生错误: {str(e)}"
            logger.error(error_msg)
            return {
                'success': False,
                'error': error_msg,
                'message': '语音合成失败'
            }
    
    def save_audio_to_file(self, audio_base64: str, filename: str) -> bool:
        """将base64编码的音频数据保存为文件"""
        try:
            audio_data = base64.b64decode(audio_base64)
            with open(filename, 'wb') as f:
                f.write(audio_data)
            logger.info(f"音频文件已保存: {filename}")
            return True
        except Exception as e:
            logger.error(f"保存音频文件失败: {str(e)}")
            return False


# 创建全局TTS服务实例
tts_service = QwenTTSService()
