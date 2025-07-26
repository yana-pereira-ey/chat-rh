import os
import json
import pandas as pd
from typing import List 


class folders:

    APP_DIR = os.path.abspath(os.path.dirname('src/'))
    FRONTEND = os.path.join(APP_DIR, 'frontend')
    STATIC = os.path.join(FRONTEND, 'static')
    TEMPLATES = os.path.join(FRONTEND, 'templates')


def convert_to_dataframe(data):
    """
    Converte os dados em uma estrutura tabular (DataFrame) a partir de diferentes formatos de entrada.

    Dependendo do tipo de dado fornecido, a função trata de duas formas principais:
    1. **String**: Se os dados forem uma string, espera-se que ela esteja em um formato tabular com linhas separadas por quebras de linha e colunas separadas por tabulação (ou outro delimitador especificado).
    2. **Lista de Linhas**: Se os dados forem uma lista de objetos do tipo `Row`, extrai os valores e utiliza as chaves do primeiro `Row` como nomes das colunas.

    Args:
        data (Union[str, List[Row]]): Dados a serem convertidos para um DataFrame. Pode ser uma string em formato tabular ou uma lista de objetos do tipo `Row`.

    Returns:
        pd.DataFrame: Um DataFrame pandas contendo os dados fornecidos.

    Raises:
        ValueError: Se o tipo de dado fornecido não for suportado (deve ser uma string ou uma lista de `Row`).
    """

    if isinstance(data, str):
        # If data is a string, split it into lines (assuming tabular format)
        lines = data.strip().split('\n')
        # Split the first line to get column names
        column_names = lines[0].split('\t')
        # Split each subsequent line by a delimiter (e.g., tab, comma, etc.)
        rows = [line.split('\t') for line in lines[1:]]
    elif isinstance(data, list):
        # If data is a List[Row], extract the values from each Row
        rows = [list(row) for row in data]
        # Assume column names are the keys of the first Row
        column_names = list(data[0].asDict().keys())
    else:
        raise ValueError("Unsupported data type. Expected List[Row] or str.")

    # Create a DataFrame from the rows
    df = pd.DataFrame(rows, columns=column_names)
    return df


def save_last_queries_and_responses(id: str, last_queries: List[str], last_resp: List[str]) -> None:
    """
    Salva as últimas consultas e respostas em um arquivo JSON.

    Args:
        id (str): String aleatória de uma conversa.
        last_queries (List[str]): Lista das últimas consultas feitas.
        last_resp (List[str]): Lista das últimas respostas correspondentes.

    Returns:
        None
    """

    qa_dict = {q: r for q, r in zip(last_queries, last_resp)}

    os.makedirs('files', exist_ok=True)

    file_name = f"files/{id}_conversation.json"

    with open(file_name, 'w', encoding='utf8') as f:
        json.dump(qa_dict, f, ensure_ascii=False, indent=4)


def save_messages_from_session(session) -> None:
    """
    Salva as últimas consultas e respostas em um arquivo JSON.

    Args:
        session (session): objeto Flask session contendo user_id,
        mensagens do assistente e do usuário 

    Returns:
        None
    """

    user_token = session['user_id']
    user_messages = session['messages']["user"]
    assistant_messages = session['messages']["ai"]

    qa_dict = {q: r for q, r in zip(user_messages, assistant_messages)}

    os.makedirs('files', exist_ok=True)

    file_name = f"files/{user_token}_conversation.json"

    with open(file_name, 'w', encoding='utf8') as f:
        json.dump(qa_dict, f, ensure_ascii=False, indent=4)
