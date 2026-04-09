# 中国古代教育史问答机器人

基于智谱AI的RAG（检索增强生成）问答系统，专为考研辅导设计。

## 功能特点

- **专业知识问答**：基于上传的PDF知识库，提供关于中国古代教育史的专业解答
- **RAG技术**：使用语义检索和向量数据库，确保答案基于真实文档内容
- **考研辅导风格**：严谨、专业、学术化的回答风格
- **安全约束**：严格基于知识库回答，超出范围的问题会明确告知
- **多对话管理**：支持创建多个对话，保存和切换历史对话
- **简洁界面**：类似ChatGPT的现代化聊天界面

## 技术栈

- **后端**：Python + FastAPI
- **前端**：HTML + Tailwind CSS + Vanilla JavaScript
- **AI模型**：智谱AI (Anthropic兼容接口)
- **RAG组件**：
  - PDF处理：pdfplumber
  - 文本嵌入：sentence-transformers (paraphrase-multilingual-MiniLM-L12-v2)
  - 向量数据库：FAISS
  - LLM：智谱AI Claude模型

## 项目结构

```
├── backend/
│   ├── app/
│   │   ├── __init__.py          # 应用模块
│   │   ├── main.py              # FastAPI主应用
│   │   ├── rag.py               # RAG系统实现
│   │   └── pdf_processor.py     # PDF处理器
│   ├── pdfs/                    # 存放PDF知识库文件
│   └── requirements.txt        # Python依赖
├── frontend/
│   ├── index.html              # 前端页面
│   └── script.js               # 前端脚本
├── .env.example               # 环境变量模板
└── README.md                  # 项目说明文档
```

## 快速开始

### 1. 环境准备

确保你的系统已安装以下软件：

- Python 3.8+
- pip

### 2. 克隆项目

```bash
cd c:\Users\zhang\slide-deck\electromagnetic-induction\prompts
```

### 3. 安装依赖

```bash
pip install -r requirements.txt
```

### 4. 配置智谱AI API Key

#### 获取智谱AI API Key：

1. 访问智谱AI官网：https://open.bigmodel.cn/
2. 注册账号并登录
3. 在控制台创建API Key
4. 复制你的API Key

#### 配置环境变量：

1. 复制环境变量模板：
   ```bash
   cp .env.example .env
   ```

2. 编辑 `.env` 文件，替换 `your_zhipu_api_key_here` 为你的实际API Key：

   ```env
   ZHIPU_API_KEY=你的实际API密钥
   ZHIPU_BASE_URL=https://api.z.ai/api/anthropic
   ```

### 5. 上传PDF知识库

将关于中国古代教育史的PDF文件上传到系统中：

#### 方法1：通过Web界面上传

1. 启动服务（见下一步）
2. 访问 http://localhost:8000
3. 点击左侧的"上传PDF"按钮
4. 选择你的PDF文件并上传

#### 方法2：直接复制到pdfs目录

```bash
# 将PDF文件复制到pdfs目录
cp /path/to/your/education1.pdf backend/pdfs/
cp /path/to/your/education2.pdf backend/pdfs/
```

**重要**：确保PDF文件内容涵盖中国古代教育史相关知识，包括：
- 西周至清朝的教育制度
- 各朝代的教育政策和实践
- 科举制度的演变
- 古代教育思想
- 官学与私学的发展
- 等等...

### 6. 启动服务

在项目根目录运行：

```bash
cd backend
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

或者在Windows上：

```bash
cd backend
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

看到以下输出表示启动成功：

```
==================================================
中国古代教育史问答机器人启动中...
==================================================
✓ 智谱AI API Key 已配置
✓ 找到 2 个PDF文件:
  - education1.pdf
  - education2.pdf
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
```

### 7. 初始化知识库

1. 访问 http://localhost:8000
2. 点击左侧的"初始化知识库"按钮
3. 等待知识库构建完成（首次可能需要几分钟）

系统会自动：
- 提取PDF文本内容
- 分块处理文档
- 生成向量嵌入
- 构建FAISS索引

### 8. 开始提问

现在你可以开始提问了！

**示例问题：**
- "西周的教育制度有什么特点？"
- "科举制度是从哪个朝代开始的？"
- "古代私学教育是如何发展的？"
- "朱熹的教育思想有哪些主要内容？"

## 使用说明

### 基本操作

1. **新建对话**：点击左侧"新建对话"按钮
2. **发送消息**：在底部输入框输入问题，按Enter或点击"发送"按钮
3. **查看历史**：左侧显示所有历史对话，点击可切换
4. **删除对话**：鼠标悬停在历史对话上，点击删除图标

