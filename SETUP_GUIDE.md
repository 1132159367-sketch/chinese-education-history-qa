# 快速上手指南

## 5分钟快速开始

### 第一步：获取智谱AI API Key

1. 访问 https://open.bigmodel.cn/
2. 注册账号并登录
3. 进入控制台 → API密钥 → 创建新的API Key
4. 复制你的API Key（格式类似：`sk.xxxxxxxxx`）

### 第二步：配置环境变量

1. 打开项目目录中的 `.env.example` 文件
2. 将 `your_zhipu_api_key_here` 替换为你的实际API Key
3. 将文件另存为 `.env`（注意文件名前面有点）

**示例：**
```env
ZHIPU_API_KEY=sk.xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
ZHIPU_BASE_URL=https://api.z.ai/api/anthropic
```

### 第三步：上传PDF文件

将你的中国古代教育史相关PDF文件放入 `backend/pdfs/` 目录。

**或者**通过Web界面上传（启动服务后）。

### 第四步：启动服务

**Windows用户：**
双击 `start.bat` 文件

**命令行方式：**
```bash
pip install -r requirements.txt
cd backend
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

### 第五步：使用系统

1. 打开浏览器访问：http://localhost:8000
2. 点击左侧"初始化知识库"按钮
3. 等待知识库构建完成
4. 开始提问！

## 常见问题速查

### ❌ 启动时提示"未设置 ZHIPU_API_KEY"

**解决：** 确保在项目根目录创建了 `.env` 文件，且内容正确。

### ❌ 安装依赖时出错

**解决：**
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### ❌ 知识库初始化失败

**检查：**
- PDF文件是否已放入 `backend/pdfs/` 目录
- API Key是否有效
- 网络连接是否正常

### ❌ 回答"超出知识库范围"

**这是正常的！** 系统严格基于知识库回答，确保PDF文件包含相关知识。

## 示例问题

试试问这些问题：

- "西周的教育制度有什么特点？"
- "科举制度是从哪个朝代开始的？"
- "古代私学教育是如何发展的？"
- "朱熹的教育思想有哪些主要内容？"
- "明代国子监的教育内容有哪些？"
- "古代科举考试有哪些科目？"

## 界面操作

- **新建对话**：点击左上角"新建对话"按钮
- **发送消息**：在底部输入框输入，按Enter发送
- **多行输入**：Shift + Enter 换行
- **查看历史**：左侧列表可切换对话
- **删除对话**：鼠标悬停在历史对话上，点击删除图标

## 技术支持

如遇问题，请查看：
1. 控制台输出的详细错误信息
2. README.md 文档中的"常见问题"部分
3. API文档：http://localhost:8000/docs

---

**祝使用愉快！** 🚀
