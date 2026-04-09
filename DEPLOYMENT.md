# 部署指南

## 快速部署方案

### 方案1：使用 ngrok（5分钟部署）

适用于：快速测试、本地演示、临时使用

```bash
# 1. 下载 ngrok
# 访问 https://ngrok.com/download

# 2. 启动你的项目
cd backend
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000

# 3. 启动 ngrok
ngrok http 8000

# 4. 复制 ngrok 提供的公网地址，例如：
# https://abc123.ngrok.io
```

### 方案2：使用 Cloudflare Tunnel（免费且稳定）

适用于：长期使用、稳定域名

```bash
# 1. 安装 cloudflared
# Windows: https://github.com/cloudflare/cloudflared/releases
# Linux: wget https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64
#         chmod +x cloudflared-linux-amd64

# 2. 登录 Cloudflare
cloudflared tunnel login

# 3. 创建隧道
cloudflared tunnel create education-qa

# 4. 配置隧道
cloudflared tunnel route dns education-qa your-domain.com

# 5. 启动隧道
cloudflared tunnel --url http://localhost:8000
```

### 方案3：Docker 部署（推荐）

适用于：生产环境、易于管理、可移植

```bash
# 1. 构建 Docker 镜像
docker-compose build

# 2. 启动服务
docker-compose up -d

# 3. 查看日志
docker-compose logs -f

# 4. 停止服务
docker-compose down
```

### 方案4：云服务器部署（推荐用于生产）

#### 阿里云/腾讯云 部署步骤

```bash
# 1. 连接到服务器
ssh root@your-server-ip

# 2. 安装必要软件
sudo apt update
sudo apt install -y python3 python3-pip python3-venv nginx git

# 3. 克隆或上传项目
# 方式A: 使用git
git clone <你的项目地址>
cd chinese-education-history-qa

# 方式B: 使用scp上传
# 在本地执行：scp -r 项目目录 root@server-ip:/root/

# 4. 配置环境
cd chinese-education-history-qa
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# 5. 配置环境变量
cp .env.example .env
nano .env  # 填入你的API Key

# 6. 创建 systemd 服务
sudo nano /etc/systemd/system/education-qa.service
```

**service 文件内容：**
```ini
[Unit]
Description=中国古代教育史问答机器人
After=network.target

[Service]
User=root
WorkingDirectory=/root/chinese-education-history-qa/backend
Environment="PATH=/root/chinese-education-history-qa/venv/bin"
ExecStart=/root/chinese-education-history-qa/venv/bin/gunicorn app.main:app \
    --workers 4 \
    --worker-class uvicorn.workers.UvicornWorker \
    --bind 127.0.0.1:8000
Restart=always

[Install]
WantedBy=multi-user.target
```

```bash
# 7. 启动服务
sudo systemctl start education-qa
sudo systemctl enable education-qa
sudo systemctl status education-qa

# 8. 配置 Nginx
sudo nano /etc/nginx/sites-available/education-qa
```

**Nginx 配置：**
```nginx
server {
    listen 80;
    server_name your-domain.com;

    client_max_body_size 100M;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

```bash
# 9. 启用 Nginx 配置
sudo ln -s /etc/nginx/sites-available/education-qa /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx

# 10. 配置 SSL（可选但推荐）
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d your-domain.com
```

## 安全配置

### 防火墙配置

```bash
# UFW (Ubuntu)
sudo ufw allow 22    # SSH
sudo ufw allow 80    # HTTP
sudo ufw allow 443   # HTTPS
sudo ufw enable

# 阿里云安全组
# 在控制台添加入站规则：80, 443 端口
```

### API Key 保护

```bash
# 设置正确的文件权限
chmod 600 .env

# 不要将 .env 文件提交到 Git（已在 .gitignore 中）
```

### 限制上传大小

在 Nginx 配置中已设置：
```nginx
client_max_body_size 100M;  # 限制最大上传100MB
```

## 监控和维护

### 查看服务状态

```bash
# systemd 服务
sudo systemctl status education-qa

# 查看日志
sudo journalctl -u education-qa -f

# Docker 服务
docker-compose logs -f
```

### 自动重启

systemd 配置中已设置 `Restart=always`，服务会自动重启

### 备份数据

```bash
# 备份 PDF 文件
tar -czf pdfs_backup_$(date +%Y%m%d).tar.gz backend/pdfs/

# 备份配置
cp .env .env.backup
```

## 性能优化

### Gunicorn 配置

```bash
# 根据 CPU 核心数调整 workers 数量
# 推荐公式：2 * CPU核心数 + 1
--workers 4  # 4核CPU
```

### Nginx 缓存（可选）

```nginx
proxy_cache_path /var/cache/nginx levels=1:2 keys_zone=api_cache:10m max_size=1g inactive=60m;

server {
    location / {
        proxy_cache api_cache;
        proxy_pass http://127.0.0.1:8000;
        proxy_cache_valid 200 10m;
        add_header X-Cache-Status $upstream_cache_status;
    }
}
```

## 故障排除

### 服务无法启动

```bash
# 检查端口占用
sudo netstat -tlnp | grep 8000

# 检查日志
sudo journalctl -u education-qa -n 50
```

### 无法访问网站

```bash
# 检查服务状态
curl http://localhost:8000/health

# 检查 Nginx 配置
sudo nginx -t

# 检查防火墙
sudo ufw status
```

### PDF 上传失败

```bash
# 检查目录权限
ls -la backend/pdfs/

# 检查 Nginx 配置中的 client_max_body_size
sudo nginx -t
```

## 成本估算

### 各方案成本对比

| 方案 | 成本 | 适用场景 |
|------|------|---------|
| ngrok 免费版 | 免费 | 开发测试 |
| Cloudflare Tunnel | 免费 | 个人使用 |
| 阿里云 ECS (1核2G) | ~50元/月 | 小型项目 |
| 阿里云 ECS (2核4G) | ~150元/月 | 推荐配置 |
| 域名 | ~50元/年 | 可选 |

## 推荐方案

### 个人学习/测试
**推荐：Cloudflare Tunnel**
- 免费
- 稳定
- 无需购买服务器

### 生产环境
**推荐：阿里云/腾讯云 + Nginx**
- 稳定可靠
- 性能好
- 可扩展
- 适合长期使用

### 快速部署
**推荐：Docker**
- 一键部署
- 环境隔离
- 易于迁移

---

需要帮助选择适合你的部署方案吗？
