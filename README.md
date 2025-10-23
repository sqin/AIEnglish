# 阿里云通义千问TTS语音合成服务

基于阿里云通义千问TTS API的Python语音合成服务，支持多种TTS模型，通过配置文件灵活切换。

## ✨ 特性

- 🎯 **多模型支持**: 支持Sambert、CosyVoice等多种TTS模型
- 🔧 **灵活配置**: 通过JSON配置文件管理模型参数
- 🚀 **RESTful API**: 提供完整的HTTP API接口
- 💰 **成本计算**: 实时计算语音合成成本
- 🎵 **多音色支持**: 每个模型支持多种音色选择
- 📊 **详细日志**: 完整的操作日志记录
- 🔄 **模型切换**: 支持运行时动态切换模型

## 📋 支持的模型

### Sambert 知初 (sambert-zhichu-v1)
- **描述**: 阿里云Sambert模型，中文语音合成
- **价格**: 0.1元/万字符
- **最大文本长度**: 600字符
- **音色**: zhichu, zhijiang, zhimeng, zhixia, zhixuan, zhiyan, zhiya, zhiyu

### CosyVoice v3 (cosyvoice-v3)
- **描述**: 阿里云CosyVoice v3模型，高质量英文语音合成
- **价格**: 0.4元/万字符
- **最大文本长度**: 2000字符
- **音色**: longjielidou, longxiaochun, loongstella, longyue, longshuo, longfei, longxiaobai, longlaotie

## 🚀 快速开始

### 1. 环境配置

复制环境变量模板文件：
```bash
cp config.env.example config.env
```

编辑 `config.env` 文件，设置您的API密钥：
```env
DASHSCOPE_API_KEY=your_api_key_here
HOST=0.0.0.0
PORT=5000
DEBUG=True
```

### 2. 安装依赖

```bash
pip install -r requirements.txt
```

### 3. 启动服务

```bash
python app.py
```

服务将在 `http://localhost:5000` 启动。

## 🔧 模型切换

### 使用切换工具

```bash
# 查看所有可用模型
python switch_model.py list

# 查看当前模型信息
python switch_model.py current

# 切换到指定模型
python switch_model.py switch sambert-zhichu-v1
python switch_model.py switch cosyvoice-v3
```

### 使用API切换

```bash
# 获取所有模型
curl http://localhost:5000/api/models

# 获取当前模型信息
curl http://localhost:5000/api/model/info

# 切换模型
curl -X POST http://localhost:5000/api/models/sambert-zhichu-v1
```

## 📡 API接口

### 健康检查
```bash
GET /api/health
```

### 获取模型列表
```bash
GET /api/models
```

### 获取当前模型信息
```bash
GET /api/model/info
```

### 切换模型
```bash
POST /api/models/{model_name}
```

### 获取音色列表
```bash
GET /api/voices
```

### 语音合成
```bash
POST /api/synthesize
Content-Type: application/json

{
    "text": "Hello, world!",
    "voice": "zhichu",
    "format": "wav",
    "sample_rate": 22050
}
```

### 下载音频文件
```bash
GET /api/download/{filename}
```

## 📝 配置文件说明

### model_config.json

模型配置文件包含所有支持的TTS模型信息：

```json
{
  "models": {
    "sambert-zhichu-v1": {
      "name": "sambert-zhichu-v1",
      "display_name": "Sambert 知初",
      "description": "阿里云Sambert模型，中文语音合成",
      "price_per_10k_chars": 0.1,
      "max_text_length": 600,
      "voices": {
        "zhichu": "知初音色",
        "zhijiang": "知江音色"
      },
      "default_voice": "zhichu",
      "supported_formats": ["wav", "mp3"],
      "default_format": "wav",
      "supported_sample_rates": [16000, 22050, 44100],
      "default_sample_rate": 22050,
      "api_parameters": {
        "model": "sambert-zhichu-v1",
        "format": "wav",
        "sample_rate": 22050
      }
    }
  },
  "current_model": "sambert-zhichu-v1"
}
```

## 🧪 测试

### 使用测试脚本

```bash
# 测试服务功能
python test_service.py

# 测试语音合成
python demo.py
```

### 使用curl测试

```bash
# 健康检查
curl http://localhost:5000/api/health

# 语音合成
curl -X POST http://localhost:5000/api/synthesize \
  -H "Content-Type: application/json" \
  -d '{"text": "Hello, world，Now i run on the pi!", "voice": "zhichu"}'
```

## 📁 项目结构

```
aienglish/
├── app.py                 # Flask应用主文件
├── tts_service.py         # TTS服务核心逻辑
├── demo.py               # 演示脚本
├── test_service.py       # 测试脚本
├── switch_model.py       # 模型切换工具
├── start.py              # 快速启动脚本
├── requirements.txt       # Python依赖
├── config.env.example    # 环境变量模板
├── config.env            # 环境变量配置
├── model_config.json     # 模型配置文件
└── README.md            # 项目说明
```

## 🔧 开发

### 添加新模型

1. 在 `model_config.json` 中添加新模型配置
2. 确保API参数正确
3. 测试新模型功能

### 自定义配置

- 修改 `model_config.json` 调整模型参数
- 修改 `config.env` 调整服务配置
- 修改 `tts_service.py` 扩展功能

## 📄 许可证

MIT License

## 🤝 贡献

欢迎提交Issue和Pull Request！

## 📞 支持

如有问题，请查看：
1. 阿里云通义千问TTS官方文档
2. 项目Issue页面
3. API密钥权限配置