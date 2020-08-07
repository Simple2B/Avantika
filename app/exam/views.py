from flask import Blueprint, render_template, url_for, redirect, flash, request
from flask_user import roles_required, current_user

from .models import Exam, ExamLevel
from .forms import ExamForm, CreateExamForm, SolutionForm
from .choisen_answer.forms import ChoiceCreateExamForm, ChoiceExamForm
from .controller import (
    check_answer,
    goto_next_exam,
    check_answer_choice,
    goto_prev_exam,
)
from app.result.controller import go_pass_exam, next_to_pass_exam, go_fail_exam
from app.tab import get_allowed_tabs
from app.logger import log

exam_blueprint = Blueprint("exam", __name__)


def render_base_template(template_name_or_list, **args):
    return render_template(template_name_or_list, tabs=get_allowed_tabs(), **args)


def exam_level_sort(reg_name: str, prem_name: str, path):
    level = ExamLevel.query.filter(ExamLevel.name == reg_name).first()
    exams = Exam.query.filter(Exam.type_id == level.id).all()
    level_prem = ExamLevel.query.filter(ExamLevel.name == prem_name).first()
    exams_prem = Exam.query.filter(Exam.type_id == level_prem.id).all()
    return render_base_template(path, exams=exams, exams_prem=exams_prem)


@exam_blueprint.route("/main_exam_py_base", methods=["GET", "POST"])
def main_exam_page_py_base():
    return exam_level_sort(
        "Python Basics reg", "Python Basics prem", "exam/main_exam_page_py_base.html"
    )


@exam_blueprint.route("/main_exam_py_inter", methods=["GET", "POST"])
def main_exam_page_py_inter():
    return exam_level_sort(
        "Python Inter", "Python Inter Prem", "exam/main_exam_page_py_inter.html"
    )


@exam_blueprint.route("/main_exam_py_adv", methods=["GET", "POST"])
def main_exam_page_py_adv():
    return exam_level_sort(
        "Python adv", "Python adv prem", "exam/main_exam_page_py_adv.html"
    )


@exam_blueprint.route("/main_exam_java", methods=["GET", "POST"])
def main_exam_page_java():
    return exam_level_sort(
        "Java Basics reg", "Java Basics prem", "exam/main_exam_page_java.html"
    )


@exam_blueprint.route("/main_exam_html", methods=["GET", "POST"])
def main_exam_page_html():
    return exam_level_sort(
        "HTML, CSS, JS reg", "HTML, CSS, JS prem", "exam/main_exam_page_html.html"
    )


@exam_blueprint.route("/exam/py/<exam_id>", methods=["GET", "POST"])
def exam_py(exam_id):
    exam = Exam.query.filter(Exam.id == exam_id).first()
    if exam.exam_type == Exam.Type.code:
        form = ExamForm(request.form)
    else:
        form = ChoiceExamForm(request.form)
        form.answer.choices = [(choice, choice) for choice in exam.answer.split("\n")]
    if form.validate_on_submit():
        if request.form["submit"] == "Next":
            user = current_user
            next_to_pass_exam(exam_id=exam.id, user_id=user.id)
            return goto_next_exam(exam_id)
        elif request.form["submit"] == "Prev":
            return goto_prev_exam(exam_id)
        else:
            assert exam
            if exam.exam_type == Exam.Type.code:
                if check_answer(exam, form.code.data) is True:
                    flash(f"Exam success '{exam.name}'.", "success")
                    user = current_user
                    go_pass_exam(exam_id=exam.id, user_id=user.id)
                else:
                    flash(f"Exam failed '{exam.name}'.", "danger")
                    user = current_user
                    go_fail_exam(exam_id=exam.id, user_id=user.id)
            elif exam.exam_type == Exam.Type.choice:
                if check_answer_choice(exam.id, form.answer.data) is True:
                    flash(f"Exam success '{exam.name}'.", "success")
                    user = current_user
                    go_pass_exam(exam_id=exam.id, user_id=user.id)
                else:
                    flash(f"Exam failed '{exam.name}'.", "danger")
                    user = current_user
                    go_fail_exam(exam_id=exam.id, user_id=user.id)
            else:
                flash(f"Exam failed '{exam.name}'.", "danger")
                user = current_user
                go_fail_exam(exam_id=exam.id, user_id=user.id)
            if exam.exam_type == Exam.Type.code:
                return render_base_template(
                    "exam/exam.html",
                    form=form,
                    instruction_height=(exam.instruction.count("\n") + 2),
                    code_height=(exam.template.count("\n") + 2),
                )
            elif exam.exam_type == Exam.Type.choice:
                return render_base_template(
                    "exam/exam_choice.html",
                    form=form,
                    instruction_height=(exam.instruction.count("\n") + 2),
                )
            else:
                return render_base_template(
                    "exam/exam.html",
                    form=form,
                    instruction_height=(exam.instruction.count("\n") + 2),
                    code_height=(exam.template.count("\n") + 2),
                )
    elif form.is_submitted():
        if request.form["submit"] == "Next":
            user = current_user
            next_to_pass_exam(exam_id=exam.id, user_id=user.id)
            return goto_next_exam(exam_id)
        elif request.form["submit"] == "Prev":
            return goto_prev_exam(exam_id)
    if exam.exam_type == Exam.Type.code:
        form.name.data = exam.name
        form.exam_id.data = exam.id
        form.code.data = exam.template
        form.instruction.data = exam.instruction
        return render_base_template(
            "exam/exam.html",
            form=form,
            instruction_height=(exam.instruction.count("\n") + 2),
        )
    form.name.data = exam.name
    form.exam_id.data = exam.id
    form.answer.choices = [(choice, choice) for choice in exam.answer.split("\n")]
    form.instruction.data = exam.instruction
    return render_base_template(
        "exam/exam_choice.html",
        form=form,
        instruction_height=(exam.instruction.count("\n") + 2),
    )


