from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required, current_user

from app.tab import get_allowed_tabs

dashboard_blueprint = Blueprint("dashboard", __name__)


@dashboard_blueprint.route("/dashboard")
@login_required
def index():
    if "Admin" not in [role.name for role in current_user.roles]:
        return redirect(url_for("main.index"))
    tabs = get_allowed_tabs()
    return render_template("dashboard/dashboard.html", tabs=tabs)
