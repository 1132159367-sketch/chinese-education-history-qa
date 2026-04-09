@echo off
chcp 65001 > nul
echo ==========================================
echo 中国古代教育史问答机器人 - 启动脚本
echo ==========================================
echo.

REM 检查Python是否安装
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo 错误：未检测到Python，请先安装Python 3.8+
    pause
    exit /b 1
)

echo [1/5] 检查环境...
python --version

echo.
echo [2/5] 安装依赖包...
pip install -r requirements.txt

echo.
echo [3/5] 检查环境变量...
if not exist .env (
    echo 警告：未找到.env文件
    echo.
    echo 请按照以下步骤配置：
    echo 1. 复制 .env.example 为 .env
    echo 2. 在智谱AI官网获取API Key: https://open.bigmodel.cn/
    echo 3. 将API Key填入 .env 文件
    echo.
    pause
) else (
    echo ✓ .env 文件存在
)

echo.
echo [4/5] 检查PDF目录...
if not exist backend\pdfs (
    mkdir backend\pdfs
    echo ✓ 创建 backend\pdfs 目录
)

echo.
echo [5/5] 启动服务...
echo.
echo ==========================================
echo 服务启动成功！
echo 请在浏览器中访问：http://localhost:8000
echo 按 Ctrl+C 停止服务
echo ==========================================
echo.

cd backend
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

pause
