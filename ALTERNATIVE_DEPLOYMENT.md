# 替代部署方案

## 🎯 Render 出错时的替代方案

| 平台 | 月费 | 免费存储 | 推荐度 | 部署难度 |
|------|------|---------|---------|---------|
| **Railway** | $5 | 1GB | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| **Fly.io** | $0 | 3GB | ⭐⭐⭐ | ⭐⭐⭐ |
| **Zeabur** | $0 | 1GB | ⭐⭐⭐⭐ | ⭐⭐⭐ |
| **Hugging Face** | $0 | 100MB | ⭐⭐⭐ | ⭐⭐ |
| **Streamlit Cloud** | $0 | 有限 | ⭐⭐⭐⭐ | ⭐⭐⭐ |

## 🚀 方案1：Railway（最推荐）

### 为什么选择Railway：

1. **最易用** - 界面友好，配置简单
2. **完全免费** - $5/月，但功能完整
3. **Python支持好** - FastAPI完美支持
4. **文档完善** - 中文支持良好
5. **社区活跃** - 问题解决快

### Railway 部署步骤：

#### 方法A：连接GitHub（推荐）

1. 访问 https://railway.app/
2. 使用GitHub账号登录
3. 点击 **"New Project"** 或 **"+"** 按钮
4. 选择 **"Deploy from GitHub repo"**
5. 选择仓库：`1132159367-sketch/chinese-education-history-qa`
6. 点击 **"Deploy Now"**

#### 方法B：使用CLI部署

```bash
# 1. 安装Railway CLI
npm install -g @railway/cli

# 2. 登录
railway login

# 3. 初始化项目
railway init

# 4. 部署
railway up

# 5. 查看日志
railway logs
```

### 环境变量配置：

在Railway Dashboard中设置：
```bash
ZHIPU_API_KEY = 3f410ea451664d1d98882c496c598f70.1eGG7WBoMbiYGHsS
ZHIPU_BASE_URL = https://api.z.ai/api/anthropic
```

### Railway 特点：

✅ **优点**：
- 简单易用的界面
- 自动GitHub集成
- 实时日志查看
- 域名：`your-app.railway.app`
- 支持自定义域名
- 持久化存储支持
- 免费SSL证书

⚠️ **限制**：
- 免费层：$5/月（但新用户有试用）
- 内存：512MB
- 带宽：100GB/月

## 🚀 方案2：Fly.io

### Fly.io 部署步骤：

```bash
# 1. 安装Fly CLI
curl -L https://fly.io/install.sh | sh

# 2. 登录
flyctl auth login

# 3. 初始化项目
flyctl init

# 4. 部署
flyctl deploy

# 5. 查看状态
flyctl status

# 6. 查看日志
flyctl logs
```

### Fly.io 特点：

✅ **优点**：
- 永久免费（有限制）
- 全球边缘部署
- 自动SSL证书
- 数据库支持（免费Postgres）
- Docker容器支持

⚠️ **限制**：
- 免费层：3个共享CPU，256MB内存
- 启动时间：每次重启需要1-2分钟
- 带宽：160GB出站/月

## 🚀 方案3：Zeabur（完全免费）

### Zeabur 部署步骤：

```bash
# 1. 安装Zeabur CLI
npm install -g @zeabur/cli

# 2. 登录
zeabur login

# 3. 创建应用
zeabur init education-qa-bot

# 4. 部署
zeabur deploy

# 5. 查看日志
zeabur logs --tail
```

### Zeabur 特点：

✅ **优点**：
- 完全免费（无付费计划）
- 全球CDN加速
- 自动SSL证书
- 支持持久化存储
- 良好的文档

⚠️ **限制**：
- 容器重启后会丢失数据（除非使用存储）
- 512MB内存限制
- 冷启动较慢

## 🚀 方案4：Hugging Face Spaces

### Hugging Face 部署步骤：

