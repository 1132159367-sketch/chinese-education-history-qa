# Render 最小化部署指南

## 🚨 当前问题

错误：`Exited with status 1` 表示服务启动失败。

## 🧪 测试方法

### 方法1：最小配置部署

替换文件为简化版本：

```bash
# 1. 使用简化的render.yaml
mv render-minimal.yaml render.yaml

# 2. 使用简化的依赖
mv requirements-simple.txt requirements.txt

# 3. 提交并推送
git add .
git commit -m "Try minimal deployment"
git push origin main
```

### 方法2：手动创建服务

如果自动配置失败，手动创建：

1. 访问 https://dashboard.render.com/
2. 点击 **New Web Service**
3. 连接你的GitHub仓库
4. 手动配置：
   ```
   Name: education-qa-bot
   Environment: Python
   Build Command: pip install -r requirements.txt
   Start Command: python -m uvicorn app.main:app --host 0.0.0.0 --port $PORT
   Plan: Free
   ```

### 方法3：检查文件权限

确保所有文件都有正确的权限：

```bash
# 在本地测试启动
cd backend
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000
```

## 🔍 常见失败原因

### 1. 内存不足

Render免费层只有512MB内存，加载AI模型可能导致OOM。

**解决方法：**
- 移除或简化sentence-transformers模型
- 减少初始加载
- 使用更小的嵌入模型

### 2. 依赖安装超时

某些依赖包很大，安装可能超时。

**解决方法：**
- 移除版本限制
- 分开安装依赖
- 使用更小的模型

### 3. 启动命令错误

uvicorn的某些参数在Render环境中可能不工作。

**解决方法：**
- 使用最简单的启动命令
- 移除workers和复杂的配置
- 直接使用python -m uvicorn

## 💡 建议步骤

### 第一步：使用最小化配置

```bash
# 1. 使用简化版本
cp render-minimal.yaml render.yaml
cp requirements-simple.txt requirements.txt

# 2. 测试本地启动
cd backend
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000

# 3. 如果本地能启动，推送到GitHub
git add .
git commit -m "Try minimal configuration"
git push origin main
```

### 第二步：在Render中手动设置环境变量

如果自动部署仍然失败，在Render Dashboard中手动设置：

1. 进入你的服务 `education-qa-bot`
2. 点击 **"Environment"** 标签页
3. 添加环境变量：
   ```
   ZHIPU_API_KEY = 3f410ea451664d1d98882c496c598f70.1eGG7WBoMbiYGHsS
   ZHIPU_BASE_URL = https://api.z.ai/api/anthropic
   ```

### 第三步：监控部署日志

1. 在Render Dashboard中查看 **"Events"** 标签页
2. 点击失败的部署查看详细错误
3. 复制完整的错误堆栈跟踪

## 🎯 最小化文件的优势

### render-minimal.yaml
- ✅ 只包含必需配置
- ✅ 移除复杂的环境变量
- ✅ 移除磁盘存储配置（可以后续添加）
- ✅ 简化启动命令

### requirements-simple.txt
- ✅ 移除版本限制
- ✅ 只列出必要依赖
- ✅ 避免版本冲突

## 🔄 如果最小配置成功

如果最小配置部署成功，可以逐步添加功能：

1. **添加环境变量**
2. **添加磁盘存储**
3. **优化性能**

## 📋 故障排除检查清单

在查看Render Logs时检查：

- [ ] Python版本是否正确（需要Python 3.8+）
- [ ] 所有依赖是否能成功安装
- [ ] 启动命令是否正确
- [ ] 是否有导入错误
- [ ] 是否有语法错误
- [ ] 环境变量是否设置
- [ ] 文件路径是否正确

## 🆘 需要进一步帮助？

如果以上方法都尝试过，请提供：

1. **Render Logs中的完整错误堆栈**
2. **Events标签页显示的具体错误信息**
3. **是Build阶段失败还是启动阶段失败**

这样我可以进一步诊断和解决问题！

---

**建议先尝试最小化配置** 🚀
