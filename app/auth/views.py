from flask import Blueprint, render_template, url_for, redirect, flash, request
from flask_login import login_user, logout_user, login_required
from flask_user import roles_required

from .models import User, Role, UserRoles
from .forms import LoginForm, RegistrationForm

auth_blueprint = Blueprint("auth", __name__)


@auth_blueprint.route("/register", methods=["GET", "POST"])
@roles_required("Admin")
def register():
    form = RegistrationForm(request.form)
    if form.validate_on_submit():
        user = User(
            # We need username, password, role
            username=form.username.data,
            password=form.password.data,
            active=form.active.data,
            # role=form.role.data,
        )
        user.save()
        role = Role.query.filter(Role.name == form.role.data).first()
        if not role:
            role = Role(name=form.role.data)
            role.save()
        user_to_role = UserRoles(user_id=user.id, role_id=role.id)
        user_to_role.save()
        flash("Registration successful. You are logged in.", "success")
        return redirect(url_for("dashboard.index"))
    elif form.is_submitted():
        flash("The given data was invalid.", "danger")
    return render_template("auth/register.html", form=form)


@auth_blueprint.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm(request.form)
    if form.validate_on_submit():
        user = User.authenticate(form.user_id.data, form.password.data)
        if user is not None:
            login_user(user)
            flash("Login successful.", "success")
            return redirect(url_for("main.index"))
        flash("Wrong user ID or password.", "danger")
    return render_template("auth/login.html", form=form)


@auth_blueprint.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You were logged out.", "info")
    return redirect(url_for("main.index"))
