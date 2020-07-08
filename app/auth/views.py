from flask import Blueprint, render_template, url_for, redirect, flash, request
from flask_login import login_user, logout_user, login_required
from flask_user import roles_required

from .models import User, Role, UserRoles
from .forms import LoginForm, RegistrationForm, UserEditForm, UNCHANGED_PASSWORD
from app.logger import log

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
            active=(form.active.data == "Active"),
            # role=form.role.data,
        )
        user.save()
        role = Role.query.filter(Role.name == form.role.data).first()
        if not role:
            flash("Wrong role name.", "danger")
            log(log.ERROR, "Bad DB! Wrong role name: %s", form.role.data)
            return redirect(url_for("dashboard.index"))
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


@auth_blueprint.route("/delete/<user_id>", methods=["GET"])
@roles_required("Admin")
def delete_user(user_id):
    user_id = int(user_id)
    user = User.query.filter(User.id == user_id).first()
    if user:
        user.delete()
    else:
        flash("Wrong user id", "danger")
    return redirect(url_for("dashboard.index"))


@auth_blueprint.route("/user_edit/<user_id>", methods=["GET", "POST"])
@roles_required("Admin")
def edit_user(user_id):
    user_id = int(user_id)
    user = User.query.filter(User.id == user_id).first()
    if user is None:
        flash("Wrong account id.", "danger")
        return redirect(url_for("dashboard.index"))
    user_role = UserRoles.query.filter(UserRoles.user_id == user_id).first()
    if not user_role:
        log(log.ERROR, "Bad DB! User %d was without role!", user_id)
        flash("User without role.", "danger")
        return redirect(url_for("dashboard.index"))
    role = Role.query.filter(Role.id == user_role.role_id).first()
    if not role:
        flash("Wrong user role id.", "danger")
        log(
            log.ERROR,
            "Bad DB! Wrong role id:%d for user: %d",
            user_role.role_id,
            user_id,
        )
        return redirect(url_for("dashboard.index"))

    form = UserEditForm(request.form)
    if form.validate_on_submit():
        user.username = form.username.data
        if UNCHANGED_PASSWORD != form.password.data:
            user.password = form.password.data
        user.role = form.role.data
        user.active = form.active.data == "Active"
        user.save()
        new_role = Role.query.filter(Role.name == form.role.data).first()
        if not new_role:
            flash("Wrong role name.", "danger")
            log(log.ERROR, "Bad DB! Wrong role name: %s", form.role.data)
            return redirect(url_for("dashboard.index"))
        if user_role.role_id != new_role.id:
            log(log.INFO, "User %d changed role to %d!", user_id, new_role.id)
            user_role.role_id = new_role.id
            user_role.save()
        return redirect(url_for("dashboard.index"))
    else:
        form.user_id.data = user_id
        form.username.data = user.username
        form.password.data = user.password
        form.role.data = user.roles[0].name
        form.active.data = "Active" if user.active else "Not Active"
        form.close_button = url_for("dashboard.index")
    return render_template("auth/user_edit.html", form=form)
