import sys 
import os

module_path = os.path.abspath(os.path.join('../../../'))

if module_path not in sys.path:
    sys.path.append(module_path)

from src.backend.vector_store import VectorDatabase
from src.backend.rag.chunks import create_chunks
# from src.backend.storage.process_docs import load_pdf, read_txt_file, read_csv_file
from src.backend.rag.read_data import load_pdf, read_txt_file, read_csv_file
# from src.backend.utils.utils import convert_to_dataframe
from langchain_community.docstore.document import Document
from dotenv import load_dotenv
from loguru import logger

load_dotenv()

"""Aplicacao para fazer upload de documentos, chunks, e vector Storage 
   uso: python main_rag.py
"""

INDEX = os.getenv("INDEX")
local_folder_path = "docs_for_embeddings"


def rag():
    """
    Processa dados para o sistema RAG (Retrieval-Augmented Generation).

    1. Obtém dados da fonte.
    2. Converte os dados em um DataFrame.
    3. Converte cada linha do DataFrame em JSON e cria documentos.
    4. Divide os documentos em chunks.
    5. Cria um índice no banco de dados vetorial, se não existir.
    6. Adiciona os documentos ao banco de dados vetorial.

    Operações principais:
    - **Obtenção de dados**: Obtém dados de uma fonte externa usando a função `get_dados_entregas()`.
    - **Conversão e preparação**: Converte dados para JSON e cria instâncias de `Document`.
    - **Chunking**: Divide documentos em chunks para armazenamento eficiente.
    - **Armazenamento vetorial**: Cria e adiciona chunks ao banco de dados vetorial.

    Logs:
    - Registra o início e a conclusão das operações de obtenção de dados, chunking e armazenamento.
    - Captura e registra erros durante a criação de índices e a adição de documentos.
    """
    vector_db = VectorDatabase(provider="AZURE")
    
    try:
        vector_db.create_index_in_vector_store(INDEX)
        logger.info("Creating new Indexes")
    except Exception as e:
        logger.error(f"create_index_in_vector_store: {e}")


    logger.info("Getting data...")
    for file_name in os.listdir(local_folder_path):
        if file_name.lower().endswith('.pdf'):
            pdf_file_path = os.path.join(local_folder_path, file_name)
            data = load_pdf(pdf_file_path)
            chunks = create_chunks(data, chunk_method="token", chunk_size=500, chunk_overlap=100)
            logger.info("Chunking .pdf")
        elif file_name.lower().endswith('.txt'):
            txt_file_path = os.path.join(local_folder_path, file_name)
            data = read_txt_file(txt_file_path)
            chunks = create_chunks(data, chunk_method="token", chunk_size=500, chunk_overlap=100)
            logger.info("Chunking .txt")
        elif file_name.lower().endswith('.csv'):
            csv_file_path = os.path.join(local_folder_path, file_name)
            data = read_csv_file(csv_file_path)
            chunks = create_chunks(data, chunk_method="token", chunk_size=500, chunk_overlap=100)
            logger.info("Chunking .csv")
            
        try:
            vector_db.add_documents_to_vector_store_with_retry(INDEX, chunks)  
            logger.info("Adding documents to the vector store")
        except Exception as e:
            logger.error(f"add_documents_to_vector_store_with_retry: {e}")

if __name__=="__main__":
    rag()

    
