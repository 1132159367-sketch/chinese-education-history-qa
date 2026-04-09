import requests

# 测试知识库初始化
print("正在测试知识库初始化...")

response = requests.post('http://localhost:8000/api/init-knowledge-base')

print(f"状态码: {response.status_code}")
print(f"响应内容: {response.text}")

if response.status_code == 200:
    data = response.json()
    print("[OK] 知识库初始化成功！")
    print(f"文档数量: {data['document_count']}")
    print(f"PDF数量: {data['pdf_count']}")
else:
    print("[ERROR] 初始化失败")
