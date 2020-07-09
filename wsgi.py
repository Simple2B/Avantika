#!/user/bin/env python
import json
import click

from app import create_app, db, models, forms
from app.auth.models import User, Role, UserRoles
from app.exam.models import Exam, ExamType, RoleExamType

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
    # create all roles
    create_role("Admin")
    create_role("Student_PB_reg")
    create_role("Student_PB_prem")
    create_role("Student_PB_prem_outsider")
    create_role("Student_PI_reg")
    create_role("Student_PI_prem")
    create_role("Student_PI_prem_outsider")
    create_role("Student_PA_reg")
    create_role("Student_PA_prem")
    create_role("Student_PA_prem_outsider")
    create_role("Student_J_reg")
    create_role("Student_J_pre")
    create_role("Student_J_pre_outsider")
    create_role("Student_HTML_reg")
    create_role("Student_HTML_prem")
    create_role("Student_HTML_prem_outsider")
    # create all exam types
    create_exam_type("Python Basics reg")
    create_exam_type("Python Basics prem")
    create_exam_type("Python Inter")
    create_exam_type("Python Inter Prem")
    create_exam_type("Python adv")
    create_exam_type("Python adv prem")
    create_exam_type("Java Basics reg")
    create_exam_type("Java Basics prem")
    create_exam_type("HTML, CSS, JS reg")
    create_exam_type("HTML, CSS, JS prem")
    # create all connection exam_type with role
    # Python Basics reg
    create_exam_type("Python Basics reg", "Admin")
    create_exam_type("Python Basics reg", "Student_PB_reg")
    create_exam_type("Python Basics reg", "Student_PB_prem")
    create_exam_type("Python Basics reg", "Student_PI_reg")
    create_exam_type("Python Basics reg", "Student_PI_prem")
    create_exam_type("Python Basics reg", "Student_PA_reg")
    create_exam_type("Python Basics reg", "Student_PA_prem")
    # Python Basics prem
    create_exam_type("Python Basics prem", "Admin")
    create_exam_type("Python Basics prem", "Student_PB_prem")
    create_exam_type("Python Basics prem", "Student_PB_prem_outsider")
    create_exam_type("Python Basics prem", "Student_PI_prem")
    create_exam_type("Python Basics prem", "Student_PI_prem_outsider")
    create_exam_type("Python Basics prem", "Student_PA_prem")
    create_exam_type("Python Basics prem", "Student_PA_prem_outsider")
    # Python Inter
    create_exam_type("Python Inter", "Admin")
    create_exam_type("Python Inter", "Student_PI_reg")
    create_exam_type("Python Inter", "Student_PI_prem")
    create_exam_type("Python Inter", "Student_PA_reg")
    create_exam_type("Python Inter", "Student_PA_prem")
    # Python Inter Prem
    create_exam_type("Python Inter Prem", "Admin")
    create_exam_type("Python Inter Prem", "Student_PI_prem")
    create_exam_type("Python Inter Prem", "Student_PI_prem_outsider")
    create_exam_type("Python Inter Prem", "Student_PA_prem")
    create_exam_type("Python Inter Prem", "Student_PA_prem_outsider")
    # Python adv
    create_exam_type("Python adv", "Admin")
    create_exam_type("Python adv", "Student_PA_reg")
    create_exam_type("Python adv", "Student_PA_prem")
    # Python adv prem
    create_exam_type("Python adv prem", "Admin")
    create_exam_type("Python adv prem", "Student_PA_prem")
    create_exam_type("Python adv prem", "Student_PA_prem_outsider")
    # Java Basics reg
    create_exam_type("Java Basics reg", "Admin")
    create_exam_type("Java Basics reg", "Student_J_reg")
    create_exam_type("Java Basics reg", "Student_J_pre")
    # Java Basics prem
    create_exam_type("Java Basics prem", "Admin")
    create_exam_type("Java Basics prem", "Student_J_pre")
    create_exam_type("Java Basics prem", "Student_J_pre_outsider")
    # HTML, CSS, JS reg
    create_exam_type("HTML, CSS, JS reg", "Admin")
    create_exam_type("HTML, CSS, JS reg", "Student_HTML_reg")
    create_exam_type("HTML, CSS, JS reg", "Student_HTML_prem")
    # HTML, CSS, JS prem
    create_exam_type("HTML, CSS, JS prem", "Admin")
    create_exam_type("HTML, CSS, JS prem", "Student_HTML_prem")
    create_exam_type("HTML, CSS, JS prem", "Student_HTML_prem_outsider")
    # create users
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
    assert user_role
    join_user_to_role = UserRoles(user_id=user.id, role_id=user_role.id)
    join_user_to_role.save()


def create_role(role_name):
    user_role = Role.query.filter(Role.name == role_name).first()
    if not user_role:
        user_role = Role(name=role_name)
        user_role.save()


def create_exam_type(exam_type):
    user_exam_type = ExamType.query.filter(ExamType.name == exam_type).first()
    if not user_exam_type:
        user_exam_type = ExamType(name=exam_type)
        user_exam_type.save()


def connect_exam_type_role(exam_type, role_name):
    the_exam_type = ExamType.query.filter(ExamType.name == exam_type).first()
    assert the_exam_type
    the_role = Role.query.filter(Role.name == role_name).first()
    assert the_role
    the_connect = RoleExamType.query.filter(
        RoleExamType.exam_type_id == the_exam_type.id,
        RoleExamType.role_id == the_role.id,
    ).first()
    if not the_connect:
        RoleExamType(exam_type_id=the_exam_type.id, role_id=the_role.id).save()


@app.cli.command()
@click.confirmation_option(prompt="Drop all database tables?")
def drop_db():
    """Drop the current database."""
    db.drop_all()


if __name__ == "__main__":
    app.run()
