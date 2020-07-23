from flask import Blueprint, render_template
from flask_user import current_user
from app.tab import get_allowed_tabs
from app.result.models import Result
from app.exam.models import Exam

result_blueprint = Blueprint("result", __name__)


@result_blueprint.route("/status")
def result():
    # For output user name in the site's form
    user = current_user.username
    user_id_results = Result.query.filter(Result.user_id == current_user.id).all()
    exam_name = Exam.query.filter(Result.exam_id == Exam.id).all()
    tabs = get_allowed_tabs()
    return render_template(
        "exam/status.html",
        tabs=tabs,
        user=user,
        user_id_results=user_id_results,
        exam_name=exam_name,
    )
