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
    exams = (
        Exam.query.filter(Exam.deleted == False)  # noqa E712
        .filter(Exam.lang == Exam.Language.py)
        .order_by(Exam.id.desc())
        .all()
    )
    tabs = get_allowed_tabs()
    return render_template("dashboard/exam_dashboard.html", tabs=tabs, exams=exams)


@dashboard_blueprint.route("/exam_dashboard_java")
@roles_required("Admin")
def list_of_exam_java():
    exams = (
        Exam.query.filter(Exam.deleted == False)  # noqa E712
        .filter(Exam.lang == Exam.Language.java)
        .order_by(Exam.id.desc())
        .all()
    )
    tabs = get_allowed_tabs()
    return render_template("dashboard/exam_dashboard_java.html", tabs=tabs, exams=exams)


@dashboard_blueprint.route("/exam_dashboard_html")
@roles_required("Admin")
def list_of_exam_html():
    exams = (
        Exam.query.filter(Exam.deleted == False)  # noqa E712
        .filter(Exam.lang == Exam.Language.html)
        .all()
    )
    tabs = get_allowed_tabs()
    return render_template("dashboard/exam_dashboard_html.html", tabs=tabs, exams=exams)