@exam_blueprint.route("/exam_lang/<lang>")
def exam_lang(lang):
    exam = Exam.query.filter(Exam.lang == lang).first()
    return redirect(url_for(f"exam.exam_{lang}", exam_id=exam.id))


@exam_blueprint.route("/exam/java/<exam_id>", methods=["GET", "POST"])
def exam_java(exam_id):
    exam = Exam.query.filter(Exam.id == exam_id).first()
    if exam.exam_type == Exam.Type.code:
        form = ExamForm(request.form)
    else:
        form = ChoiceExamForm(request.form)
        form.answer.choices = [(choice, choice) for choice in exam.answer.split("\n")]
    if form.validate_on_submit():
        if request.form["submit"] == "Next":
            user = current_user
            next_to_pass_exam(exam_id=exam.id, user_id=user.id)
            return goto_next_exam(exam_id)
        elif request.form["submit"] == "Prev":
            return goto_prev_exam(exam_id)
        else:
            assert exam
            if exam.exam_type == Exam.Type.code:
                if check_answer(exam, form.code.data):
                    flash(f"Exam success '{exam.name}'.", "success")
                    user = current_user
                    go_pass_exam(exam_id=exam.id, user_id=user.id)
                else:
                    flash(f"Exam failed '{exam.name}'.", "danger")
                    user = current_user
                    go_fail_exam(exam_id=exam.id, user_id=user.id)
            elif exam.exam_type == Exam.Type.choice:
                if check_answer_choice(exam.id, form.answer.data):
                    flash(f"Exam success '{exam.name}'.", "success")
                    user = current_user
                    go_pass_exam(exam_id=exam.id, user_id=user.id)
                else:
                    flash(f"Exam failed '{exam.name}'.", "danger")
                    user = current_user
                    go_fail_exam(exam_id=exam.id, user_id=user.id)
            else:
                flash(f"Exam failed '{exam.name}'.", "danger")
            # return redirect(url_for("exam.exam_py", exam_id=exam_id))
            if exam.exam_type == Exam.Type.code:
                return render_base_template(
                    "exam/exam.html",
                    form=form,
                    instruction_height=(exam.instruction.count("\n") + 2),
                    code_height=(exam.template.count("\n") + 2),
                )
            elif exam.exam_type == Exam.Type.choice:
                return render_base_template(
                    "exam/exam_choice.html",
                    form=form,
                    instruction_height=(exam.instruction.count("\n") + 2),
                )
            else:
                return render_base_template(
                    "exam/exam.html",
                    form=form,
                    instruction_height=(exam.instruction.count("\n") + 2),
                    code_height=(exam.template.count("\n") + 2),
                )
    elif form.is_submitted():
        flash("The given data was invalid.", "danger")

    if exam.exam_type == Exam.Type.code:
        form.name.data = exam.name
        form.exam_id.data = exam.id
        form.code.data = exam.template
        form.instruction.data = exam.instruction
        return render_base_template(
            "exam/exam.html",
            form=form,
            instruction_height=(exam.instruction.count("\n") + 2),
        )
    form.name.data = exam.name
    form.exam_id.data = exam.id
    form.answer.choices = [(choice, choice) for choice in exam.answer.split("\n")]
    form.instruction.data = exam.instruction
    return render_base_template(
        "exam/exam_choice.html",
        form=form,
        instruction_height=(exam.instruction.count("\n") + 2),
    )


