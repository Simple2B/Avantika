from flask import Blueprint, render_template
from flask_user import roles_required
from app.tab import get_allowed_tabs

dashboard_blueprint = Blueprint("dashboard", __name__)


@dashboard_blueprint.route("/dashboard")
@roles_required("Admin")
def index():
    tabs = get_allowed_tabs()
    return render_template("dashboard/dashboard.html", tabs=tabs)
