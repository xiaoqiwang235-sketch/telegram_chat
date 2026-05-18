# 本地 Embedding 模型配置指南

本项目支持使用本地模型替代 OpenAI API，实现零成本、保护隐私的长期记忆功能。

## 🎯 优势

- ✅ **完全免费** - 无需付费 API
- ✅ **数据隐私** - 所有数据在本地处理
- ✅ **离线运行** - 不需要网络连接
- ✅ **中文优化** - 使用专门为中文优化的模型

## 📦 推荐模型

| 模型 | 大小 | 维度 | 优点 | 下载时间* |
|------|------|------|------|-----------|
| **m3e-base** (推荐) | ~400MB | 768 | 中文效果好，速度快 | ~2分钟 |
| bge-base-zh-v1.5 | ~400MB | 768 | BAAI出品，SOTA | ~2分钟 |
| paraphrase-multilingual-MiniLM-L12-v2 | ~470MB | 384 | 多语言支持 | ~3分钟 |

*取决于网络速度

## 🚀 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

这将自动安装：
- `sentence-transformers` - 模型框架
- `torch` - 深度学习库
- `transformers` - 模型库

### 2. 配置 `.env` 文件

已自动配置以下选项：

```env
# 使用本地 embedding 模型
USE_LOCAL_EMBEDDINGS=true

# 模型名称（m3e-base 是推荐选择）
LOCAL_EMBEDDING_MODEL=moka-ai/m3e-base

# 运行设备（cpu 或 cuda，如果有 GPU）
LOCAL_EMBEDDING_DEVICE=cpu

# 向量维度（m3e-base 是 768）
LOCAL_EMBEDDING_DIMENSIONS=768
```

### 3. 首次启动

启动时会自动下载模型：

```bash
python -m src.main
```

**首次启动输出：**
```
📦 Loading local embedding model: moka-ai/m3e-base
Downloading model... 100% ██████████████████ 400MB
✅ Model loaded successfully! Dimension: 768
```

**模型缓存位置：**
```
C:\Users\你的用户名\.cache\huggingface\hub\
```

## 🔄 切换模型

如果想使用其他模型，只需修改 `.env` 中的 `LOCAL_EMBEDDING_MODEL`：

```env
# 使用 BGE 模型
LOCAL_EMBEDDING_MODEL=BAAI/bge-base-zh-v1.5
LOCAL_EMBEDDING_DIMENSIONS=768

# 或使用多语言模型
LOCAL_EMBEDDING_MODEL=sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2
LOCAL_EMBEDDING_DIMENSIONS=384
```

重启机器人后会自动下载新模型。

## 💻 GPU 加速（可选）

如果有 NVIDIA GPU，可以启用 GPU 加速：

```env
LOCAL_EMBEDDING_DEVICE=cuda
```

需要先安装 CUDA 和 PyTorch GPU 版本：
```bash
pip install torch torchvision --index-url https://download.pytorch.org/whl/cu118
```

## 📊 性能对比

| 指标 | 本地模型 (m3e-base) | OpenAI API |
|------|---------------------|------------|
| 成本 | 免费 | $0.0001/1K次 |
| 延迟 | ~100ms | ~500ms |
| 准确度 | 中文：优秀 | 通用：优秀 |
| 隐私 | 完全本地 | 数据上传 |

## ❓ 常见问题

### 1. 模型下载失败？

**问题：** 网络原因导致下载失败

**解决方案：**
```bash
# 使用国内镜像（可选）
export HF_ENDPOINT=https://hf-mirror.com
python -m src.main
```

### 2. 内存不足？

**问题：** 模型加载后内存占用过高

**解决方案：**
- 使用更小的模型：`paraphrase-multilingual-MiniLM-L12-v2`
- 或关闭长期记忆功能

### 3. 首次启动慢？

**问题：** 第一次启动需要下载模型

**说明：** 只需下载一次，之后会缓存到本地。首次启动约需 2-5 分钟（取决于网络）。

### 4. 想回退到 OpenAI API？

修改 `.env`：
```env
USE_LOCAL_EMBEDDINGS=false
OPENAI_API_KEY=你的实际API密钥
```

## 🎉 完成！

配置完成后，你的机器人现在拥有：
- ✅ 完全的长期记忆功能
- ✅ 零成本运行
- ✅ 数据隐私保护
- ✅ 离线工作能力

开始聊天吧！🚀