@exam_blueprint.route("/exam/html/<exam_id>", methods=["GET", "POST"])
def exam_html(exam_id):
    exam = Exam.query.filter(Exam.id == exam_id).first()
    if exam.exam_type == Exam.Type.code:
        form = ExamForm(request.form)
    else:
        form = ChoiceExamForm(request.form)
        form.answer.choices = [(choice, choice) for choice in exam.answer.split("\n")]
    if form.validate_on_submit():
        if request.form["submit"] == "Next":
            user = current_user
            next_to_pass_exam(exam_id=exam.id, user_id=user.id)
            return goto_next_exam(exam_id)
        elif request.form["submit"] == "Prev":
            return goto_prev_exam(exam_id)
        else:
            assert exam
            if exam.exam_type == Exam.Type.code:
                if check_answer(exam, form.code.data):
                    flash(f"Exam success '{exam.name}'.", "success")
                    user = current_user
                    go_pass_exam(exam_id=exam.id, user_id=user.id)
                else:
                    flash(f"Exam failed '{exam.name}'.", "danger")
                    user = current_user
                    go_fail_exam(exam_id=exam.id, user_id=user.id)
            elif exam.exam_type == Exam.Type.choice:
                if check_answer_choice(exam.id, form.answer.data):
                    flash(f"Exam success '{exam.name}'.", "success")
                    user = current_user
                    go_pass_exam(exam_id=exam.id, user_id=user.id)
                else:
                    flash(f"Exam failed '{exam.name}'.", "danger")
                    user = current_user
                    go_fail_exam(exam_id=exam.id, user_id=user.id)
            else:
                flash(f"Exam failed '{exam.name}'.", "danger")
        if exam.exam_type == Exam.Type.code:
            return render_base_template(
                "exam/exam.html",
                form=form,
                instruction_height=(exam.instruction.count("\n") + 2),
                code_height=(exam.template.count("\n") + 2),
            )
        elif exam.exam_type == Exam.Type.choice:
            return render_base_template(
                "exam/exam_choice.html",
                form=form,
                instruction_height=(exam.instruction.count("\n") + 2),
            )
        else:
            return render_base_template(
                "exam/exam.html",
                form=form,
                instruction_height=(exam.instruction.count("\n") + 2),
                code_height=(exam.template.count("\n") + 2),
            )
    elif form.is_submitted():
        flash("The given data was invalid.", "danger")

    if exam.exam_type == Exam.Type.code:
        form.name.data = exam.name
        form.exam_id.data = exam.id
        form.code.data = exam.template
        form.instruction.data = exam.instruction
        return render_base_template(
            "exam/exam.html",
            form=form,
            instruction_height=(exam.instruction.count("\n") + 2),
        )
    form.name.data = exam.name
    form.exam_id.data = exam.id
    form.answer.choices = [(choice, choice) for choice in exam.answer.split("\n")]
    form.instruction.data = exam.instruction
    return render_base_template(
        "exam/exam_choice.html",
        form=form,
        instruction_height=(exam.instruction.count("\n") + 2),
    )


@exam_blueprint.route("/create_exam", methods=["GET", "POST"])
@roles_required("Admin")
def create_exam():
    form = CreateExamForm(request.form)
    if form.validate_on_submit():
        exam = Exam()
        exam.name = form.name.data
        level = ExamLevel.query.filter(ExamLevel.name == form.exam_level.data).first()
        if not level:
            flash("The level invalid", "danger")
        exam.type_id = level.id
        exam.exam_type = form.exam_type.data
        exam.lang = form.lang.data
        exam.instruction = form.instruction.data
        exam.solution = form.solution.data
        exam.template = form.template.data
        exam.verification = form.verification.data
        exam.save()
        return redirect_for_lang(exam.lang)

    elif form.is_submitted():
        flash("The given data was invalid.", "danger")
    return render_base_template(
        "exam/create_exam_py.html", form=form, post_action=url_for("exam.create_exam"),
    )


@exam_blueprint.route("/create_choice_exam", methods=["GET", "POST"])
@roles_required("Admin")
def create_choice_exam():
    form = ChoiceCreateExamForm(request.form)
    if form.validate_on_submit():
        exam = Exam()
        exam.name = form.name.data
        level = ExamLevel.query.filter(ExamLevel.name == form.exam_level.data).first()
        if not level:
            flash("The level invalid", "danger")
        exam.type_id = level.id
        exam.exam_type = form.exam_type.data
        exam.lang = form.lang.data
        exam.instruction = form.instruction.data
        exam.answer = form.answer.data
        exam.correct_answer = form.correct_answer.data
        exam.save()
        return redirect_for_lang(exam.lang)
    elif form.is_submitted():
        flash("The given data was invalid.", "danger")
    return render_base_template(
        "exam/create_exam_choice.html",
        form=form,
        post_action=url_for("exam.create_choice_exam"),
    )


