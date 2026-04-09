import requests

# 测试问答功能
print("正在测试问答功能...")

test_question = "西周的教育制度有什么特点？"

response = requests.post('http://localhost:8000/api/ask', json={
    'question': test_question,
    'session_id': 'test_session_001'
})

print(f"状态码: {response.status_code}")

if response.status_code == 200:
    data = response.json()
    print("[OK] 问答成功！")
    print(f"\n问题: {test_question}")
    print(f"\n回答: {data['answer']}")
    print(f"\n来源: {data['sources']}")
    print(f"使用上下文: {data['context_used']}")
else:
    print("[ERROR] 问答失败")
    print(f"错误信息: {response.text}")
