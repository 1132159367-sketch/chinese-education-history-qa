# 开发者指南

## 项目架构

### 后端架构

```
backend/
├── app/
│   ├── main.py              # FastAPI应用入口
│   ├── rag.py               # RAG系统核心
│   ├── pdf_processor.py     # PDF处理模块
│   └── __init__.py
├── pdfs/                    # PDF知识库存储
└── requirements.txt
```

### 前端架构

```
frontend/
├── index.html               # 主页面（HTML + Tailwind CSS）
└── script.js                # 前端逻辑（JavaScript）
```

## 核心模块说明

### 1. FastAPI主应用 ([main.py](backend/app/main.py))

**主要功能：**
- API路由定义
- CORS配置
- 静态文件服务
- 全局状态管理

**关键函数：**
- `startup_event()` - 应用启动时的初始化
- `upload_pdf()` - 处理PDF上传
- `init_knowledge_base()` - 初始化RAG系统
- `ask_question()` - 处理用户提问

### 2. RAG系统 ([rag.py](backend/app/rag.py))

**主要功能：**
- 文档向量化和索引构建
- 语义检索
- LLM调用和答案生成
- 对话历史管理

**核心类 `RAGSystem`：**

```python
class RAGSystem:
    def __init__(self, api_key, base_url)
    def build_index(self, documents)           # 构建FAISS索引
    def retrieve(self, query, top_k=3)         # 检索相关文档
    def answer(self, question, history)        # 生成答案
```

**技术栈：**
- `sentence-transformers` - 文本嵌入
- `FAISS` - 向量数据库
- `anthropic` SDK - 智谱AI API调用

### 3. PDF处理器 ([pdf_processor.py](backend/app/pdf_processor.py))

**主要功能：**
- PDF文件保存和管理
- 文本提取
- 文档分块

**核心类 `PDFProcessor`：**

```python
class PDFProcessor:
    def save_pdf(self, file)                   # 保存PDF
    def extract_text(self, filename)          # 提取和分块
    def list_pdfs()                           # 列出所有PDF
    def delete_pdf(self, filename)            # 删除PDF
```

### 4. 前端界面 ([index.html](frontend/index.html) + [script.js](frontend/script.js))

**HTML结构：**
- 左侧边栏：对话历史、知识库管理
- 右侧聊天区：消息展示、输入框

**JavaScript功能：**
- 消息发送和接收
- 对话历史管理
- PDF上传
- 知识库初始化

## 数据流

### 提问流程

```
用户提问
  ↓
前端发送POST /api/ask
  ↓
后端接收请求
  ↓
RAG系统检索相关文档 (retrieve)
  ↓
构建上下文 + 调用智谱AI (answer)
  ↓
返回答案和来源
  ↓
前端展示结果
```

### 知识库初始化流程

```
用户点击"初始化知识库"
  ↓
前端发送POST /api/init-knowledge-base
  ↓
后端读取所有PDF
  ↓
提取文本并分块 (extract_text)
  ↓
生成向量嵌入
  ↓
构建FAISS索引 (build_index)
  ↓
返回初始化结果
```

## API端点

### 知识库管理

| 方法 | 路径 | 描述 |
|------|------|------|
| POST | `/api/upload-pdf` | 上传PDF文件 |
| GET | `/api/pdfs` | 获取PDF列表 |
| DELETE | `/api/pdfs/{filename}` | 删除PDF |
| POST | `/api/init-knowledge-base` | 初始化知识库 |

### 问答接口

| 方法 | 路径 | 描述 |
|------|------|------|
| POST | `/api/ask` | 提问 |
| GET | `/api/history/{session_id}` | 获取对话历史 |
| DELETE | `/api/history/{session_id}` | 删除对话 |
| GET | `/api/sessions` | 获取所有会话 |

### 系统

| 方法 | 路径 | 描述 |
|------|------|------|
| GET | `/` | 返回前端页面 |
| GET | `/health` | 健康检查 |
| GET | `/docs` | API文档 |

## 配置参数

### RAG系统参数

**在 `rag.py` 中：**

```python
# 检索参数
top_k = 3                    # 返回前3个最相关文档

# LLM参数
model = "claude-3-5-sonnet-20241022"
max_tokens = 2000
temperature = 0.3

# 上下文参数
max_tokens_context = 8000    # 最大上下文token数

# 文档分块参数
chunk_size = 500            # 每块字符数
overlap = 50                # 块间重叠
```

### FastAPI配置

**在 `main.py` 中：**

```python
app = FastAPI(
    title="中国古代教育史问答机器人",
    description="基于智谱AI的RAG问答系统",
    version="1.0.0"
)

# CORS配置
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    ...
)
```

## 扩展开发

### 添加新的文档格式支持

在 `pdf_processor.py` 中添加新方法：

```python
def extract_text_from_docx(self, filename: str) -> List[Dict]:
    """提取Word文档"""
    # 使用python-docx
    pass
```

### 自定义嵌入模型

在 `rag.py` 中修改：

```python
def __init__(self, api_key: str):
    # 使用其他中文模型
    self.embedder = SentenceTransformer('your-model-name')
```

### 添加新的API端点

在 `main.py` 中添加：

```python
@app.post("/api/custom-endpoint")
async def custom_endpoint(data: YourModel):
    # 你的逻辑
    return {"result": ...}
```

### 自定义前端样式

在 `index.html` 中修改Tailwind CSS类名：

```html
<div class="bg-blue-600 hover:bg-blue-700 ...">
```

## 调试技巧

### 1. 查看详细日志

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

### 2. 测试单个组件

```python
# 测试PDF处理
from app.pdf_processor import PDFProcessor
processor = PDFProcessor("backend/pdfs")
docs = processor.extract_text("test.pdf")
print(docs[0])

# 测试RAG系统
from app.rag import RAGSystem
rag = RAGSystem(api_key="your_key")
rag.build_index(docs)
result = rag.answer("测试问题")
print(result["answer"])
```

### 3. 使用API文档

访问 http://localhost:8000/docs 进行交互式测试。

## 性能优化建议

### 1. 向量索引持久化

```python
import pickle

# 保存索引
with open('index.pkl', 'wb') as f:
    pickle.dump(rag.index, f)

# 加载索引
with open('index.pkl', 'rb') as f:
    rag.index = pickle.load(f)
```

### 2. 并发请求处理

FastAPI原生支持异步，确保使用async/await：

```python
@app.post("/api/ask")
async def ask_question(question_data: Question):
    # 异步处理
    result = await async_answer(question_data)
    return result
```

### 3. 缓存常用查询

使用Redis缓存常见问题及其答案。

## 测试

### 单元测试

创建 `backend/tests/` 目录：

```python
# test_rag.py
import pytest
from app.rag import RAGSystem

def test_rag_answer():
    rag = RAGSystem(api_key="test_key")
    # 测试逻辑
```

### 集成测试

```python
# test_api.py
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
```

## 部署建议

### Docker部署

创建 `Dockerfile`：

```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### 云服务部署

- 使用Gunicorn + Uvicorn workers
- 配置Nginx作为反向代理
- 使用PM2管理进程

---

**祝开发顺利！** 💻
