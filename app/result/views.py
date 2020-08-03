from flask import Blueprint, render_template
from flask_user import current_user, roles_required
from app.tab import get_allowed_tabs
from app.result.models import Result
from app.auth.models import User

result_blueprint = Blueprint("result", __name__)


@result_blueprint.route("/status")
def result():
    user = User.query.filter(User.id == current_user.id).first()
    results = Result.query.filter(Result.user_id == current_user.id).all()
    tabs = get_allowed_tabs()
    return render_template("exam/status.html", tabs=tabs, results=results, user=user)


@result_blueprint.route("/status_for_admin/<user_id>")
@roles_required("Admin")
def result_for_admin(user_id):
    user_id = int(user_id)
    user = User.query.filter(User.id == user_id).first()
    results = Result.query.filter(Result.user_id == user_id).all()
    tabs = get_allowed_tabs()
    return render_template(
        "exam/status_for_admin.html", tabs=tabs, results=results, user=user
    )
