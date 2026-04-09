"""
智谱AI API客户端
"""

import httpx
import os
from dotenv import load_dotenv

load_dotenv()

class ZhipuAIClient:
    """智谱AI API客户端"""

    def __init__(self, api_key: str = None, base_url: str = None):
        """
        初始化智谱AI客户端

        参数:
            api_key: API密钥
            base_url: API基础URL
        """
        self.api_key = api_key or os.getenv("ZHIPU_API_KEY")
        self.base_url = base_url or os.getenv("ZHIPU_BASE_URL", "https://open.bigmodel.cn/api/paas/v4")

        if not self.api_key:
            raise ValueError("请设置 ZHIPU_API_KEY 环境变量")

        self.client = httpx.Client(timeout=60.0)

    def chat(self, messages: list, model: str = "glm-4", system_prompt: str = None, max_tokens: int = 2000, temperature: float = 0.3) -> dict:
        """
        聊天接口

        参数:
            messages: 消息列表
            model: 模型名称
            system_prompt: 系统提示词
            max_tokens: 最大token数
            temperature: 温度参数

        返回:
            响应结果
        """
        # 构建请求体
        payload = {
            "model": model,
            "messages": messages,
            "max_tokens": max_tokens,
            "temperature": temperature
        }

        # 添加系统提示词
        if system_prompt:
            payload["messages"].insert(0, {
                "role": "system",
                "content": system_prompt
            })

        # 发送请求
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        try:
            response = self.client.post(
                f"{self.base_url}/chat/completions",
                json=payload,
                headers=headers
            )
            response.raise_for_status()
            return response.json()

        except httpx.HTTPStatusError as e:
            error_msg = f"HTTP {e.response.status_code}: {e.response.text}"
            raise Exception(error_msg)
        except Exception as e:
            raise Exception(f"智谱AI API调用失败: {str(e)}")

    def close(self):
        """关闭客户端"""
        self.client.close()
