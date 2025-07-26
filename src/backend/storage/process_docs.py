from typing import List
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.docstore.document import Document
from PyPDF2 import PdfReader

def load_pdf(path) -> List[Document]:
    reader = PdfReader(path)
    documents = []
    for page_number in range(len(reader.pages)):
        page = reader.pages[page_number]
        page_content = page.extract_text()
        documents.append(Document(page_content=page_content, metadata={'source': path, 'page': page_number}))
    return documents