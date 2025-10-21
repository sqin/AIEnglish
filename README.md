# AI English TTS Service

一个基于阿里云通义千问的英文文本转语音服务。

## 功能特性

- 🎤 支持8种英文音色
- 🌍 支持中英文混合文本
- 📁 支持多种音频格式输出
- 🔧 RESTful API接口
- 💰 成本计算功能

## 快速开始

### 1. 环境配置

复制环境变量模板文件：
```bash
cp config.env.example .env
```

编辑 `.env` 文件，设置您的API密钥：
```bash
DASHSCOPE_API_KEY=your_actual_api_key_here
```

### 2. 安装依赖

```bash
pip install -r requirements.txt
```

### 3. 启动服务

```bash
python start.py
```

或者指定端口：
```bash
PORT=8080 python app.py
```

## API 接口

### 健康检查
```bash
GET /api/health
```

### 获取音色列表
```bash
GET /api/voices
```

### 文本转语音
```bash
POST /api/synthesize
Content-Type: application/json

{
  "text": "Hello, this is a test.",
  "voice": "Jennifer",
  "format": "wav"
}
```

### 下载音频文件
```bash
POST /api/synthesize/file
Content-Type: application/json

{
  "text": "Hello, this is a test.",
  "voice": "Cherry",
  "format": "wav"
}
```

## 支持的音色

| 音色名称 | 描述 |
|---------|------|
| Jennifer | 品牌级、电影质感般美语女声 |
| Ryan | 节奏拉满，戏感炸裂 |
| Katerina | 御姐音色，韵律回味十足 |
| Elias | 学科严谨性，叙事技巧 |
| Cherry | 阳光积极、亲切自然小姐姐 |
| Serena | 温柔小姐姐 |
| Ethan | 标准普通话，带部分北方口音 |
| Chelsie | 二次元虚拟女友 |

## 安全说明

⚠️ **重要**: 请勿将包含真实API密钥的 `.env` 文件提交到版本控制系统。

- `.env` 文件已添加到 `.gitignore`
- 使用 `config.env.example` 作为模板
- 确保您的API密钥安全

## 开发

### 项目结构
```
aienglish/
├── app.py              # Flask应用主文件
├── tts_service.py      # TTS服务核心逻辑
├── start.py           # 启动脚本
├── config.env.example # 环境变量模板
├── requirements.txt   # Python依赖
└── README.md         # 项目说明
```

### 环境变量
- `DASHSCOPE_API_KEY`: 阿里云通义千问API密钥
- `PORT`: 服务端口（默认5000）

## 许可证

MIT License