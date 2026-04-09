# 安全配置指南

## 🚨 重要：永远不要将API Key上传到GitHub

### ❌ 危险做法（不要这样）：

```python
# 永远不要这样做！
API_KEY = "sk-xxxxxxxxxxxxx"  # ❌ 硬编码API Key

# 永远不要这样做！
render.yaml:
  envVars:
    - key: API_KEY
      value: "sk-xxxxxxxxxxxxx"  # ❌ 在配置文件中填入真实Key
```

### ✅ 正确做法（应该这样）：

```python
# 正确的做法：使用环境变量
api_key = os.getenv("ZHIPU_API_KEY")  # ✅ 从环境变量读取

if not api_key:
    raise ValueError("请设置 ZHIPU_API_KEY 环境变量")  # ✅ 提供清晰的错误提示
```

```yaml
# 正确的做法：在部署平台设置环境变量
render.yaml:
  envVars:
    - key: ZHIPU_API_KEY      # ✅ 只定义变量名
      sync: false               # ✅ 不同步到其他服务
      # ❌ 不要在这里填入value！
```

## 🔑 环境变量配置

### 本地开发

创建 `.env` 文件：

```bash
# .env 文件（不会上传到GitHub，因为有.gitignore）
ZHIPU_API_KEY=你的智谱AI密钥
ZHIPU_BASE_URL=https://api.z.ai/api/anthropic
```

### Render部署

1. 在GitHub上只有 `.env.example` 文件
2. 在Render Dashboard中手动设置环境变量：
   - 变量名：`ZHIPU_API_KEY`
   - 值：你的真实API Key
3. 不要在 `render.yaml` 中填入 `value`

## ⚠️ 常见的安全错误

### 错误1：大小写不一致

```python
# 代码中
api_key = os.getenv("API_KEY")  # 大写

# Render中设置
api_key = "sk-xxxxx"          # ❌ 错误！变量名不匹配
```

**解决方法：** 确保变量名完全一致，包括大小写
```python
# 代码和配置中都要用大写
API_KEY = os.getenv("API_KEY")
```

### 错误2：变量名拼写错误

```python
# 代码中
key = os.getenv("API_KEYS")  # 多了一个's'

# Render中设置
API_KEY = "sk-xxxxx"         # ❌ 变量名不匹配！
```

### 错误3：硬编码在配置文件中

```yaml
# render.yaml
envVars:
  - key: API_KEY
    value: "sk-xxxxxxxxxxxxx"  # ❌ 这个value会被上传到GitHub！
```

## 🎯 当前项目配置

### ✅ 已确保的安全措施

1. **代码中使用环境变量**：
   ```python
   zhipu_api_key = os.getenv("ZHIPU_API_KEY")
   if not zhipu_api_key:
       raise ValueError("请设置 ZHIPU_API_KEY 环境变量")
   ```

2. **render.yaml中正确配置**：
   ```yaml
   envVars:
     - key: ZHIPU_API_KEY
       sync: false
     - key: ZHIPU_BASE_URL
       value: https://api.z.ai/api/anthropic
   ```

3. **.gitignore包含.env**：
   ```
   # .gitignore
   .env    # ✅ 本地环境变量文件
   ```

4. **提供示例文件**：
   ```
   # .env.example
   ZHIPU_API_KEY=your_api_key_here
   ```

## 📋 部署检查清单

在部署到Render之前，确认：

- [ ] 代码中没有硬编码API Key
- [ ] 使用os.getenv()读取环境变量
- [ ] .gitignore包含.env
- [ ] .env.example作为模板文件上传
- [ ] render.yaml中没有value字段
- [ ] 变量名在代码和配置中完全一致
- [ ] 提供清晰的错误提示（如变量未设置）

## 🔍 检查方法

### 检查GitHub仓库

```bash
# 确保没有敏感信息
git log --all --full

# 检查.env是否被提交
git log --all -- .env

# 确认.gitignore生效
git check-ignore -v .env
```

### 本地测试

```bash
# 测试环境变量读取
python -c "import os; print(os.getenv('ZHIPU_API_KEY'))"  # 应该返回空

# 测试本地配置
cd backend
python -m uvicorn app.main:app --port 8000
```

## 🚨 如果发现安全问题

1. 立即停止部署
2. 修改提交历史（如需要）
3. 更新代码移除敏感信息
4. 强制推送到新分支（清除敏感提交）
5. 重新生成API Key
6. 部署修复后的版本

---

**记住：安全第一！** 🔐

永远不要将任何API Key、密码或敏感信息上传到公共代码仓库！
