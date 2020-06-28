from flask import render_template, Blueprint

from app.tab import get_allowed_tabs

main_blueprint = Blueprint("main", __name__)


@main_blueprint.route("/")
def index():
    tabs = get_allowed_tabs()
    return render_template("index.html", tabs=tabs)
