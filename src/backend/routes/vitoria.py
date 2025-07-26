import os
from flask import Blueprint, request, jsonify, render_template, session, redirect, url_for
from src.backend.rag.chains import run_query_on_docs
from src.backend.utils.utils import folders, save_messages_from_session
from dotenv import load_dotenv
from loguru import logger

load_dotenv()


bp = Blueprint("vitoria_agent", __name__, template_folder=folders.TEMPLATES,
                static_folder=folders.STATIC)


INDEX = os.getenv("INDEX")


@bp.route('/chatAgente1', methods=['GET'])
def show_chat_vitoria():
    """
    Exibe a página de chat com a Vitória.

    Método HTTP:
        GET

    Respostas:
        200: Retorna a página de chat se o usuário estiver autenticado.
        302: Redireciona para a página de logout se o usuário não estiver autenticado.
    """

    user = session.get('user_id')

    if not user:
        return redirect(url_for("auth.logout"))
    
    return render_template('chat/vitoria.html')


@bp.route('/chatAgente1/query', methods=['POST'])
def query_vitoria():
    """
    Envia uma consulta para a agente do chatbot Vitória e retorna a resposta.

    Método HTTP:
        POST

    Dados de entrada:
        JSON contendo 'query'.

    Respostas:
        200: Retorna a resposta do chatbot e o pensamento do agente.
        400: Requisição inválida (dados faltando ou usuário não autenticado).
        500: Erro interno do servidor.
    """

    try:
        # Extract the query from the request
        data = request.json
        query = data.get('query')

        if not query:
            return jsonify({'error': 'Query is required'}), 400
        
        user = session.get('user_id')

        if not user:
            return jsonify({'error': 'User ID is required'}), 400

        # Run the query using run_query_on_docs
        resp, pensamento = run_query_on_docs(query, history=session['history'], index_name=INDEX)

        session['messages']["user"].append(query)
        session['messages']["ai"].append(resp)

        # save_messages_from_session(session=session)

        # Return the response as JSON
        return jsonify({'response': resp, 'thought': pensamento})
    except Exception as e:
        logger.error(f"chatAgente1: An error occurred: {e}")
        return jsonify({'error': str(e)}), 500

