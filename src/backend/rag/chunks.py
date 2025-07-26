from langchain.text_splitter import TokenTextSplitter, RecursiveCharacterTextSplitter
from typing import List, Union
from langchain.docstore.document import Document


def create_chunks(documents: List[Document], chunk_method, chunk_size=500, chunk_overlap=100) -> Union[str, List[Document]]:
    """
    Cria chunks de documentos usando o método especificado pelo desenvolvedor.

    Args:
        documents (List[Document]): A lista de documentos a serem fragmentados.
        chunk_method (str): O método de fragmentação a ser usado ('token' ou 'recursive').
        chunk_size (int, opcional): O tamanho de cada fragmento em caracteres ou tokens. O padrão é 500.
        chunk_overlap (int, opcional): O número de caracteres ou tokens que cada fragmento deve sobrepor com o próximo. O padrão é 100.

    Returns:
        Union[str, List[Document]]: Uma lista de documentos fragmentados ou uma string de erro se o método de fragmentação for inválido.
    """

    if chunk_method == 'token':
      text_splitter = TokenTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
      )  
    elif chunk_method == 'recursive':
      text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
      )
    else:
      return "Invalid chunk model"

    chunks = text_splitter.split_documents(documents)
    return chunks


