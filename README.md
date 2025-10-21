# 阿里云通义千问TTS英文语音合成服务

基于阿里云通义千问Qwen3-TTS模型开发的英文文本转语音服务，提供RESTful API接口和Python客户端。

## 功能特性

- 🎵 **多种音色支持**: 支持8种不同的英文音色，包括Jennifer、Ryan、Katerina等
- 🌍 **多语言支持**: 支持中文、英语、法语、德语、俄语、意大利语、西班牙语、葡萄牙语、日语、韩语
- ⚡ **高性能**: 基于Qwen3-TTS-Flash模型，响应速度快
- 💰 **成本透明**: 实时计算转换成本，按字符数计费
- 🔧 **灵活配置**: 支持语速、音量、音调等参数调节
- 📁 **文件管理**: 支持音频文件保存和直接下载
- 🛡️ **错误处理**: 完善的错误处理和日志记录

## 支持的音色

| 音色名称 | 参数值 | 音色效果 | 支持语言 |
|---------|--------|----------|----------|
| Jennifer | Jennifer | 品牌级、电影质感般美语女声 | 中文、英语、法语、德语、俄语、意大利语、西班牙语、葡萄牙语、日语、韩语 |
| Ryan | Ryan | 节奏拉满，戏感炸裂，真实与张力共舞 | 中文、英语、法语、德语、俄语、意大利语、西班牙语、葡萄牙语、日语、韩语 |
| Katerina | Katerina | 御姐音色，韵律回味十足 | 中文、英语、法语、德语、俄语、意大利语、西班牙语、葡萄牙语、日语、韩语 |
| Elias | Elias | 既保持学科严谨性，又通过叙事技巧将复杂知识转化为可消化的认知模块 | 中文、英语、法语、德语、俄语、意大利语、西班牙语、葡萄牙语、日语、韩语 |
| Cherry | Cherry | 阳光积极、亲切自然小姐姐 | 中文、英语 |
| Serena | Serena | 温柔小姐姐 | 中文、英语 |
| Ethan | Ethan | 标准普通话，带部分北方口音。阳光、温暖、活力、朝气 | 中文、英语 |
| Chelsie | Chelsie | 二次元虚拟女友 | 中文、英语 |

## 安装和配置

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 配置API密钥

复制配置文件模板：
```bash
cp config.env.example .env
```

编辑 `.env` 文件，设置您的阿里云API密钥：
```env
DASHSCOPE_API_KEY=your_api_key_here
HOST=0.0.0.0
PORT=5000
DEBUG=True
```

### 3. 启动服务

```bash
python app.py
```

服务将在 `http://localhost:5000` 启动。

## API接口文档

### 1. 健康检查

```http
GET /api/health
```

**响应示例：**
```json
{
  "status": "healthy",
  "service": "Qwen TTS English Service",
  "timestamp": "2024-01-01T12:00:00"
}
```

### 2. 获取可用音色

```http
GET /api/voices
```

**响应示例：**
```json
{
  "success": true,
  "voices": {
    "jennifer": "Jennifer",
    "ryan": "Ryan",
    "katerina": "Katerina",
    "elias": "Elias",
    "cherry": "Cherry",
    "serena": "Serena",
    "ethan": "Ethan",
    "chelsie": "Chelsie"
  },
  "count": 8,
  "message": "获取音色列表成功"
}
```

### 3. 语音合成

```http
POST /api/synthesize
Content-Type: application/json

{
  "text": "Hello, this is a demonstration of English text-to-speech service.",
  "voice": "Jennifer",
  "format": "wav",
  "sample_rate": 22050,
  "speed": 1.0,
  "volume": 1.0,
  "pitch": 1.0,
  "save_file": false
}
```

**参数说明：**
- `text` (必需): 要转换的英文文本，最大600字符
- `voice` (可选): 音色名称，默认"Jennifer"
- `format` (可选): 音频格式，支持"wav"、"mp3"，默认"wav"
- `sample_rate` (可选): 采样率，默认22050
- `speed` (可选): 语速，范围0.5-2.0，默认1.0
- `volume` (可选): 音量，范围0.1-2.0，默认1.0
- `pitch` (可选): 音调，范围0.5-2.0，默认1.0
- `save_file` (可选): 是否保存文件，默认false

**响应示例：**
```json
{
  "success": true,
  "audio_data": "base64编码的音频数据",
  "format": "wav",
  "sample_rate": 22050,
  "text_length": 75,
  "voice": "Jennifer",
  "cost": 0.006,
  "message": "语音合成成功"
}
```

### 4. 语音合成并下载文件

```http
POST /api/synthesize/file
Content-Type: application/json

{
  "text": "Hello, this is a demonstration of English text-to-speech service.",
  "voice": "Jennifer",
  "format": "wav"
}
```

直接返回音频文件供下载。

### 5. 计算成本

```http
POST /api/cost
Content-Type: application/json

{
  "text": "Hello, this is a demonstration of English text-to-speech service."
}
```

**响应示例：**
```json
{
  "success": true,
  "text_length": 75,
  "cost": 0.006,
  "currency": "CNY",
  "message": "成本计算成功"
}
```

## 使用示例

### Python客户端使用

```python
from demo import TTSClient

# 创建客户端
client = TTSClient("http://localhost:5000")

# 语音合成
result = client.synthesize(
    text="Hello, this is a demonstration of English text-to-speech service.",
    voice="Jennifer",
    save_file=True
)

if result['success']:
    print(f"合成成功! 成本: {result['cost']} 元")
    print(f"保存文件: {result['saved_file']}")
else:
    print(f"合成失败: {result['error']}")
```

### cURL示例

```bash
# 语音合成
curl -X POST http://localhost:5000/api/synthesize \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Hello, this is a demonstration of English text-to-speech service.",
    "voice": "Jennifer",
    "save_file": true
  }'

# 获取音色列表
curl http://localhost:5000/api/voices

# 计算成本
curl -X POST http://localhost:5000/api/cost \
  -H "Content-Type: application/json" \
  -d '{"text": "Hello world"}'
```

## 运行演示

运行完整的演示程序：

```bash
python demo.py
```

演示程序包含：
- 基础功能演示
- 不同音色测试
- 高级参数调节
- 文件下载功能
- 交互式操作界面

## 成本说明

- **计费方式**: 按输入字符数计费
- **价格**: 0.8元/万字符
- **字符计算**: 英文字母、标点符号、空格 = 1个字符
- **免费额度**: 各2000字符，有效期90天（百炼开通后）

## 注意事项

1. **API密钥**: 需要有效的阿里云DashScope API密钥
2. **文本长度**: 单次请求最大600字符
3. **音频格式**: 支持WAV和MP3格式
4. **文件存储**: 音频文件默认保存在`audio_outputs`目录
5. **错误处理**: 所有接口都有完善的错误处理机制

## 故障排除

### 常见问题

1. **API密钥错误**
   ```
   错误: 请设置DASHSCOPE_API_KEY环境变量
   解决: 检查.env文件中的API密钥配置
   ```

2. **文本长度超限**
   ```
   错误: 文本长度超过限制: 650 > 600
   解决: 将文本分割为多个较短的片段
   ```

3. **音色不支持**
   ```
   错误: 不支持的音色: InvalidVoice
   解决: 使用/api/voices接口查看支持的音色
   ```

### 日志查看

服务运行时会输出详细的日志信息，包括：
- 请求处理状态
- 错误信息
- 性能指标
- 成本计算

## 许可证

本项目基于MIT许可证开源。

## 联系方式

如有问题或建议，请通过以下方式联系：
- 创建Issue
- 发送邮件
- 提交Pull Request
