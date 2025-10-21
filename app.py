"""
Flask API服务 - 英文语音合成接口
提供RESTful API接口用于英文文本转语音
"""

from flask import Flask, request, jsonify, send_file
import os
import logging
from datetime import datetime
import uuid
from tts_service import tts_service

# 创建Flask应用
app = Flask(__name__)

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 创建输出目录
OUTPUT_DIR = "audio_outputs"
if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)


@app.route('/api/health', methods=['GET'])
def health_check():
    """健康检查接口"""
    return jsonify({
        'status': 'healthy',
        'service': 'Qwen TTS English Service',
        'timestamp': datetime.now().isoformat()
    })


@app.route('/api/voices', methods=['GET'])
def get_voices():
    """获取可用的英文音色列表"""
    try:
        voices = tts_service.get_available_voices()
        return jsonify({
            'success': True,
            'voices': voices,
            'count': len(voices),
            'message': '获取音色列表成功'
        })
    except Exception as e:
        logger.error(f"获取音色列表失败: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e),
            'message': '获取音色列表失败'
        }), 500


@app.route('/api/synthesize', methods=['POST'])
def synthesize_speech():
    """
    英文文本转语音接口
    
    请求参数:
    {
        "text": "要转换的英文文本",
        "voice": "音色名称 (可选，默认Jennifer)",
        "format": "音频格式 (可选，默认wav)",
        "sample_rate": "采样率 (可选，默认22050)",
        "speed": "语速 (可选，默认1.0)",
        "volume": "音量 (可选，默认1.0)",
        "pitch": "音调 (可选，默认1.0)",
        "save_file": "是否保存文件 (可选，默认false)"
    }
    """
    try:
        # 获取请求数据
        data = request.get_json()
        
        if not data:
            return jsonify({
                'success': False,
                'error': '请求数据不能为空',
                'message': '请求参数错误'
            }), 400
        
        # 验证必需参数
        text = data.get('text')
        if not text:
            return jsonify({
                'success': False,
                'error': 'text参数不能为空',
                'message': '请求参数错误'
            }), 400
        
        # 获取可选参数
        voice = data.get('voice', 'Jennifer')
        format = data.get('format', 'wav')
        sample_rate = data.get('sample_rate', 22050)
        speed = data.get('speed', 1.0)
        volume = data.get('volume', 1.0)
        pitch = data.get('pitch', 1.0)
        save_file = data.get('save_file', False)
        
        logger.info(f"收到语音合成请求: 文本长度={len(text)}, 音色={voice}")
        
        # 调用TTS服务
        result = tts_service.synthesize_speech(
            text=text,
            voice=voice,
            format=format,
            sample_rate=sample_rate,
            speed=speed,
            volume=volume,
            pitch=pitch
        )
        
        # 如果需要保存文件
        if save_file and result['success']:
            filename = f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{uuid.uuid4().hex[:8]}.{format}"
            filepath = os.path.join(OUTPUT_DIR, filename)
            
            if tts_service.save_audio_to_file(result['audio_data'], filepath):
                result['saved_file'] = filename
                result['file_path'] = filepath
        
        # 返回结果
        if result['success']:
            return jsonify(result)
        else:
            return jsonify(result), 500
            
    except Exception as e:
        logger.error(f"语音合成接口错误: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e),
            'message': '服务器内部错误'
        }), 500


@app.route('/api/synthesize/file', methods=['POST'])
def synthesize_and_download():
    """
    英文文本转语音并直接下载文件
    
    请求参数同 /api/synthesize
    """
    try:
        # 获取请求数据
        data = request.get_json()
        
        if not data or not data.get('text'):
            return jsonify({
                'success': False,
                'error': 'text参数不能为空',
                'message': '请求参数错误'
            }), 400
        
        # 获取参数
        text = data['text']
        voice = data.get('voice', 'Jennifer')
        format = data.get('format', 'wav')
        sample_rate = data.get('sample_rate', 22050)
        speed = data.get('speed', 1.0)
        volume = data.get('volume', 1.0)
        pitch = data.get('pitch', 1.0)
        
        logger.info(f"收到语音合成下载请求: 文本长度={len(text)}, 音色={voice}")
        
        # 调用TTS服务
        result = tts_service.synthesize_speech(
            text=text,
            voice=voice,
            format=format,
            sample_rate=sample_rate,
            speed=speed,
            volume=volume,
            pitch=pitch
        )
        
        if result['success']:
            # 生成文件名
            filename = f"speech_{datetime.now().strftime('%Y%m%d_%H%M%S')}.{format}"
            filepath = os.path.join(OUTPUT_DIR, filename)
            
            # 保存文件
            if tts_service.save_audio_to_file(result['audio_data'], filepath):
                # 返回文件下载
                return send_file(
                    filepath,
                    as_attachment=True,
                    download_name=filename,
                    mimetype=f'audio/{format}'
                )
            else:
                return jsonify({
                    'success': False,
                    'error': '保存音频文件失败',
                    'message': '文件保存失败'
                }), 500
        else:
            return jsonify(result), 500
            
    except Exception as e:
        logger.error(f"语音合成下载接口错误: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e),
            'message': '服务器内部错误'
        }), 500


@app.route('/api/cost', methods=['POST'])
def calculate_cost():
    """计算文本转语音成本"""
    try:
        data = request.get_json()
        
        if not data or not data.get('text'):
            return jsonify({
                'success': False,
                'error': 'text参数不能为空',
                'message': '请求参数错误'
            }), 400
        
        text = data['text']
        cost = tts_service.calculate_cost(text)
        
        return jsonify({
            'success': True,
            'text_length': len(text),
            'cost': cost,
            'currency': 'CNY',
            'message': '成本计算成功'
        })
        
    except Exception as e:
        logger.error(f"成本计算接口错误: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e),
            'message': '服务器内部错误'
        }), 500


@app.errorhandler(404)
def not_found(error):
    """404错误处理"""
    return jsonify({
        'success': False,
        'error': '接口不存在',
        'message': '请检查请求路径'
    }), 404


@app.errorhandler(500)
def internal_error(error):
    """500错误处理"""
    return jsonify({
        'success': False,
        'error': '服务器内部错误',
        'message': '请联系管理员'
    }), 500


if __name__ == '__main__':
    # 从环境变量获取配置
    host = os.getenv('HOST', '0.0.0.0')
    port = int(os.getenv('PORT', 5000))
    debug = os.getenv('DEBUG', 'True').lower() == 'true'
    
    logger.info(f"启动TTS服务: {host}:{port}")
    app.run(host=host, port=port, debug=debug)
