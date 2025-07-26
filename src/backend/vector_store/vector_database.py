from typing import List
from .azure_vector_store import get_vector_store_azure, delete_index_from_vector_store_azure, add_documents_to_vector_store_with_retry_azure
from .aws_vector_store import get_vector_store_aws, delete_index_from_vector_store_aws, add_documents_to_vector_store_with_retry_aws
from langchain.docstore.document import Document
import logging 


class VectorDatabase:

    def __init__(self, provider='AZURE') -> None:
        """
        Inicializa a instância da classe VectorDatabase.

        Args:
            provider (str): O provedor de serviços de vetor. Pode ser 'AZURE' ou 'AWS'. O padrão é 'AZURE'.
        """
        self.provider = provider

    def get_vector_store(self, index_name: str):
        """
        Obtém a vector store com base no provedor especificado.

        Args:
            index_name (str): O nome do índice para o qual a vector store deve ser obtida.

        Returns:
            O objeto da vector store correspondente ao provedor.
        """

        if self.provider == "AZURE":
            vector_store = get_vector_store_azure(index_name)
        else:
            vector_store = get_vector_store_aws()

        return vector_store

    def get_relevant_documents(self, query:str, index_name:str, search_type: str)->List[Document]:
        """
        Obtém documentos relevantes com base na consulta fornecida.

        Args:
            query (str): A consulta para a pesquisa de similaridade.
            index_name (str): O nome do índice para o qual a pesquisa deve ser realizada.
            search_type (str): O tipo de pesquisa a ser utilizada.

        Returns:
            List[Document]: Uma lista de documentos relevantes.
        """

        vector_store = self.get_vector_store(index_name)
        docs = vector_store.similarity_search(query=query, k=3, search_type=search_type)

        return docs

    def add_documents_to_vector_store(self, index_name: str, documents: List[Document])->List[str]:
        """
        Adiciona documentos à vector store.

        Args:
            index_name (str): O nome do índice para o qual os documentos devem ser adicionados.
            documents (List[Document]): A lista de documentos a ser adicionada.

        Returns:
            List[str]: Uma lista de identificadores dos documentos adicionados.
        """

        vector_store = self.get_vector_store(index_name)
        resp = vector_store.add_documents(documents=documents)
        return resp

    def add_documents_to_vector_store_with_retry(self, index_name: str, documents: List[Document]) -> List[str]:
        """
        Adiciona documentos à vector store com tentativas de reenvio em caso de falha.

        Args:
            index_name (str): O nome do índice para o qual os documentos devem ser adicionados.
            documents (List[Document]): A lista de documentos a ser adicionada.

        Returns:
            List[str]: Uma lista de identificadores dos documentos adicionados.
        """

        vector_store = self.get_vector_store(index_name)
    
        if self.provider == "AZURE":
            add_documents_to_vector_store_with_retry_azure(vector_store, documents),
        
        else:
            add_documents_to_vector_store_with_retry_aws()
    
    def create_index_in_vector_store(self, index_name: str)->None:
        """
        Cria um índice na vector store. Se um índice já existir, ele será excluído antes de criar um novo.

        Args:
            index_name (str): O nome do índice a ser criado.
        """

        try:
            self.delete_index_from_vector_store(index_name)
            self.get_vector_store(index_name)
            logging.info("Creating new Indexes")
        except Exception as e:
            logging.info(e)
    
    def delete_index_from_vector_store(self, index_name: str):
        """
        Exclui um índice da vector store.

        Args:
            index_name (str): O nome do índice a ser excluído.
        """

        if self.provider == "AZURE":
            delete_index_from_vector_store_azure(index_name),
        
        else:
            delete_index_from_vector_store_aws()
