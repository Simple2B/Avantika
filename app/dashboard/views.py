from flask import Blueprint, render_template
from flask_user import roles_required
from app.tab import get_allowed_tabs
from app.auth.models import User
from app.exam.models import Exam

dashboard_blueprint = Blueprint("dashboard", __name__)


@dashboard_blueprint.route("/dashboard")
@roles_required("Admin")
def index():
    users = User.query.all()
    tabs = get_allowed_tabs()
    return render_template("dashboard/dashboard.html", tabs=tabs, users=users)


@dashboard_blueprint.route("/exam_dashboard")
@roles_required("Admin")
def list_of_exam():
    exams = Exam.query.all()
    tabs = get_allowed_tabs()
    return render_template("dashboard/exam_dashboard.html", tabs=tabs, exams=exams)