1. 访问 https://huggingface.co/new-space
2. 选择空间类型：**New Space**
3. 配置信息：
   - **Space name**: `education-qa-bot`
   - **License**: MIT
   - **SDK**: Docker
   - **Docker template**: Python FastAPI
4. 在Settings中添加Secrets：
   ```
   ZHIPU_API_KEY = 你的密钥
   ZHIPU_BASE_URL = https://api.z.ai/api/anthropic
   ```
5. 点击 **"Create Space"**

### Hugging Face 特点：

✅ **优点**：
- 完全免费
- 机器学习社区集成
- 模型分享平台
- 简单的Web界面
- 实时预览

⚠️ **限制**：
- 100MB存储限制
- 适合模型演示而非完整应用
- Python版本可能有限制

## 🚀 方案5：本地部署 + 内网穿透

### 使用ngrok本地部署：

```bash
# 1. 安装ngrok
# 下载：https://ngrok.com/download

# 2. 本地启动项目
cd backend
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000

# 3. 启动ngrok
ngrok http 8000

# 4. 复制ngrok提供的链接
# 例如：https://abc123.ngrok.io
```

### 优点：
- ✅ 完全控制本地环境
- ✅ 立即可用
- ✅ 无部署限制

### 缺点：
- ❌ 需要保持本地服务运行
- ❌ 每次重启地址会变
- ❌ 适合临时演示

## 🎯 综合推荐

### 最推荐：Railway

**理由**：
1. 最易用的界面，配置简单
2. 与GitHub完美集成
3. 文档完善，中文支持好
4. 错误提示清晰，问题解决快
5. 适合生产环境使用

### 次推荐：Fly.io

**理由**：
1. 功能完整，稳定性好
2. 全球边缘部署，性能佳
3. 免费层功能相对丰富
4. Docker支持，部署标准化

### 第三推荐：ngrok（临时方案）

**理由**：
1. 立即可用，无需等待
2. 适合快速演示和测试
3. 完全控制本地环境
4. 可以先验证配置再部署

## 📋 部署前检查清单

在尝试任何部署前，确认：

- [ ] 本地项目可以正常启动
- [ ] 所有依赖已安装
- [ ] 环境变量配置正确
- [ ] .gitignore包含敏感文件
- [ ] GitHub仓库是最新的
- [ ] 知道部署平台的具体要求

## 🔧 故障排除

### 如果所有平台都失败：

1. **检查代码兼容性**：
   ```bash
   # 检查Python版本
   python --version  # 需要3.8+

   # 检查依赖
   pip list
   ```

2. **最小化项目测试**：
   - 只保留核心功能
   - 移除复杂的依赖
   - 使用最简单的启动命令

3. **使用Docker镜像**：
   - 创建Dockerfile
   - 使用标准Python镜像
   - 避免本地依赖问题

4. **查看详细日志**：
   - 记录完整的错误堆栈
   - 查看具体哪个步骤失败
   - 搜索类似的已知问题

## 🎉 成功部署后

一旦部署成功：

1. **上传PDF文件** - 在应用界面上传你的PDF
2. **初始化知识库** - 点击初始化按钮
3. **测试问答功能** - 问几个问题验证功能
4. **分享链接** - 把应用地址分享给别人使用

## 💰 费用对比总结

| 平台 | 完全免费 | 月费 | 存储空间 | 适合场景 |
|------|----------|------|---------|---------|
| **Railway** | ❌ | $5 | 1GB | 🌟 生产环境 |
| **Fly.io** | ⭐⭐⭐ | $0 | 3GB | 🌟 生产环境 |
| **Zeabur** | ⭐⭐⭐⭐ | $0 | 1GB | 🌟 个人项目 |
| **Hugging Face** | ⭐⭐⭐⭐ | $0 | 100MB | 🔧 模型演示 |
| **ngrok** | ⭐⭐⭐⭐ | $0 | 无限制 | 🧪 临时测试 |

---

**建议先尝试Railway，如果不行再试Fly.io！** 🚀
