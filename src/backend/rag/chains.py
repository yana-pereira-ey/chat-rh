from src.backend.vector_store import VectorDatabase
from src.backend.llm.llm import LLM
from langchain.memory import ConversationBufferWindowMemory
from langchain.chains import ConversationChain
import re
from loguru import logger


def run_query_on_docs(query: str, history: ConversationBufferWindowMemory, index_name: str) -> tuple:
    """
    Executa uma consulta nos vetores obtidos a partir do AIDA, gera uma resposta estruturada e explica o pensamento por trás da resposta.

    Args:
        query (str): A pergunta feita pelo usuário.
        history (ConversationBufferWindowMemory): O histórico da conversa para manter o contexto.
        index_name (str): O nome do índice onde os documentos serão buscados.

    Returns:
        tuple: Um tupla contendo a resposta e o pensamento por trás da resposta.
    """

    vector_db = VectorDatabase(provider="AZURE")
    docs = vector_db.get_relevant_documents(query, index_name, search_type="hybrid")

    logger.info(f"{len(docs)} Documents Retrieved")

    context = ' '.join([doc.page_content for doc in docs])

    prompt_string = (
        f"""
        Você é um agente de inteligência artificial com o nome de Judite, e capacitado para atuar nos setores de Talent e Recursos Humanos. 
        Seus conhecimentos específicos sobre o assunto estão no contexto abaixo entre ***.
        Você trabalha na EY, também chamada de Ernst & Young.
        O usuário também trabalha na EY e irá te fazer uma pergunta. 
        Seu objetivo é ler essa pergunta, explicar seu pensamento e retornar uma resposta clara e abrangente para o usuário.  
        Caso sejam necessárias informações adicionais, pergunte ao usuário. 
        Caso você não saiba a resposta, não invente, apenas diga que não sabe. 
        Responda apenas com informações obtidas através do contexto.
        Para explicar o pensamento de forma clara, detalhe o processo de raciocínio lógico seguido para conectar a pergunta com as informações no contexto.
        A sua resposta precisa ter sempre duas seções, PENSAMENTO e RESPOSTA, e deve ser sempre apresentada exclusivamente no seguinte formato:

        "
        ###PENSAMENTO###


        ###RESPOSTA###
        "

        Traga as respostas sempre no formato demonstrado acima, com PENSAMENTO e RESPOSTA sinalizados por ###.        
        Instruções específicas para as perguntas do usuário:
        - Se a pergunta contiver "quem", forneça informações sobre a(s) pessoa(s) envolvida(s).
        - Se a pergunta contiver "quais", liste os itens relevantes mencionados no contexto.
        - Se a pergunta contiver "quanto", enumere os resultados e forneça números ou quantidades específicas. Nesse caso, deixe para explicar mais no pensamento e seja econômico na resposta.
        - Lembre-se sempre de filtrar as informações de acordo com o que o usuário informou.
        - Utilize linguagem característica do setor de talent/recursos humanos.

        A pergunta feita pelo usuário é: {query}

        ***CONTEXTO: {context}***
        """
    )

    models = LLM()
    llm = models.create_chat_llm()
    
    conversation = ConversationChain(llm=llm, verbose=True, memory=history)

    response = conversation.invoke(prompt_string)

    response_text = response['response'].replace('"', '').replace('\n', '')

    match = re.search(r'###PENSAMENTO###(.*?)###RESPOSTA###(.*)', response_text, re.DOTALL)
    
    if match:
        pensamento = match.group(1).strip()
        resposta = match.group(2).strip()
    else:
        pensamento = "Erro: Não foi possível extrair o pensamento da resposta."
        resposta = "Erro: A resposta não contém os delimitadores esperados."

    return (resposta, pensamento)
