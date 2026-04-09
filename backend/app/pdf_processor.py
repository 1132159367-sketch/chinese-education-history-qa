"""
PDF文件处理器
用于提取PDF文本内容和分块处理
"""

import pdfplumber
from typing import List, Dict
from pathlib import Path
import re
from fastapi import UploadFile
import aiofiles
import os


class PDFProcessor:
    """PDF文件处理器"""

    def __init__(self, pdf_dir: str):
        """
        初始化PDF处理器

        参数:
            pdf_dir: PDF文件存储目录
        """
        self.pdf_dir = Path(pdf_dir)
        self.pdf_dir.mkdir(exist_ok=True)

    async def save_pdf(self, file: UploadFile) -> str:
        """
        保存上传的PDF文件

        参数:
            file: 上传的文件对象

        返回:
            保存的文件路径
        """
        # 确保文件名安全
        filename = file.filename
        filename = re.sub(r'[^\w\-_\.]', '_', filename)

        file_path = self.pdf_dir / filename

        # 保存文件
        async with aiofiles.open(file_path, 'wb') as f:
            content = await file.read()
            await f.write(content)

        return str(file_path)

    def list_pdfs(self) -> List[str]:
        """
        列出所有PDF文件

        返回:
            PDF文件名列表
        """
        return [
            f.name
            for f in self.pdf_dir.glob("*.pdf")
            if f.is_file()
        ]

    def delete_pdf(self, filename: str):
        """
        删除PDF文件

        参数:
            filename: 要删除的文件名
        """
        file_path = self.pdf_dir / filename
        if file_path.exists():
            file_path.unlink()
        else:
            raise FileNotFoundError(f"文件 {filename} 不存在")

    def extract_text(self, filename: str, chunk_size: int = 500, overlap: int = 50) -> List[Dict[str, str]]:
        """
        提取PDF文本并分块

        参数:
            filename: PDF文件名
            chunk_size: 每块的字符数
            overlap: 块之间的重叠字符数

        返回:
            文档块列表，每个块包含 'text' 和 'metadata'
        """
        file_path = self.pdf_dir / filename

        if not file_path.exists():
            raise FileNotFoundError(f"文件 {filename} 不存在")

        documents = []
        full_text = ""
        page_texts = []

        # 使用pdfplumber提取文本
        try:
            with pdfplumber.open(file_path) as pdf:
                for page_num, page in enumerate(pdf.pages):
                    text = page.extract_text()
                    if text:
                        page_texts.append({
                            'page': page_num + 1,
                            'text': text
                        })
                        full_text += f"\n\n[第{page_num+1}页]\n{text}"
        except Exception as e:
            print(f"提取PDF文本时出错: {str(e)}")
            raise

        # 按段落分块
        chunks = self._chunk_by_paragraphs(full_text, chunk_size, overlap)

        # 为每个块创建文档记录
        for i, chunk in enumerate(chunks):
            # 找到这个块来自哪个页面
            page_num = self._find_page_for_chunk(chunk, page_texts)

            documents.append({
                'text': chunk,
                'metadata': {
                    'source': filename,
                    'page': page_num,
                    'chunk_id': i
                }
            })

        print(f"从 {filename} 提取了 {len(documents)} 个文档块")
        return documents

    def _chunk_by_paragraphs(self, text: str, chunk_size: int, overlap: int) -> List[str]:
        """
        按段落分块文本

        参数:
            text: 输入文本
            chunk_size: 每块最大字符数
            overlap: 重叠字符数

        返回:
            文本块列表
        """
        # 按段落分割
        paragraphs = [p.strip() for p in text.split('\n') if p.strip()]

        chunks = []
        current_chunk = ""

        for para in paragraphs:
            if len(current_chunk) + len(para) + 1 <= chunk_size:
                # 可以添加到当前块
                if current_chunk:
                    current_chunk += "\n" + para
                else:
                    current_chunk = para
            else:
                # 当前块已满，保存并开始新块
                if current_chunk:
                    chunks.append(current_chunk)

                # 处理重叠
                if overlap > 0 and current_chunk:
                    overlap_text = current_chunk[-overlap:]
                    current_chunk = overlap_text + "\n" + para
                else:
                    current_chunk = para

        # 添加最后一个块
        if current_chunk:
            chunks.append(current_chunk)

        return chunks

    def _find_page_for_chunk(self, chunk: str, page_texts: List[Dict]) -> int:
        """
        找到文本块来自哪个页面

        参数:
            chunk: 文本块
            page_texts: 页面文本列表

        返回:
            页码
        """
        # 找到包含该块内容的页面
        chunk_preview = chunk[:100]  # 使用块的前100个字符来匹配

        for page_info in page_texts:
            if chunk_preview in page_info['text']:
                return page_info['page']

        return 1  # 默认返回第一页
