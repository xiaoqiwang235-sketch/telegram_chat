# Telegram 聊天机器人 (Telegram Chatbot)

基于 Python 和大语言模型的智能 Telegram 聊天机器人，支持多种对话风格和长期记忆功能。

## 功能特性

### 核心功能
- ✅ **多风格对话**: 6种预设对话风格（幽默搞笑、温柔体贴、傲娇、严肃专业、卖萌可爱、知性理性）
- ✅ **长期记忆**: 基于向量数据库的语义搜索，记住历史对话
- ✅ **短期记忆**: 会话级上下文管理（最多50条消息）
- ✅ **群组支持**: 群聊中仅响应 @提及
- ✅ **私聊支持**: 私聊中响应所有消息
- ✅ **限流保护**: 每用户20条/60秒
- ✅ **风格切换**: 用户可设置偏好风格

### 用户命令
- `/start` - 开始使用机器人
- `/help` - 显示帮助信息
- `/style` - 查看所有对话风格
- `/setstyle <编号>` - 设置对话风格
- `/clear` - 清除短期对话记录

### 管理员命令
- `/groupstyle <编号>` - 设置群组风格
- `/resetuser <用户ID>` - 重置用户对话记录
- `/stats` - 查看机器人统计信息

## 技术架构

### 后端技术栈
- **语言**: Python 3.11+
- **框架**: python-telegram-bot 20.7
- **数据库**: MySQL 8.0+ (使用 pymysql)
- **向量数据库**: Faiss (内存索引)
- **LLM API**: XiaoMi MiMo API (OpenAI 兼容)
- **Embedding API**: OpenAI text-embedding-ada-002

### 架构分层
```
src/
├── handlers/          # Telegram 消息处理器
├── services/          # 业务逻辑层
├── memory/            # 记忆子系统
├── repositories/      # 数据访问层
├── models/            # 数据模型
├── database/          # 数据库配置
├── integrations/      # 外部 API 集成
└── utils/             # 工具类
```

### 数据库设计
5个核心表：
- `users` - 用户信息
- `conversations` - 对话记录
- `conversation_vectors` - 向量嵌入
- `group_settings` - 群组设置
- `user_preferences` - 用户偏好

## 快速开始

### 环境要求
- Python 3.11+
- MySQL 8.0+
- XiaoMi MiMo API Key
- OpenAI API Key (用于嵌入)

### 安装步骤

1. **克隆仓库**
```bash
git clone <repository-url>
cd telegram_chat
```

2. **创建虚拟环境**
```bash
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
.venv\Scripts\activate     # Windows
```

3. **安装依赖**
```bash
pip install -r requirements.txt
```

4. **配置环境变量**
复制 `.env.example` 为 `.env` 并填入配置：
```bash
cp .env.example .env
```

编辑 `.env` 文件：
```env
TELEGRAM_BOT_TOKEN=your_bot_token_here
TELEGRAM_ADMIN_USER_IDS=123456789,987654321
DB_HOST=localhost
DB_PORT=3306
DB_NAME=telegram_chatbot
DB_USER=your_db_user
DB_PASSWORD=your_db_password
MIMO_API_KEY=your_mimo_api_key
OPENAI_API_KEY=your_openai_api_key
```

5. **初始化数据库**
```bash
python scripts/migrations/001_create_initial_tables.py
```

6. **启动机器人**
```bash
python -m src.main
```

## 开发指南

### 运行测试
```bash
# 运行所有测试
pytest

# 运行特定测试
pytest tests/test_models/

# 带覆盖率报告
pytest --cov=src --cov-report=html
```

### 代码质量检查
```bash
# Pylint 检查（最低8.0/10）
pylint src/

# Black 格式化
black src/
```

### 项目规范
- **测试驱动开发 (TDD)**: 所有代码先写测试
- **代码覆盖率**: >80%
- **Pylint 评分**: ≥8.0/10
- **异步优先**: 使用 asyncio 而非 threading
- **类型提示**: 所有函数使用 type hints

## 配置说明

### 环境变量

| 变量名 | 必需 | 说明 |
|--------|------|------|
| `TELEGRAM_BOT_TOKEN` | ✅ | Telegram Bot Token |
| `TELEGRAM_ADMIN_USER_IDS` | ✅ | 管理员用户ID（逗号分隔） |
| `DB_HOST` | ✅ | MySQL 主机地址 |
| `DB_PORT` | ✅ | MySQL 端口（默认3306） |
| `DB_NAME` | ✅ | 数据库名称 |
| `DB_USER` | ✅ | 数据库用户名 |
| `DB_PASSWORD` | ✅ | 数据库密码 |
| `MIMO_API_KEY` | ✅ | XiaoMi MiMo API Key |
| `OPENAI_API_KEY` | ✅ | OpenAI API Key |

### 对话风格

1. **幽默搞笑** - 轻松有趣，经常讲笑话
2. **温柔体贴** - 温暖关怀，理解感受
3. **傲娇** - 外冷内热，傲娇性格
4. **严肃专业** - 专业准确，理性分析
5. **卖萌可爱** - 俏皮活泼，可爱卖萌
6. **知性理性** - 深度思考，逻辑清晰

## 部署

### 本地部署
本项目设计为本地部署，不涉及云服务。

### 生产环境建议
1. 使用进程管理器（如 systemd、supervisor）
2. 配置日志轮转
3. 定期备份数据库
4. 监控 bot 运行状态

### 启动脚本示例

创建 `start.sh`:
```bash
#!/bin/bash
source .venv/bin/activate
python -m src.main
```

使用 systemd 服务（Linux）:
```ini
[Unit]
Description=Telegram Chatbot
After=network.target mysql.service

[Service]
Type=simple
User=your_user
WorkingDirectory=/path/to/telegram_chat
Environment="PATH=/path/to/telegram_chat/.venv/bin"
ExecStart=/path/to/telegram_chat/.venv/bin/python -m src.main
Restart=always

[Install]
WantedBy=multi-user.target
```

## 故障排除

### 常见问题

1. **数据库连接失败**
   - 检查 MySQL 服务是否运行
   - 验证 `.env` 中的数据库配置
   - 确保数据库和表已创建

2. **API 调用失败**
   - 检查 API Key 是否正确
   - 验证网络连接
   - 查看日志了解详细错误

3. **机器人无响应**
   - 检查 bot token 是否有效
   - 确认 bot 已启动
   - 验证 Telegram API 可访问

### 日志
日志文件位置：`logs/bot.log`

## 许可证

MIT License

## 贡献

欢迎提交 Issue 和 Pull Request！

## 联系方式

如有问题，请提交 GitHub Issue。
