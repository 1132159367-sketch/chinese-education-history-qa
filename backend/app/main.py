"""
中国古代教育史问答机器人 - FastAPI 主应用
使用智谱AI API 实现RAG问答系统
"""

from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import List, Optional
import os
from dotenv import load_dotenv
import json
from pathlib import Path

from .rag import RAGSystem
from .pdf_processor import PDFProcessor

# 加载环境变量
load_dotenv()

# 创建FastAPI应用
app = FastAPI(
    title="中国古代教育史问答机器人",
    description="基于智谱AI的RAG问答系统",
    version="1.0.0"
)

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 静态文件服务（前端）
frontend_dir = Path(__file__).parent.parent.parent / "frontend"
app.mount("/static", StaticFiles(directory=str(frontend_dir)), name="static")

# 全局变量
rag_system = None
pdf_processor = None
conversation_history = {}  # 存储对话历史 {session_id: [{role, content}]}


class Question(BaseModel):
    """用户问题模型"""
    question: str
    session_id: str = "default"


class AnswerResponse(BaseModel):
    """回答响应模型"""
    answer: str
    sources: List[str]
    context_used: bool


class ConversationHistory(BaseModel):
    """对话历史模型"""
    session_id: str
    messages: List[dict]


def get_rag_system() -> RAGSystem:
    """获取或初始化RAG系统"""
    global rag_system
    if rag_system is None:
        # 从环境变量获取配置
        zhipu_api_key = os.getenv("ZHIPU_API_KEY")
        if not zhipu_api_key:
            raise ValueError("请设置 ZHIPU_API_KEY 环境变量")

        rag_system = RAGSystem(
            api_key=zhipu_api_key,
            base_url=os.getenv("ZHIPU_BASE_URL", "https://api.z.ai/api/anthropic")
        )
    return rag_system


def get_pdf_processor() -> PDFProcessor:
    """获取PDF处理器"""
    global pdf_processor
    if pdf_processor is None:
        pdf_dir = Path(__file__).parent.parent / "pdfs"
        pdf_dir.mkdir(exist_ok=True)
        pdf_processor = PDFProcessor(pdf_dir=str(pdf_dir))
    return pdf_processor


@app.on_event("startup")
async def startup_event():
    """应用启动时的事件处理"""
    print("=" * 50)
    print("中国古代教育史问答机器人启动中...")
    print("=" * 50)

    # 检查API配置
    api_key = os.getenv("ZHIPU_API_KEY")
    if not api_key:
        print("[WARNING] 警告: 未设置 ZHIPU_API_KEY，请配置后重启服务")
    else:
        print("[OK] 智谱AI API Key 已配置")

    # 检查PDF文件
    pdf_processor = get_pdf_processor()
    pdf_files = pdf_processor.list_pdfs()

    if pdf_files:
        print(f"[OK] 找到 {len(pdf_files)} 个PDF文件:")
        for pdf in pdf_files:
            print(f"  - {pdf}")
    else:
        print("[WARNING] 未找到PDF文件，请上传知识库文件")


@app.get("/")
async def root():
    """根路径 - 返回前端页面"""
    return FileResponse(str(frontend_dir / "index.html"))


@app.get("/health")
async def health_check():
    """健康检查"""
    return {"status": "ok", "service": "中国古代教育史问答机器人"}


@app.post("/api/upload-pdf")
async def upload_pdf(file: UploadFile = File(...)):
    """
    上传PDF文件

    参数:
        file: PDF文件

    返回:
        文件名和处理状态
    """
    try:
        # 验证文件类型
        if not file.filename.lower().endswith('.pdf'):
            raise HTTPException(status_code=400, detail="只支持PDF文件")

        # 保存文件
        pdf_processor = get_pdf_processor()
        file_path = await pdf_processor.save_pdf(file)

        return {
            "message": "PDF上传成功",
            "filename": file.filename,
            "path": file_path
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"上传失败: {str(e)}")


@app.get("/api/pdfs")
async def list_pdfs():
    """
    获取已上传的PDF文件列表

    返回:
        PDF文件列表
    """
    try:
        pdf_processor = get_pdf_processor()
        pdf_files = pdf_processor.list_pdfs()
        return {"pdfs": pdf_files}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.delete("/api/pdfs/{filename}")
async def delete_pdf(filename: str):
    """
    删除PDF文件

    参数:
        filename: PDF文件名

    返回:
        删除结果
    """
    try:
        pdf_processor = get_pdf_processor()
        result = pdf_processor.delete_pdf(filename)
        return {"message": f"文件 {filename} 已删除"}
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="文件不存在")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/init-knowledge-base")
async def init_knowledge_base():
    """
    初始化知识库（从PDF构建向量索引）

    返回:
        初始化结果和文档数量
    """
    try:
        # 获取PDF处理器
        pdf_processor = get_pdf_processor()

        # 提取所有PDF文本
        all_documents = []
        pdf_files = pdf_processor.list_pdfs()

        if not pdf_files:
            raise HTTPException(
                status_code=400,
                detail="未找到PDF文件，请先上传知识库"
            )

        print(f"\n开始处理 {len(pdf_files)} 个PDF文件...")

        for pdf_file in pdf_files:
            print(f"处理文件: {pdf_file}")
            documents = pdf_processor.extract_text(pdf_file)
            all_documents.extend(documents)

        if not all_documents:
            raise HTTPException(
                status_code=400,
                detail="未能从PDF中提取到文本内容"
            )

        # 构建向量索引
        rag = get_rag_system()
        rag.build_index(all_documents)

        print(f"✓ 知识库初始化完成，共 {len(all_documents)} 个文档片段")

        return {
            "message": "知识库初始化成功",
            "document_count": len(all_documents),
            "pdf_count": len(pdf_files)
        }
    except Exception as e:
        print(f"初始化知识库失败: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/ask", response_model=AnswerResponse)
async def ask_question(question_data: Question):
    """
    回答用户问题

    参数:
        question_data: 包含问题和会话ID的数据

    返回:
        答案和参考来源
    """
    try:
        # 获取RAG系统
        rag = get_rag_system()

        # 检查是否已初始化知识库
        if not rag.is_index_built():
            raise HTTPException(
                status_code=400,
                detail="知识库未初始化，请先上传PDF文件并初始化知识库"
            )

        # 获取对话历史
        session_id = question_data.session_id
        history = conversation_history.get(session_id, [])

        # 调用RAG系统回答问题
        result = rag.answer(
            question=question_data.question,
            conversation_history=history
        )

        # 更新对话历史
        conversation_history[session_id] = result["updated_history"]

        return AnswerResponse(
            answer=result["answer"],
            sources=result["sources"],
            context_used=result["context_used"]
        )

    except Exception as e:
        print(f"回答问题时出错: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/history/{session_id}")
async def get_conversation_history(session_id: str):
    """
    获取指定会话的对话历史

    参数:
        session_id: 会话ID

    返回:
        对话历史
    """
    history = conversation_history.get(session_id, [])
    return {"session_id": session_id, "messages": history}


@app.delete("/api/history/{session_id}")
async def delete_conversation(session_id: str):
    """
    删除指定会话的对话历史

    参数:
        session_id: 会话ID

    返回:
        删除结果
    """
    if session_id in conversation_history:
        del conversation_history[session_id]
        return {"message": f"会话 {session_id} 已删除"}
    else:
        return {"message": "会话不存在"}


@app.get("/api/sessions")
async def list_sessions():
    """
    获取所有会话列表

    返回:
        会话ID列表
    """
    return {"sessions": list(conversation_history.keys())}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
