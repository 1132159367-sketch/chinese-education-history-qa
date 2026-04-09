# Render 部署故障排除指南

## ❌ 错误：Exited with status 127

这个错误表示进程启动失败。以下是可能的原因和解决方法。

## 🔍 问题1：依赖安装失败

### 症状
在Render Logs中看到类似错误：
```
ERROR: Could not find a version that satisfies the requirement
```

### 解决方法
1. 检查 `requirements.txt` 中的版本是否正确
2. 移除版本限制，使用最新版本：
   ```python
   fastapi>=0.104.1  # 改为 fastapi
   ```
3. 在本地测试安装：
   ```bash
   pip install -r requirements.txt
   ```

## 🔍 问题2：内存不足

### 症状
在Logs中看到类似错误：
```
MemoryError: Unable to allocate array
OOMKilled
```

### 解决方法
1. 减少workers数量：
   ```yaml
   # render.yaml 中
   startCommand: uvicorn app.main:app --host 0.0.0.0 --port $PORT --workers 1
   ```
2. 使用更简单的模型：
   ```python
   # rag.py 中
   self.embedder = SentenceTransformer('distiluse-base-multilingual-cased-v1')  # 更小的模型
   ```

## 🔍 问题3：端口绑定错误

### 症状
在Logs中看到类似错误：
```
OSError: [Errno 98] Address already in use
```

### 解决方法
1. 确保使用 `$PORT` 环境变量：
   ```yaml
   startCommand: uvicorn app.main:app --host 0.0.0.0 --port $PORT
   ```
2. 不要硬编码端口号

## 🔍 问题4：导入错误

### 症状
在Logs中看到类似错误：
```
ModuleNotFoundError: No module named 'xxx'
ImportError: cannot import name 'xxx'
```

### 解决方法
1. 检查文件结构是否正确：
   ```
   backend/app/__init__.py
   backend/app/main.py
   backend/app/rag.py
   ```
2. 检查相对导入是否正确：
   ```python
   from .rag import RAGSystem  # 正确
   from rag import RAGSystem     # 错误
   ```

## 🔍 问题5：环境变量缺失

### 症状
在Logs中看到类似错误：
```
ValueError: 请设置 ZHIPU_API_KEY 环境变量
KeyError: 'ZHIPU_API_KEY'
```

### 解决方法
1. 在Render Dashboard中检查环境变量：
   - 变量名：`ZHIPU_API_KEY`
   - 值：`3f410ea451664d1d98882c496c598f70.1eGG7WBoMbiYGHsS`
2. 确保 `sync: false`（只在这个服务中使用）

## 🔍 问题6：文件路径错误

### 症状
在Logs中看到类似错误：
```
FileNotFoundError: [Errno 2] No such file or directory
RuntimeError: Directory 'xxx' does not exist
```

### 解决方法
1. 检查render.yaml中的路径配置：
   ```yaml
   # 确保路径相对于项目根目录
   mountPath: /opt/render/project/backend/pdfs
   ```
2. 在GitHub中确认文件结构

## 🚨 当前修复内容

我已经为你做了以下修复：

### 1. 简化启动命令
```yaml
# 之前（使用gunicorn + workers）
startCommand: gunicorn app.main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:$PORT

# 现在（直接使用uvicorn）
startCommand: uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

### 2. 减少内存使用
- 移除复杂的gunicorn配置
- 减少初始加载压力

### 3. 修复YAML格式
- 使用正确的2空格缩进
- 修复格式错误

## 🔧 故障排除步骤

### 1. 查看详细日志
在Render Dashboard中：
1. 点击你的服务名称
2. 进入 **"Logs"** 标签页
3. 查看完整的错误信息

### 2. 查看构建日志
进入 **"Events"** 标签页：
- 查看构建过程的详细输出
- 找出具体失败的步骤

### 3. 本地测试
在推送前先在本地测试：
```bash
# 模拟Render环境
export PORT=8000
cd backend
python -m uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

### 4. 逐步排查
1. 先测试最小配置
2. 然后逐步添加功能
3. 每步都验证

## 💡 推荐配置

如果问题持续存在，使用这个简化配置：

```yaml
services:
  - type: web
    name: education-qa-bot
    env: python
    buildCommand: pip install -r requirements.txt
    startCommand: python -m uvicorn app.main:app --host 0.0.0.0 --port $PORT
    plan: free
    envVars:
      - key: ZHIPU_API_KEY
        sync: false
      - key: ZHIPU_BASE_URL
        value: https://api.z.ai/api/anthropic
```

## 📋 检查清单

在重新部署前确认：

- [ ] render.yaml格式正确（2空格缩进）
- [ ] requirements.txt中所有依赖可以安装
- [ ] 环境变量在Render Dashboard中设置
- [ ] main.py使用 `$PORT` 而不是硬编码
- [ ] 所有相对导入使用正确的语法

## 🔄 重新部署步骤

1. 在Render Dashboard中手动重新部署
2. 或者推送新触发自动部署
3. 查看日志确认启动成功

## 🆘 需要进一步帮助？

如果以上方法都试过但仍然失败：

1. 在Render Logs中复制完整的错误信息
2. 告诉我错误的具体内容
3. 我可以帮你进一步诊断问题

常见需要的信息：
- 具体的错误消息
- 错误发生的步骤（构建、启动等）
- Render Logs中的完整堆栈跟踪
- 是否有任何警告信息

---

**准备好重新部署了吗？** 🚀
