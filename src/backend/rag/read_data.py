from typing import List, Dict
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.docstore.document import Document


def load_pdf(path: str) -> List[Document]:
    """
    Carrega um documento PDF e o retorna como uma lista de objetos Document.

    Args:
        path (str): O caminho para o arquivo PDF.

    Returns:
        List[Document]: Uma lista contendo os documentos carregados.
    """

    loader = PyPDFLoader(path)
    return loader.load()

def read_txt_file(path: str) -> List[Document]:
    """
    Lê um arquivo de texto e retorna seu conteúdo como uma lista de objetos Document.

    Args:
        path (str): O caminho para o arquivo de texto.

    Returns:
        List[Document]: Uma lista contendo o documento lido.
    """

    with open(path, 'r', encoding='utf-8') as file:
        lines = file.read()
        document = [Document(lines)]
    return document

def read_csv_file(path: str) -> List[Document]:
    """
    Lê um arquivo CSV e retorna seu conteúdo como uma lista de objetos Document.

    Args:
        path (str): O caminho para o arquivo CSV.

    Returns:
        List[Document]: Uma lista contendo o documento lido.
    """
    
    with open(path, 'r') as file:
        data = file.read()
        document = [Document(data)]
    return document
