import os
from .azure_llm import create_azure_chat_llm, create_azure_embeddings_llm
from .aws_llm import create_aws_chat_llm, create_aws_embeddings_llm


class LLM:
    """
    Classe para criar modelos de linguagem de chat e embeddings.

    Args:
        provider (str, opcional): O provedor de serviço para o LLM ('AZURE' ou 'AWS'). O padrão é 'AZURE'.

    Métodos:
        create_chat_llm(): Cria um modelo de linguagem de chat baseado no provedor especificado.
        create_embeddings_llm(): Cria um modelo de embeddings baseado no provedor especificado.
    """

    def __init__(self, provider='AZURE') -> None:
        """
        Inicializa a classe LLM com o provedor especificado.

        Args:
            provider (str, opcional): O provedor de serviço para o LLM ('AZURE' ou 'AWS'). O padrão é 'AZURE'.
        """

        self.provider = provider

    def create_chat_llm(self):
        """
        Cria um modelo de linguagem de chat baseado no provedor especificado.

        Returns:
            callable: Um modelo de linguagem de chat.
        """

        llms = {
            'AZURE': create_azure_chat_llm(),
            'AWS': create_aws_chat_llm()
            }

        return llms[self.provider]

    def create_embeddings_llm(self):
        """
        Cria um modelo de embeddings baseado no provedor especificado.

        Returns:
            callable: Um modelo de embeddings.
        """

        embeddings = {
            'AZURE': create_azure_embeddings_llm(),
            'AWS': create_aws_embeddings_llm()
            }

        return embeddings[self.provider]
