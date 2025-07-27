import os
import uuid
from flask import Blueprint, request, render_template, make_response, redirect, url_for, session
import identity.web
from dotenv import load_dotenv
from langchain.memory import ConversationBufferWindowMemory
from src.backend.utils.utils import folders


load_dotenv()

bp = Blueprint("auth", __name__, template_folder=folders.TEMPLATES,
                static_folder=folders.STATIC)

AUTHORITY = os.getenv("AUTHORITY")
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")

print("CLIENT_ID:", CLIENT_ID)
print("CLIENT_SECRET:", CLIENT_SECRET)
print("AUTHORITY:", AUTHORITY)

assert CLIENT_ID is not None, "❌ CLIENT_ID não está definido!"
assert CLIENT_SECRET is not None, "❌ CLIENT_SECRET não está definido!"
assert AUTHORITY is not None, "❌ AUTHORITY não está definido!"


auth = identity.web.Auth(
    session=session,
    authority=AUTHORITY,
    client_id=CLIENT_ID,
    client_credential=CLIENT_SECRET,
)

@bp.route("/login")
def login():
    return render_template("auth/login_sso.html", **auth.log_in(
        scopes=["User.Read"],
        redirect_uri=url_for("auth.auth_response", _external=True),
        prompt="select_account",
        ))


@bp.route("/getAToken")
def auth_response():
    
    result = auth.complete_log_in(request.args)
    
    if "error" in result:
        return make_response(result.get("error"))
    
    user_id = session.get('user_id')

    if not user_id:
        session['user_id'] = str(uuid.uuid4())
        session['messages'] = {
            "ai": [],
            "user": []
        }
        session['history'] = ConversationBufferWindowMemory(return_messages=True, k=1)

    return redirect(url_for("home.show_chat"))


@bp.route("/logout")
def logout():

    user_id = session.get('user_id')

    if user_id:
        session.pop(user_id, None)
        session.pop('history')
        session.pop('messages')
    
    session.clear()

    return redirect(auth.log_out(url_for("auth.login", _external=True)))
