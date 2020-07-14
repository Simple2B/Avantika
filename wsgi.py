#!/user/bin/env python
import click

from app import create_app, db, models, forms
from app.auth.models import User, Role, UserRoles
from app.exam.models import Exam, ExamLevels, RoleExamLevels

app = create_app()


# flask cli context setup
@app.shell_context_processor
def get_context():
    """Objects exposed here will be automatically available from the shell."""
    return dict(app=app, db=db, models=models, forms=forms)


def load_exams():
    Exam.load_all_exams()


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
    create_exam_level("Python Basics reg")
    create_exam_level("Python Basics prem")
    create_exam_level("Python Inter")
    create_exam_level("Python Inter Prem")
    create_exam_level("Python adv")
    create_exam_level("Python adv prem")
    create_exam_level("Java Basics reg")
    create_exam_level("Java Basics prem")
    create_exam_level("HTML, CSS, JS reg")
    create_exam_level("HTML, CSS, JS prem")
    # create all connection exam_type with role
    # Python Basics reg
    connect_exam_level_role("Python Basics reg", "Admin")
    connect_exam_level_role("Python Basics reg", "Student_PB_reg")
    connect_exam_level_role("Python Basics reg", "Student_PB_prem")
    connect_exam_level_role("Python Basics reg", "Student_PI_reg")
    connect_exam_level_role("Python Basics reg", "Student_PI_prem")
    connect_exam_level_role("Python Basics reg", "Student_PA_reg")
    connect_exam_level_role("Python Basics reg", "Student_PA_prem")
    # Python Basics prem
    connect_exam_level_role("Python Basics prem", "Admin")
    connect_exam_level_role("Python Basics prem", "Student_PB_prem")
    connect_exam_level_role("Python Basics prem", "Student_PB_prem_outsider")
    connect_exam_level_role("Python Basics prem", "Student_PI_prem")
    connect_exam_level_role("Python Basics prem", "Student_PI_prem_outsider")
    connect_exam_level_role("Python Basics prem", "Student_PA_prem")
    connect_exam_level_role("Python Basics prem", "Student_PA_prem_outsider")
    # Python Inter
    connect_exam_level_role("Python Inter", "Admin")
    connect_exam_level_role("Python Inter", "Student_PI_reg")
    connect_exam_level_role("Python Inter", "Student_PI_prem")
    connect_exam_level_role("Python Inter", "Student_PA_reg")
    connect_exam_level_role("Python Inter", "Student_PA_prem")
    # Python Inter Prem
    connect_exam_level_role("Python Inter Prem", "Admin")
    connect_exam_level_role("Python Inter Prem", "Student_PI_prem")
    connect_exam_level_role("Python Inter Prem", "Student_PI_prem_outsider")
    connect_exam_level_role("Python Inter Prem", "Student_PA_prem")
    connect_exam_level_role("Python Inter Prem", "Student_PA_prem_outsider")
    # Python adv
    connect_exam_level_role("Python adv", "Admin")
    connect_exam_level_role("Python adv", "Student_PA_reg")
    connect_exam_level_role("Python adv", "Student_PA_prem")
    # Python adv prem
    connect_exam_level_role("Python adv prem", "Admin")
    connect_exam_level_role("Python adv prem", "Student_PA_prem")
    connect_exam_level_role("Python adv prem", "Student_PA_prem_outsider")
    # Java Basics reg
    connect_exam_level_role("Java Basics reg", "Admin")
    connect_exam_level_role("Java Basics reg", "Student_J_reg")
    connect_exam_level_role("Java Basics reg", "Student_J_pre")
    # Java Basics prem
    connect_exam_level_role("Java Basics prem", "Admin")
    connect_exam_level_role("Java Basics prem", "Student_J_pre")
    connect_exam_level_role("Java Basics prem", "Student_J_pre_outsider")
    # HTML, CSS, JS reg
    connect_exam_level_role("HTML, CSS, JS reg", "Admin")
    connect_exam_level_role("HTML, CSS, JS reg", "Student_HTML_reg")
    connect_exam_level_role("HTML, CSS, JS reg", "Student_HTML_prem")
    # HTML, CSS, JS prem
    connect_exam_level_role("HTML, CSS, JS prem", "Admin")
    connect_exam_level_role("HTML, CSS, JS prem", "Student_HTML_prem")
    connect_exam_level_role("HTML, CSS, JS prem", "Student_HTML_prem_outsider")
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


def create_exam_level(exam_level):
    user_exam_level = ExamLevels.query.filter(ExamLevels.name == exam_level).first()
    if not user_exam_level:
        user_exam_level = ExamLevels(name=exam_level)
        user_exam_level.save()


def connect_exam_level_role(exam_level, role_name):
    the_exam_level = ExamLevels.query.filter(ExamLevels.name == exam_level).first()
    assert the_exam_level
    the_role = Role.query.filter(Role.name == role_name).first()
    assert the_role
    the_connect = RoleExamLevels.query.filter(
        RoleExamLevels.exam_level_id == the_exam_level.id,
        RoleExamLevels.role_id == the_role.id,
    ).first()
    if not the_connect:
        RoleExamLevels(exam_level_id=the_exam_level.id, role_id=the_role.id).save()


@app.cli.command()
@click.confirmation_option(prompt="Drop all database tables?")
def drop_db():
    """Drop the current database."""
    db.drop_all()


if __name__ == "__main__":
    app.run()
