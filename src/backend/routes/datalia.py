from flask import Blueprint
from src.backend.utils.utils import folders


bp = Blueprint("datalia_agent", __name__, template_folder=folders.TEMPLATES,
                static_folder=folders.STATIC)


@bp.route('/agente2')
def datalia():
    return "Você escolheu Agente 2!"

