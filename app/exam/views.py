from flask import (
    Blueprint,
    render_template,
    url_for,
    redirect,
    flash,
    request,
    make_response,
)
from flask_user import roles_required, current_user

from .models import Exam, ExamLevel
from .forms import ExamForm, CreateExamForm, SolutionForm
from .choisen_answer.forms import ChoiseExamForm, ChoiseCreateExamForm
from .controller import (
    check_answer,
    goto_next_exam,
    check_answer_choise,
    goto_prev_exam,
)
from app.result.controller import go_pass_exam, next_to_pass_exam
from app.tab import get_allowed_tabs
from app.logger import log

exam_blueprint = Blueprint("exam", __name__)


@exam_blueprint.route("/exam/py/<exam_id>", methods=["GET", "POST"])
def exam_py(exam_id):
    exam = Exam.query.filter(Exam.id == exam_id).first()
    if exam.exam_type == Exam.Type.code:
        form = ExamForm(request.form)
    else:
        form = ChoiseExamForm(request.form)
        form.answer.choices = [(choise, choise) for choise in exam.answer.split("\n")]
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
            elif exam.exam_type == Exam.Type.choise:
                if check_answer_choise(exam.id, form.answer.data):
                    flash(f"Exam success '{exam.name}'.", "success")
                    user = current_user
                    go_pass_exam(exam_id=exam.id, user_id=user.id)
                else:
                    flash(f"Exam failed '{exam.name}'.", "danger")
            else:
                flash(f"Exam failed '{exam.name}'.", "danger")
            if exam.exam_type == Exam.Type.code:
                return render_template(
                    "exam/exam.html",
                    form=form,
                    instruction_height=(exam.instruction.count("\n") + 2),
                    code_height=(exam.template.count("\n") + 2),
                    tabs=get_allowed_tabs(),
                )
            elif exam.exam_type == Exam.Type.choise:
                return render_template(
                    "exam/exam_choise.html",
                    form=form,
                    instruction_height=(exam.instruction.count("\n") + 2),
                    tabs=get_allowed_tabs(),
                )
            else:
                return render_template(
                    "exam/exam.html",
                    form=form,
                    instruction_height=(exam.instruction.count("\n") + 2),
                    code_height=(exam.template.count("\n") + 2),
                    tabs=get_allowed_tabs(),
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
        return render_template(
            "exam/exam.html",
            form=form,
            instruction_height=(exam.instruction.count("\n") + 2),
            tabs=get_allowed_tabs(),
        )
    form.name.data = exam.name
    form.exam_id.data = exam.id
    form.answer.choices = [(choise, choise) for choise in exam.answer.split("\n")]
    form.instruction.data = exam.instruction
    return render_template(
        "exam/exam_choise.html",
        form=form,
        instruction_height=(exam.instruction.count("\n") + 2),
        tabs=get_allowed_tabs(),
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
        form = ChoiseExamForm(request.form)
        form.answer.choices = [(choise, choise) for choise in exam.answer.split("\n")]
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
            elif exam.exam_type == Exam.Type.choise:
                if check_answer_choise(exam.id, form.answer.data):
                    flash(f"Exam success '{exam.name}'.", "success")
                    user = current_user
                    go_pass_exam(exam_id=exam.id, user_id=user.id)
                else:
                    flash(f"Exam failed '{exam.name}'.", "danger")
            else:
                flash(f"Exam failed '{exam.name}'.", "danger")
            # return redirect(url_for("exam.exam_py", exam_id=exam_id))
            if exam.exam_type == Exam.Type.code:
                return render_template(
                    "exam/exam.html",
                    form=form,
                    instruction_height=(exam.instruction.count("\n") + 2),
                    code_height=(exam.template.count("\n") + 2),
                    tabs=get_allowed_tabs(),
                )
            elif exam.exam_type == Exam.Type.choise:
                return render_template(
                    "exam/exam_choise.html",
                    form=form,
                    instruction_height=(exam.instruction.count("\n") + 2),
                    tabs=get_allowed_tabs(),
                )
            else:
                return render_template(
                    "exam/exam.html",
                    form=form,
                    instruction_height=(exam.instruction.count("\n") + 2),
                    code_height=(exam.template.count("\n") + 2),
                    tabs=get_allowed_tabs(),
                )
    elif form.is_submitted():
        flash("The given data was invalid.", "danger")

    if exam.exam_type == Exam.Type.code:
        form.name.data = exam.name
        form.exam_id.data = exam.id
        form.code.data = exam.template
        form.instruction.data = exam.instruction
        return render_template(
            "exam/exam.html",
            form=form,
            instruction_height=(exam.instruction.count("\n") + 2),
            tabs=get_allowed_tabs(),
        )
    form.name.data = exam.name
    form.exam_id.data = exam.id
    form.answer.choices = [(choise, choise) for choise in exam.answer.split("\n")]
    form.instruction.data = exam.instruction
    return render_template(
        "exam/exam_choise.html",
        form=form,
        instruction_height=(exam.instruction.count("\n") + 2),
        tabs=get_allowed_tabs(),
    )


@exam_blueprint.route("/exam/html/<exam_id>", methods=["GET", "POST"])
def exam_html(exam_id):
    form = ExamForm(request.form)
    exam = Exam.query.filter(Exam.id == exam_id).first()
    if form.validate_on_submit():
        return render_template(
            "exam/exam_html_css.html",
            form=form,
            instruction_height=(exam.instruction.count("\n") + 2),
            code_height=(exam.template.count("\n") + 2),
            tabs=get_allowed_tabs(),
        )
    elif form.is_submitted():
        flash("The given data was invalid.", "danger")
    form.name.data = exam.name
    form.exam_id.data = exam.id
    form.code.data = exam.template
    form.instruction.data = exam.instruction
    response = make_response(
        render_template(
            "exam/exam_html_css.html",
            form=form,
            instruction_height=(exam.instruction.count("\n") + 2),
            code_height=(exam.template.count("\n") + 2),
            tabs=get_allowed_tabs(),
        )
    )
    # response.set_cookie("SameSite", "None", max_age=60 * 60 * 24, secure=True)
    # response.set_cookie("SameSite", "Bubu")
    # response.set_cookie("UserName", "Kolya")
    return response


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
        return redirect(url_for("dashboard.index"))
    elif form.is_submitted():
        flash("The given data was invalid.", "danger")
    return render_template(
        "exam/create_exam_py.html", form=form, post_action=url_for("exam.create_exam"),
    )


@exam_blueprint.route("/create_choise_exam", methods=["GET", "POST"])
@roles_required("Admin")
def create_choise_exam():
    form = ChoiseCreateExamForm(request.form)
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
        return redirect(url_for("dashboard.index"))
    elif form.is_submitted():
        flash("The given data was invalid.", "danger")
    return render_template(
        "exam/create_exam_choise.html",
        form=form,
        post_action=url_for("exam.create_choise_exam"),
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
    return redirect(url_for("dashboard.index"))


@exam_blueprint.route("/exam_edit/<exam_id>", methods=["GET", "POST"])
@roles_required("Admin")
def edit_exam(exam_id):
    exam_id = int(exam_id)
    log(log.DEBUG, "edit exam: [%d]", exam_id)
    exam = Exam.query.filter(Exam.id == exam_id).first()
    if exam is None:
        flash("Wrong exam id.", "danger")
        log(log.WARNING, "NONEXISTENT EXAM [%d]", exam_id)
        return redirect(url_for("dashboard.index"))
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
            return redirect(url_for("dashboard.index"))
        else:
            form.name.data = exam.name
            form.lang.data = exam.lang
            form.exam_type.data = exam.exam_type
            form.exam_level.data = exam.exam_level.name
            form.instruction.data = exam.instruction
            form.template.data = exam.template
            form.solution.data = exam.solution
            form.verification.data = exam.verification
        return render_template(
            "exam/create_exam_py.html",
            form=form,
            post_action=url_for("exam.edit_exam", exam_id=exam_id),
        )
    else:
        form = ChoiseCreateExamForm(request.form)
        form.answer.choices = [(choise, choise) for choise in exam.answer.split("\n")]
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
            return redirect(url_for("dashboard.index"))
        else:
            form.name.data = exam.name
            form.exam_level.data = exam.exam_level.name
            form.exam_type.data = exam.exam_type
            form.instruction.data = exam.instruction
            form.answer.data = exam.answer
            form.correct_answer.data = exam.correct_answer
        return render_template(
            "exam/create_exam_choise.html",
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
    return render_template(
        "exam/show_solution.html",
        form=form,
        instruction_height=(exam.instruction.count("\n") + 2),
        code_height=(exam.template.count("\n") + 2),
    )
