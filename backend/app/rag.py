"""
RAG（检索增强生成）系统
实现文档检索和答案生成
"""

import anthropic
from typing import List, Dict, Tuple
import numpy as np
from sentence_transformers import SentenceTransformer
import faiss
import tiktoken

class RAGSystem:
    """RAG问答系统"""

    def __init__(self, api_key: str = None, base_url: str = "https://api.z.ai/api/anthropic"):
        """
        初始化RAG系统

        参数:
            api_key: 智谱AI API密钥
            base_url: API基础URL
        """
        self.api_key = api_key
        self.base_url = base_url
        self.client = anthropic.Anthropic(
            api_key=api_key,
            base_url=base_url
        )

        # 加载中文句子嵌入模型
        print("正在加载嵌入模型...")
        self.embedder = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')
        print("[OK] 嵌入模型加载完成")

        # FAISS索引
        self.index = None
        self.documents = []  # 存储文档内容
        self.metadata = []  # 存储文档元数据

        # 角色设定
        self.system_prompt = """你是一位教育学专业的考研辅导老师，专门研究中国古代教育史。

你的回答风格：
- 严谨、专业、学术化
- 条理清晰，逻辑严密
- 适合考研备考的专业水准
- 引用具体的历史事实和教育制度

重要约束：
1. 必须严格基于提供的知识库内容回答问题
2. 如果问题超出知识库范围，必须明确说明："该问题超出当前知识库范围，无法作答"
3. 禁止编造或虚构任何历史事实
4. 回答时要注明引用的知识库片段

回答结构：
- 先给出明确的答案
- 详细解释相关教育制度或历史背景
- 如有必要，引用知识库中的具体内容作为支撑
- 保持学术严谨性
"""

    def build_index(self, documents: List[Dict[str, str]]):
        """
        构建向量索引

        参数:
            documents: 文档列表，每个文档包含 'text' 和 'metadata' 字段
        """
        print("正在构建向量索引...")

        self.documents = [doc['text'] for doc in documents]
        self.metadata = [doc['metadata'] for doc in documents]

        # 生成嵌入向量
        embeddings = self.embedder.encode(self.documents)

        # 创建FAISS索引
        dimension = embeddings.shape[1]
        self.index = faiss.IndexFlatL2(dimension)
        self.index.add(embeddings.astype('float32'))

        print(f"[OK] 向量索引构建完成，共 {len(documents)} 个文档片段")

    def is_index_built(self) -> bool:
        """检查索引是否已构建"""
        return self.index is not None

    def retrieve(self, query: str, top_k: int = 3) -> List[Dict[str, str]]:
        """
        检索相关文档

        参数:
            query: 查询文本
            top_k: 返回前k个最相关的文档

        返回:
            相关文档列表
        """
        # 生成查询的嵌入向量
        query_embedding = self.embedder.encode([query])

        # 搜索
        distances, indices = self.index.search(query_embedding.astype('float32'), top_k)

        # 返回结果
        results = []
        for i, (distance, idx) in enumerate(zip(distances[0], indices[0])):
            if idx < len(self.documents):
                results.append({
                    'text': self.documents[idx],
                    'metadata': self.metadata[idx],
                    'score': float(distance)
                })

        return results

    def count_tokens(self, text: str) -> int:
        """计算文本的token数量"""
        encoding = tiktoken.get_encoding("cl100k_base")
        return len(encoding.encode(text))

    def truncate_context(self, contexts: List[str], max_tokens: int = 8000) -> str:
        """
        截断上下文以避免超出token限制

        参数:
            contexts: 上下文列表
            max_tokens: 最大token数

        返回:
            截断后的上下文字符串
        """
        combined = "\n\n---\n\n".join(contexts)

        # 如果未超出限制，直接返回
        if self.count_tokens(combined) <= max_tokens:
            return combined

        # 否则逐个移除上下文
        for i in range(len(contexts)):
            truncated = "\n\n---\n\n".join(contexts[:len(contexts)-i])
            if self.count_tokens(truncated) <= max_tokens:
                return truncated

        return contexts[0][:max_tokens * 3]  # 最后的手段：直接截断文本

    def answer(self, question: str, conversation_history: List[Dict[str, str]] = None) -> Dict:
        """
        回答问题

        参数:
            question: 用户问题
            conversation_history: 对话历史

        返回:
            包含答案、来源、上下文使用情况和更新历史的字典
        """
        if conversation_history is None:
            conversation_history = []

        # 检索相关文档
        retrieved_docs = self.retrieve(question, top_k=3)

        if not retrieved_docs:
            # 没有检索到相关文档
            answer = "该问题超出当前知识库范围，无法作答。知识库中可能不包含与此问题相关的信息。"
            return {
                "answer": answer,
                "sources": [],
                "context_used": False,
                "updated_history": conversation_history + [
                    {"role": "user", "content": question},
                    {"role": "assistant", "content": answer}
                ]
            }

        # 构建上下文
        contexts = [doc['text'] for doc in retrieved_docs]
        context_text = self.truncate_context(contexts)

        # 构建用户消息
        user_message = f"""请基于以下知识库内容回答问题：

知识库内容：
{context_text}

问题：{question}

如果知识库内容不足以回答该问题，请明确说明"该问题超出当前知识库范围，无法作答"，不要编造任何信息。"""

        # 准备消息列表
        messages = conversation_history.copy()
        messages.append({"role": "user", "content": user_message})

        # 调用智谱AI API
        try:
            response = self.client.messages.create(
                model="claude-3-5-sonnet-20241022",  # 模型名称
                max_tokens=2000,
                temperature=0.3,
                system=self.system_prompt,
                messages=messages
            )

            answer = response.content[0].text

            # 提取参考来源
            sources = [
                f"{doc['metadata']['source']} - {doc['metadata'].get('page', '未知页码')}"
                for doc in retrieved_docs
            ]

            # 更新对话历史（不包含详细的上下文）
            updated_history = conversation_history + [
                {"role": "user", "content": question},
                {"role": "assistant", "content": answer}
            ]

            return {
                "answer": answer,
                "sources": sources,
                "context_used": True,
                "updated_history": updated_history
            }

        except Exception as e:
            error_msg = f"生成答案时出错: {str(e)}"
            print(error_msg)
            return {
                "answer": error_msg,
                "sources": [],
                "context_used": False,
                "updated_history": conversation_history + [
                    {"role": "user", "content": question},
                    {"role": "assistant", "content": error_msg}
                ]
            }
