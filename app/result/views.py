from flask import Blueprint, render_template
from flask_user import current_user
from app.tab import get_allowed_tabs
from app.result.models import Result

result_blueprint = Blueprint("result", __name__)


@result_blueprint.route("/status")
def result():
    results = Result.query.filter(Result.user_id == current_user.id).all()
    tabs = get_allowed_tabs()
    return render_template("exam/status.html", tabs=tabs, results=results)
