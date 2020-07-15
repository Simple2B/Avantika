from flask import Blueprint, render_template, url_for, redirect, flash, request

from .models import Exam
from .forms import ExamForm
from .controller import check_answer, goto_next_exam
from app.tab import get_allowed_tabs

exam_blueprint = Blueprint("exam", __name__)


@exam_blueprint.route("/exam/py/<exam_id>", methods=["GET", "POST"])
def exam_py(exam_id):
    form = ExamForm(request.form)
    if form.validate_on_submit():
        if form.submit.label.text == "Next":
            return goto_next_exam(exam_id)
        else:
            exam = Exam.query.filter(Exam.id == exam_id).first()
            assert exam
            if check_answer(exam, form.code.data):
                flash(f"Exam '{exam.name}'.", "success")
            else:
                flash(f"Exam '{exam.name}'.", "danger")
            return redirect(url_for("exam.exam_py", exam_id=exam_id))
    elif form.is_submitted():
        flash("The given data was invalid.", "danger")
    exam = Exam.query.filter(Exam.id == exam_id).first()
    form.name.data = exam.name
    form.exam_id.data = exam.id
    form.code.data = exam.template
    form.instruction.data = exam.instruction
    return render_template(
        "exam/exam.html",
        form=form,
        instruction_height=(exam.instruction.count("\n") + 2),
        code_height=(exam.template.count("\n") + 2),
        tabs=get_allowed_tabs(),
    )


@exam_blueprint.route("/exam_lang/<lang>")
def exam_lang(lang):
    exam = Exam.query.filter(Exam.lang == lang).first()
    return redirect(url_for(f"exam.exam_{lang}", exam_id=exam.id))


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
    return render_template(
        "exam/exam_html_css.html",
        form=form,
        instruction_height=(exam.instruction.count("\n") + 2),
        code_height=(exam.template.count("\n") + 2),
        tabs=get_allowed_tabs(),
    )
