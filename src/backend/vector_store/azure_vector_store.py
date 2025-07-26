from dotenv import load_dotenv
import os
import time
from typing import List
from src.backend.llm import create_azure_embeddings_llm
from langchain.docstore.document import Document
from langchain_community.vectorstores.azuresearch import AzureSearch
from azure.search.documents.indexes import SearchIndexClient
from azure.core.credentials import AzureKeyCredential
from azure.search.documents.indexes.models import (
  SearchableField,
  SearchField,
  SearchFieldDataType,
  SimpleField,
)
from collections.abc import MutableMapping
from loguru import logger 

load_dotenv()

vector_store_address: str = os.getenv("AZURE_SEARCH_ENDPOINT")
vector_store_password: str = os.getenv("AZURE_SEARCH_ADMIN_KEY")


def get_relevant_documents_azure(query:str, index_name:str, search_type: str)->List[Document]:
    """
    Recupera documentos relevantes do Azure Search com base em uma consulta.

    Este método usa o serviço Azure Search para buscar documentos que são semelhantes à consulta fornecida.
    O tipo de busca pode ser configurado para diferentes perfis de pesquisa, como "similarity", "hybrid" ou "semantic_hybrid".

    Args:
        query (str): A consulta de busca para encontrar documentos relevantes.
        index_name (str): O nome do índice no Azure Search onde a busca será realizada.
        search_type (str): O tipo de pesquisa a ser realizada ("similarity", "hybrid" ou "semantic_hybrid").

    Returns:
        List[Document]: Uma lista de documentos relevantes que correspondem à consulta.
    """

    vector_store = get_vector_store_azure(index_name)
    docs = vector_store.similarity_search(query=query, k=5, search_type=search_type)

    return docs


def get_vector_store_azure(index_name: str)->AzureSearch:
    """
    Cria e retorna uma instância do cliente AzureSearch para interagir com o serviço Azure Search.

    Args:
        index_name (str): O nome do índice a ser usado no Azure Search.

    Returns:
        AzureSearch: Uma instância da classe AzureSearch configurada com o índice fornecido.
    """

    embedding_function = create_azure_embeddings_llm()
    fields = get_fields()
    vector_store = AzureSearch(
       azure_search_endpoint=vector_store_address,
       azure_search_key=vector_store_password,
       index_name=index_name,
       embedding_function=embedding_function,
       fields=fields,
    )
    return vector_store


def add_documents_to_vector_store_with_retry_azure(vector_store: AzureSearch, documents: List[Document]) -> List[str]:
    """
    Adiciona documentos ao vector store com tentativa de reenvio em caso de erro.

    Adiciona documentos ao índice do Azure Search em lotes, lidando com limites de taxa e outros erros. 
    Se ocorrer um erro de limite de taxa (código 429), a função espera um tempo e tenta novamente. 
    Em caso de outros erros, eles são registrados e a função tenta adicionar os documentos restantes.

    Args:
        vector_store (AzureSearch): A instância do cliente AzureSearch usada para adicionar documentos.
        documents (List[Document]): A lista de documentos a serem adicionados.

    Returns:
        List[str]: Uma lista de IDs dos documentos que foram adicionados com sucesso.
    """

    added_document_ids = []
    batch_size = 10  # Adjust the batch size according to your rate limit
    retry_after = 30  # Default retry after 30 seconds
 
    for i in range(0, len(documents), batch_size):
        batch = documents[i:i + batch_size]
        try:
            resp = vector_store.add_documents(documents=batch)
            added_document_ids.extend(resp)
            logger.info(f"Added documents {i} to {i + batch_size}")
        except Exception as e:
            # Check if the error is a rate limit error (429)
            if e.code == 429:
                retry_after = e.retryAfter if hasattr(e, 'retryAfter') else retry_after
                logger.info(f"Rate limit hit. Retrying after {retry_after} seconds.")
            else:
                logger.error(f"add_documents_to_vector_store_with_retry_azure - An error occurred: {e}")
            time.sleep(retry_after)
            # Retry the same batch after waiting
            continue
 
        # Delay between successful batches to avoid hitting the rate limit
        time.sleep(1)
 
    return added_document_ids


def delete_index_from_vector_store_azure(index_name: str)->None:
    """
    Remove um índice da vector store.

    Verifica se o índice com o nome especificado existe no Azure Search e, se existir, 
    remove-o. Se o índice não existir, a função não realiza nenhuma ação.

    Args:
        index_name (str): O nome do índice a ser removido.

    Returns:
        None
    """

    client = SearchIndexClient(vector_store_address, AzureKeyCredential(vector_store_password))
    indices = client.list_indexes()
    index_exists = any(index.name == index_name for index in indices)
    if index_exists:
      client.delete_index(index_name)

  
def is_indexing_completed(index_name: str)->MutableMapping[str, any]:
    """
    Verifica se a indexação de documentos foi concluída no Azure Search.

    Obtém as estatísticas do índice especificado e verifica se a contagem de documentos
    é maior que zero, indicando que a indexação foi concluída.

    Args:
        index_name (str): O nome do índice para verificar a indexação.

    Returns:
        MutableMapping[str, any]: Um dicionário contendo as estatísticas do índice.
        A função retorna True se a contagem de documentos for maior que zero, indicando
        que a indexação foi concluída; caso contrário, retorna False.
    """

    client = SearchIndexClient(vector_store_address, AzureKeyCredential(vector_store_password))
    index_statistics = client.get_index_statistics(index_name)
    return index_statistics["document_count"] > 0


def get_fields():
    """
    Retorna a definição dos campos para um índice no Azure Search.

    Cria e configura uma lista de campos com os seguintes tipos e propriedades:
    - `id`: Campo chave e filtrável do tipo String.
    - `content`: Campo pesquisável do tipo String.
    - `content_vector`: Campo pesquisável com vetores, usado para busca vetorial com dimensões especificadas e um perfil de busca.
    - `metadata`: Campo pesquisável do tipo String.
    - `source`: Campo filtrável do tipo String, usado para filtrar pela origem do documento.

    Returns:
        List[SearchField]: Lista de objetos `SearchField` configurados para o índice.
    """
    
    fields = [
      SimpleField(
          name="id",
          type=SearchFieldDataType.String,
          key=True,
          filterable=True,
      ),
      SearchableField(
          name="content",
          type=SearchFieldDataType.String,
          searchable=True,
      ),
      SearchField(
          name="content_vector",
          type=SearchFieldDataType.Collection(SearchFieldDataType.Single),
          searchable=True,
          vector_search_dimensions=1536,
          vector_search_profile_name="myHnswProfile",
      ),
      SearchableField(
          name="metadata",
          type=SearchFieldDataType.String,
          searchable=True,
      ),
      # Additional field for filtering on document source
      SimpleField(
          name="source",
          type=SearchFieldDataType.String,
          filterable=True,
      ),
    ]

    return fields