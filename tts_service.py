"""
阿里云通义千问TTS语音合成服务
支持多种TTS模型，通过配置文件灵活切换
"""

import os
import json
import logging
from typing import Optional, Dict, Any
from dotenv import load_dotenv
from dashscope import SpeechSynthesizer
import dashscope
import base64
import io

# 加载环境变量
load_dotenv('config.env')

# 设置API密钥
dashscope.api_key = os.getenv('DASHSCOPE_API_KEY')

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class TTSService:
    """TTS服务类 - 支持多种模型"""
    
    def __init__(self, config_file: str = 'model_config.json'):
        """初始化TTS服务"""
        self.api_key = os.getenv('DASHSCOPE_API_KEY')
        if not self.api_key:
            raise ValueError("请设置DASHSCOPE_API_KEY环境变量")
        
        # 加载模型配置
        self.config_file = config_file
        self.model_configs = self._load_model_config()
        self.current_model = self.model_configs.get('current_model', 'qwen3-tts-flash')
        
        # 获取当前模型配置
        self.current_config = self.model_configs['models'][self.current_model]
        
        logger.info(f"TTS服务初始化完成，当前模型: {self.current_model}")
    
    def _load_model_config(self) -> Dict[str, Any]:
        """加载模型配置文件"""
        try:
            with open(self.config_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            logger.error(f"配置文件 {self.config_file} 不存在")
            raise
        except json.JSONDecodeError as e:
            logger.error(f"配置文件格式错误: {e}")
            raise
    
    def switch_model(self, model_name: str) -> bool:
        """切换TTS模型"""
        if model_name not in self.model_configs['models']:
            logger.error(f"不支持的模型: {model_name}")
            return False
        
        self.current_model = model_name
        self.current_config = self.model_configs['models'][model_name]
        
        # 更新配置文件中的当前模型
        self.model_configs['current_model'] = model_name
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(self.model_configs, f, ensure_ascii=False, indent=2)
            logger.info(f"已切换到模型: {model_name}")
            return True
        except Exception as e:
            logger.error(f"保存配置文件失败: {e}")
            return False
    
    def get_available_voices(self) -> Dict[str, str]:
        """获取可用的音色列表"""
        return self.current_config['voices'].copy()
    
    def get_available_models(self) -> Dict[str, str]:
        """获取可用的模型列表"""
        models = {}
        for model_name, config in self.model_configs['models'].items():
            models[model_name] = config['display_name']
        return models
    
    def get_current_model_info(self) -> Dict[str, Any]:
        """获取当前模型信息"""
        return {
            'name': self.current_model,
            'display_name': self.current_config['display_name'],
            'description': self.current_config['description'],
            'price_per_10k_chars': self.current_config['price_per_10k_chars'],
            'max_text_length': self.current_config['max_text_length'],
            'default_voice': self.current_config['default_voice']
        }
    
    def validate_text(self, text: str) -> bool:
        """验证输入文本"""
        if not text or not text.strip():
            logger.warning("文本内容不能为空")
            return False
        
        # 检查文本长度
        max_length = self.current_config['max_text_length']
        if len(text) > max_length:
            logger.warning(f"文本长度超过限制: {len(text)} > {max_length}")
            return False
        
        return True
    
    def calculate_cost(self, text: str) -> float:
        """计算文本转语音成本（按字符数计费）"""
        char_count = len(text)
        price_per_10k = self.current_config['price_per_10k_chars']
        cost = (char_count / 10000) * price_per_10k
        return round(cost, 4)
    
    def synthesize_speech(self,
                          text: str,
                          voice: str = None,
                          format: str = None,
                          sample_rate: int = None,
                          speed: float = 1.0,
                          volume: float = 1.0,
                          pitch: float = 1.0) -> Dict[str, Any]:
        """
        将文本转换为语音
        
        Args:
            text: 要转换的文本
            voice: 音色名称（可选，默认使用当前模型的默认音色）
            format: 音频格式（可选，默认使用当前模型的默认格式）
            sample_rate: 采样率（可选，默认使用当前模型的默认采样率）
            speed: 语速（1.0为正常速度）
            volume: 音量（1.0为正常音量）
            pitch: 音调（1.0为正常音调）
        
        Returns:
            包含合成结果的字典
        """
        if not self.validate_text(text):
            return {"success": False, "message": "文本内容无效或过长"}
        
        # 使用默认值
        if voice is None:
            voice = self.current_config['default_voice']
        if format is None:
            format = self.current_config['default_format']
        if sample_rate is None:
            sample_rate = self.current_config['default_sample_rate']
        
        # 验证音色
        if voice not in self.current_config['voices']:
            return {"success": False, "message": f"不支持的音色: {voice}"}
        
        try:
            # 计算成本
            cost = self.calculate_cost(text)
            
            logger.info(f"开始合成语音: 模型={self.current_model}, 文本长度={len(text)}, 音色={voice}, 预估成本={cost}元")
            
            # 构建API参数
            api_params = self.current_config['api_parameters'].copy()
            api_params.update({
                'text': text,
                'voice': voice,
                'format': format,
                'sample_rate': sample_rate
            })
            
            # 调用TTS API
            response = SpeechSynthesizer.call(**api_params)
            
            if response.get_response().status_code == 200:
                # 获取音频数据
                audio_data = response.get_audio_data()
                audio_base64 = base64.b64encode(audio_data).decode('utf-8')
                
                logger.info("语音合成成功")
                return {
                    "success": True,
                    "message": "语音合成成功",
                    "audio_data": audio_base64,
                    "cost": cost,
                    "text_length": len(text),
                    "voice": voice,
                    "format": format,
                    "sample_rate": sample_rate,
                    "model": self.current_model
                }
            else:
                error_message = response.get_response().message
                logger.error(f"语音合成失败: {error_message}")
                return {"success": False, "message": f"语音合成过程中发生错误: {error_message}"}
                
        except Exception as e:
            logger.exception(f"语音合成过程中发生异常: {e}")
            return {"success": False, "message": f"语音合成过程中发生错误: {e}"}
    
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
tts_service = TTSService()
