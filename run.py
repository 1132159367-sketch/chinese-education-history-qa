"""
简单的启动脚本
解决Railway部署问题
"""

import os
import sys

# 添加backend目录到Python路径
project_root = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'backend')
if project_root not in sys.path:
    sys.path.insert(0, project_root)

if __name__ == "__main__":
    try:
        from app.main import app
        import uvicorn

        # 使用最简单的启动方式
        uvicorn.run(
            app,
            host="0.0.0.0",
            port=int(os.getenv("PORT", 8000))
        )
    except ImportError as e:
        print(f"Error importing app: {e}")
        print(f"Current directory: {os.getcwd()}")
        print(f"Project root: {project_root}")
        print(f"Sys.path: {sys.path}")
        sys.exit(1)

