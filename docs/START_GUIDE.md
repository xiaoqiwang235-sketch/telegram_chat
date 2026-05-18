# Telegram 聊天机器人 - 启动指南

## 🎯 快速开始

### 1️⃣ 运行网络诊断（推荐先运行）

```bash
cd D:/code/telegram_chat
export HF_ENDPOINT=https://hf-mirror.com
uv run python test_network.py
```

这个脚本会检查：
- ✅ Telegram API 连接
- ✅ 数据库连接
- ✅ 本地 Embedding 模型

### 2️⃣ 配置代理（如果需要）

编辑 `.env` 文件，取消注释并配置代理：

```env
# 代理配置（如果无法直接访问 Telegram）
HTTP_PROXY=http://127.0.0.1:7890
HTTPS_PROXY=http://127.0.0.1:7890
```

或者编辑 `start_bot_with_proxy.bat` 设置代理。

### 3️⃣ 启动机器人

**方式 A：使用启动脚本（推荐）**
```bash
start_bot_with_proxy.bat
```

**方式 B：命令行启动**
```bash
cd D:/code/telegram_chat
export HF_ENDPOINT=https://hf-mirror.com
uv run python -m src.main
```

## 🔧 常见问题解决

### 问题 1：Telegram API 超时

**症状：**
```
telegram.error.TimedOut: Timed out
```

**解决方案：**
1. 配置代理（见步骤2）
2. 增加 `.env` 中的超时时间：
```env
TELEGRAM_CONNECT_TIMEOUT=60
TELEGRAM_READ_TIMEOUT=60
TELEGRAM_WRITE_TIMEOUT=60
TELEGRAM_POOL_TIMEOUT=60
```

### 问题 2：数据库连接失败

**症状：**
```
ValueError: DB_HOST environment variable is required
```

**解决方案：**
1. 确保已安装并启动 MySQL 服务
2. 检查 `.env` 中的数据库配置：
```env
DB_HOST=localhost
DB_PORT=3306
DB_NAME=telegram_chatbot
DB_USER=root
DB_PASSWORD=123456
```

### 问题 3：模型下载失败

**症状：**
```
[WinError 10060] 连接失败
```

**解决方案：**
1. 确保 `.env` 中设置了：
```env
HF_ENDPOINT=https://hf-mirror.com
```
2. 检查网络连接
3. 耐心等待，模型约 400MB，首次下载需要时间

### 问题 4：端口被占用

**症状：**
```
Address already in use
```

**解决方案：**
1. 检查是否有其他进程占用端口
2. 关闭其他运行的 bot 实例

## 📊 系统要求

- **Python**: 3.13.x
- **数据库**: MySQL 5.7+
- **内存**: 至少 4GB（本地模型需要）
- **网络**: 需要能访问 Telegram API（可能需要代理）
- **磁盘**: 至少 2GB 可用空间（模型和数据）

## 🎮 使用 Telegram Bot

启动成功后，在 Telegram 中：

1. **搜索你的 bot**：使用 bot 的用户名
2. **发送 `/start`**：开始对话
3. **常用命令**：
   - `/help` - 查看帮助
   - `/style` - 查看当前对话风格
   - `/setstyle <风格>` - 设置对话风格
   - `/clear` - 清除记忆

## 📁 项目结构

```
telegram_chat/
├── src/
│   ├── main.py                 # 主入口
│   ├── database/               # 数据库相关
│   ├── memory/                 # 记忆系统
│   ├── services/               # 业务逻辑
│   └── handlers/               # 消息处理
├── .env                        # 配置文件
├── requirements.txt            # 依赖包
├── test_network.py            # 网络诊断工具
└── start_bot_with_proxy.bat   # 启动脚本
```

## 🔄 更新和维护

### 更新依赖包
```bash
uv pip sync requirements.txt
```

### 查看日志
日志保存在 `logs/bot.log`

### 停止机器人
按 `Ctrl+C` 或关闭终端窗口

## 💡 提示

1. **首次启动**：需要下载模型（400MB），请耐心等待
2. **代理配置**：如果在中国大陆，强烈建议配置代理
3. **数据库**：确保 MySQL 服务始终运行
4. **性能**：本地模型在 CPU 上运行，响应时间约 100-200ms

## 🆘 获取帮助

如果遇到问题：
1. 运行 `test_network.py` 诊断问题
2. 查看 `logs/bot.log` 日志文件
3. 检查 `.env` 配置是否正确

---

**祝使用愉快！** 🚀
