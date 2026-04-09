# Render.com 部署指南

## 为什么选择 Render.com？

✅ **完全免费** - 永久免费套餐
✅ **支持Python后端** - FastAPI完美支持
✅ **持久化存储** - 1GB免费磁盘空间，可存储PDF
✅ **HTTPS证书** - 自动配置SSL
✅ **自动部署** - Git推送自动部署
✅ **长时间运行** - 免费层支持持续运行

## 🚀 5分钟快速部署

### 1. 准备项目文件

项目根目录应包含以下文件：
```
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py
│   │   ├── rag.py
│   │   └── pdf_processor.py
│   └── pdfs/              # 空目录，Render会自动创建
├── frontend/
│   ├── index.html
│   └── script.js
├── requirements.txt
├── render.yaml            # Render配置文件
├── .renderignore          # Render忽略文件
└── .git
```

### 2. 推送代码到 GitHub

```bash
# 如果还没有Git仓库，先初始化
git init
git add .
git commit -m "Initial commit"

# 在GitHub上创建新仓库，然后关联
git remote add origin https://github.com/你的用户名/chinese-education-history-qa.git
git push -u origin master
```

### 3. 在 Render 创建服务

#### 方式A：使用 render.yaml（推荐）

1. 访问 https://dashboard.render.com/
2. 点击 "New +"
3. 选择 "New Web Service"
4. 连接你的GitHub仓库
5. Render会自动检测 `render.yaml` 文件
6. 点击 "Create Web Service"

#### 方式B：手动配置

1. 访问 https://dashboard.render.com/
2. 点击 "New +" → "New Web Service"
3. 连接你的GitHub仓库 `chinese-education-history-qa`
4. 配置服务：

**构建配置：**
```
Build Command: pip install -r requirements.txt
Start Command: gunicorn app.main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:$PORT
```

**环境变量：**
```
ZHIPU_API_KEY = 你的智谱AI密钥
ZHIPU_BASE_URL = https://api.z.ai/api/anthropicAuth
```

**磁盘存储：**
```
Name: pdf-storage
Mount Path: /opt/render/project/backend/pdfs
Size: 1 GB
```

5. 点击 "Create Web Service"

### 4. 配置环境变量

在Render Dashboard中：

1. 点击你的服务名称
2. 进入 "Environment" 标签页
3. 点击 "Add Environment Variable"
4. 添加以下变量：

```
ZHIPU_API_KEY = 你的实际API密钥
ZHIPU_BASE_URL = https://api.z.ai/api/anthropicAuth
```

5. 点击 "Save Changes"
6. Render会自动重启服务

### 5. 等待部署完成

- 部署通常需要2-5分钟
- 在 "Events" 标签页查看部署进度
- 部署成功后会显示一个URL，例如：
  `https://education-qa-bot.onrender.com`

### 6. 访问你的应用

点击Render提供的URL，即可访问公网版本！

## 📁 文件结构说明

### render.yaml

Render配置文件，自动配置服务参数：

```yaml
services:
  - type: web              # 服务类型
    name: education-qa-bot   # 服务名称
    env: python            # 运行环境
    buildCommand: pip install -r requirements.txt  # 构建命令
    startCommand: gunicorn app.main:app --workers 4 ...  # 启动命令
    plan: free            # 使用免费套餐
    envVars:             # 环境变量
      - key: ZHIPU_API_KEY
        sync: false      # 不同步到其他服务
    disk:                # 磁盘存储
      name: pdf-storage
      mountPath: /opt/render/project/backend/pdfs
      sizeGB: 1         # 1GB免费空间
```

### .renderignore

类似于.gitignore，告诉Render哪些文件不需要部署：

```gitignore
# Python缓存
__pycache__/
*.pyc

# 虚拟环境
venv/
.venv/

# 本地环境变量
.env

# PDF文件（Render会自动创建目录）
backend/pdfs/*.pdf

# IDE文件
.vscode/
.idea/
```

## 🔧 高级配置

### 自定义域名

1. 在Render Dashboard进入 "Domains" 标签页
2. 点击 "Add Custom Domain"
3. 输入你的域名，例如：`edu.yourdomain.com`
4. 按照提示配置DNS记录

### 数据库扩展（如需要）

如果将来需要数据库：

```yaml
services:
  - type: web
    name: education-qa-bot
    # ... 其他配置 ...

  - type: pserv     # 私有服务
    name: postgres
    env: docker
    image: postgres:15
    plan: free
    envVars:
      - key: POSTGRES_PASSWORD
        generateValue: true
```

### 日志监控

在Render Dashboard中：

- **Logs标签页**：实时查看应用日志
- **Metrics标签页**：CPU、内存使用情况
- **Events标签页**：部署和重启历史

## 📊 免费套餐限制

| 资源 | 免费套餐限制 |
|------|------------|
| 运行时间 | 只要活跃就一直运行 |
| 内存 | 512MB RAM |
| CPU | 0.1 CPU |
| 磁盘空间 | 1GB |
| 带宽 | 100GB/月 |
| 构建时间 | 15分钟 |
| 自动休眠 | 15分钟无请求后休眠 |

**注意**：免费层会自动休眠，但这不影响你的使用场景，有请求时会自动唤醒。

## 🔄 更新部署

每次向GitHub推送代码时，Render会自动部署：

```bash
git add .
git commit -m "Update features"
git push
```

Render会自动：
1. 检测到新提交
2. 重新构建项目
3. 重启服务
4. 保持环境变量和PDF文件

## 🚨 故障排除

### 部署失败

查看 "Events" 标签页的错误信息：

**常见问题：**

1. **端口错误**
   ```
   Error: Address already in use
   ```
   解决：确保startCommand使用 `$PORT` 变量

2. **依赖安装失败**
   ```
   ERROR: Could not find a version that satisfies...
   ```
   解决：检查 `requirements.txt` 中的版本

3. **环境变量缺失**
   ```
   KeyError: 'ZHIPU_API_KEY'
   ```
   解决：在Render Dashboard中配置环境变量

### 应用无法访问

1. **检查服务状态**
   - Render Dashboard应该显示 "Service is up"

2. **查看日志**
   - 进入 "Logs" 标签页
   - 查找错误信息

3. **手动重启**
   - 在Dashboard点击 "Manual Deploy"
   - 选择 "Clear build cache & deploy"

### PDF上传失败

1. **检查磁盘配置**
   - 确认 "Disk" 标签页中配置了pdf-storage

2. **检查目录权限**
   - 查看日志中的权限错误

3. **增大上传限制**
   - 在nginx层配置（如果有）

## 💰 成本对比

| 平台 | 月费 | 免费存储 | 持续运行 | 推荐度 |
|------|------|---------|---------|--------|
| Render | $0 | 1GB | ✅ | ⭐⭐⭐⭐⭐ |
| Railway | $5 | 1GB | ❌ | ⭐⭐⭐ |
| Hugging Face | $0 | 有限 | ⚠️ | ⭐⭐⭐⭐ |
| Streamlit | $0 | 有限 | ❌ | ⭐⭐ |
| Vercel | $0 | 无 | ❌ | ⭐ |

## 🎯 总结

Render.com 是你项目的最佳选择，因为：

✅ 完全免费，无需信用卡
✅ 支持Python后端和文件上传
✅ 自动HTTPS和域名
✅ 自动部署和更新
✅ 持久化存储PDF文件
✅ 完善的监控和日志

按照上述步骤，你可以在5-10分钟内完成部署，获得一个永久免费的公网服务！

---

**立即开始部署：** https://dashboard.render.com/
