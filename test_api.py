import anthropic
from dotenv import load_dotenv
import os

load_dotenv()

api_key = os.getenv("ZHIPU_API_KEY")
base_url = os.getenv("ZHIPU_BASE_URL")

print(f"API Key: {api_key[:20]}...")
print(f"Base URL: {base_url}")

# 测试智谱AI API
client = anthropic.Anthropic(
    api_key=api_key,
    base_url=base_url
)

try:
    # 尝试不同的模型名称
    models_to_test = ["glm-4", "glm-3-turbo", "gpt-4"]

    for model in models_to_test:
        print(f"\n正在测试模型: {model}")
        try:
            response = client.messages.create(
                model=model,
                max_tokens=100,
                messages=[{"role": "user", "content": "你好"}]
            )
            print(f"[OK] {model} 模型可用!")
            print(f"响应: {response.content[0].text}")
            break  # 找到可用模型就停止
        except Exception as e:
            print(f"[ERROR] {model} 不可用: {str(e)}")

except Exception as e:
    print(f"[ERROR] API连接失败: {str(e)}")
