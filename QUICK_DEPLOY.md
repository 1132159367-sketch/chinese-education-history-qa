# Render 快速部署指南

## 🎯 部署前准备

### 1. 确认项目文件结构
确保你的项目包含以下文件：

```
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py
│   │   ├── rag.py
│   │   └── pdf_processor.py
│   └── pdfs/              # 可以为空
├── frontend/
│   ├── index.html
│   └── script.js
├── requirements.txt          # ✅ 已存在
├── render.yaml              # ✅ 已存在
├── .renderignore            # ✅ 已存在
└── .gitignore              # ✅ 已存在
```

### 2. 推送到 GitHub

```bash
# 如果还没有 Git 仓库
git init
git add .
git commit -m "Ready for Render deployment"

# 在 GitHub 上创建新仓库
# 然后执行：
git remote add origin https://github.com/你的用户名/chinese-education-history-qa.git
git push -u origin master
```

## 🚀 在 Render 上部署

### 步骤 1：创建 Render 账户

1. 访问 https://dashboard.render.com/
2. 使用 GitHub 账户登录
3. 如果没有 GitHub 账户，可以注册

### 步骤 2：创建 Web 服务

1. 点击右上角的 **"New +"** 按钮
2. 选择 **"New Web Service"**
3. 在 **"Connect a repository"** 下找到你的 GitHub 仓库：
   - 搜索仓库名：`chinese-education-history-qa`
   - 点击 **"Connect"** 按钮

### 步骤 3：配置服务

Render 会自动检测到你的 `render.yaml` 文件，自动填充配置：

**基本信息：**
- Name: `education-qa-bot`
- Environment: `Python`
- Build Command: `pip install -r requirements.txt`
- Start Command: `gunicorn app.main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:$PORT`
- Plan: `Free`

**环境变量：**
- `ZHIPU_API_KEY` - 需要你手动填入
- `ZHIPU_BASE_URL` - 自动设置为 `https://api.z.ai/api/anthropic`

**磁盘存储：**
- Name: `pdf-storage`
- Mount Path: `/opt/render/project/backend/pdfs`
- Size: `1 GB`

### 步骤 4：设置环境变量

1. 在配置页面找到 **"Environment"** 部分
2. 点击 **"Add Environment Variable"**
3. 添加以下变量：

```bash
ZHIPU_API_KEY = 你的智谱AI密钥
```

**重要：**
- 将 `你的智谱AI密钥` 替换为实际的API Key
- 不要在 Render 环境变量中直接粘贴 `.env` 文件的内容
- 只需要填入 Key 的值，不需要变量名

### 步骤 5：创建服务

1. 检查所有配置是否正确
2. 点击页面底部的 **"Create Web Service"** 按钮
3. 等待部署完成（通常 2-5 分钟）

## 📋 部署过程监控

### 查看部署进度

1. 点击服务名称进入服务详情页
2. 查看 **"Events"** 标签页：
   - 绿色 ✓ 表示成功
   - 红色 ✗ 表示失败

### 查看实时日志

1. 进入 **"Logs"** 标签页
2. 可以看到实时日志输出
3. 部署成功后显示：
   ```
   INFO: Application startup complete.
   ```

## 🎉 部署成功后

### 访问你的应用

1. 在服务详情页顶部找到 **"Domain"**
2. 点击链接，例如：`https://education-qa-bot.onrender.com`
3. 如果没有域名，可以点击 **"Add Custom Domain"**

### 初始化知识库

1. 访问你的应用
2. 点击左侧的 **"上传PDF"** 按钮
3. 上传你的中国古代教育史PDF文件
4. 点击 **"初始化知识库"** 按钮
5. 等待知识库构建完成

## 🔧 常见问题

### 1. 部署失败

**错误：** `Build failed`

**解决：**
- 检查 `requirements.txt` 是否正确
- 查看 **"Events"** 标签页的详细错误信息
- 确保所有依赖包版本正确

### 2. 应用无法启动

**错误：** `Application startup failed`

**解决：**
- 检查环境变量是否设置正确
- 查看 **"Logs"** 标签页的错误信息
- 确认端口变量 `$PORT` 使用正确

### 3. API 调用失败

**错误：** `智谱AI API调用失败`

**解决：**
- 在 Render Dashboard 检查 `ZHIPU_API_KEY` 是否设置
- 确认 API Key 格式正确
- 查看日志中的详细错误信息

### 4. PDF 上传失败

**错误：** `无法上传文件`

**解决：**
- 检查磁盘存储是否创建成功
- 查看 **"Disks"** 标签页确认 `pdf-storage` 状态
- 检查文件大小是否超过限制（100MB）

## 💰 成本信息

### Render 免费套餐

| 资源 | 免费套餐 |
|------|---------|
| 运行时间 | 无限制（15分钟无请求后休眠） |
| 内存 | 512MB RAM |
| CPU | 0.1 CPU |
| 磁盘空间 | 1GB |
| 带宽 | 100GB/月 |
| 构建时间 | 15分钟 |
| 自动休眠 | 15分钟无请求后休眠 |

### 付费升级

如果需要更好的性能：

- Standard: $7/月 - 2GB RAM，更快的CPU
- Pro: $25/月 - 8GB RAM，专属CPU
- 更多选项查看：https://render.com/pricing

## 🔄 更新部署

每次推送代码到 GitHub，Render 会自动部署：

```bash
git add .
git commit -m "Update features"
git push
```

Render 会自动：
1. 检测到新的提交
2. 重新构建项目
3. 重启服务
4. 保持环境变量和PDF文件

## 📊 监控和维护

### 查看服务状态

在 Render Dashboard：
- **Overview**：服务运行状态
- **Metrics**：CPU、内存使用情况
- **Events**：部署和重启历史
- **Logs**：应用日志
- **Disks**：磁盘使用情况

### 手动重启

如果服务出现问题：
1. 点击 **"Manual Deploy"** 按钮
2. 选择 **"Clear build cache & deploy"**
3. 等待重新部署

## 🎯 成功标志

当你的部署成功时，你会看到：

1. ✅ 服务状态显示 **"Service is up"**
2. ✅ 域名可访问，返回正确页面
3. ✅ 上传PDF功能正常
4. ✅ 初始化知识库成功
5. ✅ 问答功能工作正常

---

**现在开始部署吧！** 🚀

访问：https://dashboard.render.com/
