#!/user/bin/env python
import json
import click

from app import create_app, db, models, forms
from app.auth.models import User, Role, UserRoles
from app.exam.models import Exam

app = create_app()


# flask cli context setup
@app.shell_context_processor
def get_context():
    """Objects exposed here will be automatically available from the shell."""
    return dict(app=app, db=db, models=models, forms=forms)


def load_exams():
    with open("exams.json", "r") as f:
        for exam in json.load(f):
            if not Exam.query.filter(Exam.name == exam["name"]).first():
                Exam(name=exam["name"]).from_dict(**exam).save()


@app.cli.command()
def create_db():
    """Create the configured database."""
    db.create_all()
    create_user("admin", "admin", "Admin")
    create_user("admin2", "admin", "Admin")
    create_user("admin3", "admin", "Admin")
    create_user("student_PB_reg", "student", "Student_PB_reg")
    create_user("student_PB_prem", "student", "Student_PB_prem")
    create_user("student_PB_prem_outsider", "student", "Student_PB_prem_outsider")
    create_user("student_PI_reg", "student", "Student_PI_reg")
    create_user("student_PI_prem", "student", "Student_PI_prem")
    create_user("student_PI_prem_outsider", "student", "Student_PI_prem_outsider")
    create_user("student_PA_reg", "student", "Student_PA_reg")
    create_user("student_PA_prem", "student", "Student_PA_prem")
    create_user("student_PA_prem_outsider", "student", "Student_PA_prem_outsider")
    create_user("student_J_reg", "student", "Student_J_reg")
    create_user("student_J_pre", "student", "Student_J_pre")
    create_user("student_J_pre_outsider", "student", "Student_J_pre_outsider")
    create_user("student_HTML_reg", "student", "Student_HTML_reg")
    create_user("student_HTML_prem", "student", "Student_HTML_prem")
    create_user("student_HTML_prem_outsider", "student", "Student_HTML_prem_outsider")
    load_exams()


def create_user(username, password, role_name):
    user = User.query.filter(User.username == username).first()
    if user:
        return
    user = User(username=username)
    user.password = password
    user.save()
    user_role = Role.query.filter(Role.name == role_name).first()
    if not user_role:
        user_role = Role(name=role_name)
        user_role.save()
    join_user_to_role = UserRoles(user_id=user.id, role_id=user_role.id)
    join_user_to_role.save()


@app.cli.command()
@click.confirmation_option(prompt="Drop all database tables?")
def drop_db():
    """Drop the current database."""
    db.drop_all()


if __name__ == "__main__":
    app.run()