@exam_blueprint.route("/delete_exam/<exam_id>", methods=["GET"])
@roles_required("Admin")
def delete_exam(exam_id):
    exam_id = int(exam_id)
    exam = Exam.query.filter(Exam.id == exam_id).first()
    if exam:
        exam.deleted = True
        flash(f"Exam {exam.name} deleted", "success")
        exam.save()
    else:
        flash("Wrong exam id", "danger")
    return redirect_for_lang(exam.lang)


@exam_blueprint.route("/exam_edit/<exam_id>", methods=["GET", "POST"])
@roles_required("Admin")
def edit_exam(exam_id):
    exam_id = int(exam_id)
    log(log.DEBUG, "edit exam: [%d]", exam_id)
    exam = Exam.query.filter(Exam.id == exam_id).first()
    if exam is None:
        flash("Wrong exam id.", "danger")
        log(log.WARNING, "NONEXISTENT EXAM [%d]", exam_id)
        return redirect(url_for("dashboard.list_of_exam"))
    if exam.exam_type == Exam.Type.code:
        form = CreateExamForm(request.form)
        if form.validate_on_submit():
            exam.name = form.name.data
            level = ExamLevel.query.filter(
                ExamLevel.name == form.exam_level.data
            ).first()
            if not level:
                flash("The level invalid", "danger")
                log(log.WARNING, "NONEXISTENT LEVEL %s", form.exam_level.data)
            exam.type_id = level.id
            exam.exam_type = form.exam_type.data
            exam.lang = form.lang.data
            exam.instruction = form.instruction.data
            exam.solution = form.solution.data
            exam.template = form.template.data
            exam.verification = form.verification.data
            exam.save()
            return redirect_for_lang(exam.lang)
        else:
            form.name.data = exam.name
            form.lang.data = exam.lang
            form.exam_type.data = exam.exam_type
            form.exam_level.data = exam.exam_level.name
            form.instruction.data = exam.instruction
            form.template.data = exam.template
            form.solution.data = exam.solution
            form.verification.data = exam.verification
        return render_base_template(
            "exam/create_exam_py.html",
            form=form,
            post_action=url_for("exam.edit_exam", exam_id=exam_id),
        )
    else:
        form = ChoiceCreateExamForm(request.form)
        form.answer.choices = [(choice, choice) for choice in exam.answer.split("\n")]
        if form.validate_on_submit():
            exam.name = form.name.data
            level = ExamLevel.query.filter(
                ExamLevel.name == form.exam_level.data
            ).first()
            if not level:
                flash("The level invalid", "danger")
                log(log.WARNING, "NONEXISTENT LEVEL %s", form.exam_level.data)
            exam.type_id = level.id
            exam.exam_type = form.exam_type.data
            exam.instruction = form.instruction.data
            exam.answer = form.answer.data
            exam.correct_answer = form.correct_answer.data
            exam.save()
            return redirect_for_lang(exam.lang)
        else:
            form.name.data = exam.name
            form.exam_level.data = exam.exam_level.name
            form.exam_type.data = exam.exam_type
            form.instruction.data = exam.instruction
            form.answer.data = exam.answer
            form.correct_answer.data = exam.correct_answer
        return render_base_template(
            "exam/create_exam_choice.html",
            form=form,
            post_action=url_for("exam.edit_exam", exam_id=exam_id),
        )


@exam_blueprint.route("/show_solution/<exam_id>", methods=["GET"])
def show_solution(exam_id):
    exam_id = int(exam_id)
    form = SolutionForm(request.form)
    exam = Exam.query.filter(Exam.id == exam_id).first()
    form.exam_id.data = exam_id
    form.name.data = exam.name
    form.instruction.data = exam.instruction
    form.code.data = exam.template
    form.solution.data = exam.solution
    return render_base_template(
        "exam/show_solution.html",
        form=form,
        instruction_height=(exam.instruction.count("\n") + 2),
        code_height=(exam.template.count("\n") + 2),
    )


def redirect_for_lang(lang):
    """Redirect by exam language
    """
    if lang == Exam.Language.py:
        return redirect(url_for("dashboard.list_of_exam"))
    elif lang == Exam.Language.java:
        return redirect(url_for("dashboard.list_of_exam_java"))
    elif lang == Exam.Language.html:
        return redirect(url_for("dashboard.list_of_exam_html"))
