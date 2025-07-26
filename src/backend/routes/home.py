from flask import Blueprint, render_template, redirect, url_for, session
from dotenv import load_dotenv
from src.backend.utils.utils import folders

load_dotenv()

bp = Blueprint("home", __name__, template_folder=folders.TEMPLATES,
                static_folder=folders.STATIC)

@bp.route("/")
def index():

    user_id = session.get('user_id')

    if user_id:
        return redirect(url_for("home.show_chat")) 
    else:
        return redirect(url_for("auth.login"))


@bp.route('/chat', methods=['GET'])
def show_chat():
    return render_template('select/index.html')