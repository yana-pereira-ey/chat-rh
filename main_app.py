import os
from datetime import timedelta
from werkzeug.middleware.proxy_fix import ProxyFix
from flask import Flask, session
from flask_session import Session
from src.backend.utils.utils import folders
from src.backend.routes import auth, home, health, vitoria, datalia
from dotenv import load_dotenv

load_dotenv()


def create_app():
    """
    Cria e configura uma instância dos ChatBots dos agentes.

    Este método configura o aplicativo Flask com as seguintes características:
    - Define a chave secreta para sessões.
    - Habilita o uso de HTTPS.
    - Configura a sessão para ser armazenada no sistema de arquivos e define o tempo de expiração da sessão.
    - Registra blueprints para as diferentes partes do aplicativo, incluindo autenticação, verificação de integridade, e direcionamento para os agentes.

    Returns:
        Flask: A instância do aplicativo Flask configurada.
    """

    app = Flask(__name__, template_folder=folders.TEMPLATES,
                static_folder=folders.STATIC)
    
    app.secret_key = os.getenv("FLASK_SECRET_KEY")
    
    # Enable https
    app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

    # Set up the session interface
    app.config["SESSION_TYPE"] = "filesystem"
    app.config["SESSION_FILE_DIR"] = "flask_session"  
    app.config["SESSION_PERMANENT"] = False
    app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=10)

    Session(app)
    
    # register blueprints
    app.register_blueprint(auth.bp)
    app.register_blueprint(home.bp)
    app.register_blueprint(health.bp)
    app.register_blueprint(vitoria.bp)
    app.register_blueprint(datalia.bp)
    
    return app

app = create_app()

if __name__ == "__main__":
    app.run()