### 知识库管理

1. **上传PDF**：点击"上传PDF"按钮，选择或拖拽PDF文件
2. **查看文件**：点击"查看文件"查看已上传的PDF列表
3. **删除文件**：在文件列表中点击删除图标
4. **重新初始化**：上传新文件后，点击"初始化知识库"重新构建索引

### 对话功能

- **多行输入**：使用 Shift + Enter 换行
- **历史记录**：自动保存对话历史
- **来源标注**：每条回答显示参考的知识库来源
- **安全约束**：超出知识库范围的问题会明确告知

## API接口文档

启动服务后，访问 http://localhost:8000/docs 查看完整的API文档。

### 主要接口

- `POST /api/ask` - 提问
- `POST /api/upload-pdf` - 上传PDF
- `GET /api/pdfs` - 获取PDF列表
- `DELETE /api/pdfs/{filename}` - 删除PDF
- `POST /api/init-knowledge-base` - 初始化知识库
- `GET /api/history/{session_id}` - 获取对话历史
- `DELETE /api/history/{session_id}` - 删除对话

## 常见问题

### 1. 启动时提示"未设置 ZHIPU_API_KEY"

**解决方案**：
- 检查 `.env` 文件是否存在于 `backend` 目录
- 确保 `.env` 文件中 `ZHIPU_API_KEY` 已正确设置
- 重启服务

### 2. 知识库初始化失败

**可能原因**：
- PDF文件损坏或格式不支持
- API Key无效
- 网络连接问题

**解决方案**：
- 检查PDF文件是否能正常打开
- 验证智谱AI API Key是否有效
- 检查网络连接

### 3. 回答"该问题超出当前知识库范围"

**这是正常行为**：
- 系统严格基于知识库内容回答
- 确保你的PDF文件包含相关知识
- 尝试重新表述问题或上传更全面的资料

### 4. 前端页面无法加载

**解决方案**：
- 确保后端服务已启动
- 检查防火墙设置
- 尝试访问 http://localhost:8000/health 检查服务状态

## 配置说明

### 向量索引参数

在 `backend/app/rag.py` 中可以调整以下参数：

```python
# 检索相关文档数量
top_k: int = 3

# 最大上下文token数
max_tokens: int = 8000

# 文档分块大小
chunk_size: int = 500

# 分块重叠
overlap: int = 50
```

### LLM模型参数

在 `backend/app/rag.py` 中可以调整模型参数：

```python
response = self.client.messages.create(
    model="claude-3-5-sonnet-20241022",  # 模型名称
    max_tokens=2000,                       # 最大回复长度
    temperature=0.3,                       # 温度参数（0-2，越低越确定）
)
```

### 系统提示词

在 `backend/app/rag.py` 中自定义系统提示词：

```python
self.system_prompt = """你是一位教育学专业的考研辅导老师...
"""
```

## 性能优化

### 1. 文档处理优化

- 对于大型PDF，可以手动调整 `chunk_size` 和 `overlap` 参数
- 预处理PDF以提高文本质量

### 2. 向量检索优化

- 调整 `top_k` 参数以平衡准确性和速度
- 考虑使用更专业的嵌入模型

### 3. 缓存策略

- 向量索引可以序列化保存到磁盘
- 避免重复初始化知识库

## 开发指南

### 添加新功能

1. 在 `backend/app/` 中添加新模块
2. 在 `main.py` 中注册新的API端点
3. 在 `frontend/script.js` 中添加前端逻辑

### 自定义样式

修改 `frontend/index.html` 中的Tailwind CSS类来自定义界面样式。

### 扩展知识源

在 `backend/app/pdf_processor.py` 中添加对其他文档格式的支持。

## 故障排除

### 日志查看

启动服务时，查看控制台输出的详细日志信息。

### 调试模式

在开发时使用 `--reload` 参数启用自动重载：

```bash
python -m uvicorn app.main:app --reload
```

### 清理缓存

删除 `backend/app/` 中的缓存文件（如果有），重新初始化知识库。

## 许可证

本项目仅供学习和研究使用。

## 联系支持

如有问题或建议，请通过以下方式联系：
- 创建Issue描述问题
- 提供详细的错误日志
- 说明你的环境和配置

## 更新日志

### v1.0.0 (2026-04-09)
- 初始版本发布
- 基本问答功能
- PDF知识库支持
- 多对话管理
- Web界面

---

**祝考研顺利！** 📚
