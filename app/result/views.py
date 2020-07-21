from flask import Blueprint, render_template
from flask_user import current_user
from app.tab import get_allowed_tabs
from app.exam.models import Exam

result_blueprint = Blueprint("result", __name__)


@result_blueprint.route("/status")
def result():
    user = current_user.username
    # All exam for exam_level current user
    exam = Exam.query.all()
    tabs = get_allowed_tabs()
    return render_template("exam/status.html", tabs=tabs, user=user, exam=exam)
