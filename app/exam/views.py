from flask import Blueprint, render_template, url_for, redirect, flash, request

from .models import Exam
from .forms import ExamForm
from .controller import check_answer
from app.tab import get_allowed_tabs

exam_blueprint = Blueprint("exam", __name__)


@exam_blueprint.route("/exam/<exam_id>", methods=["GET", "POST"])
def exam(exam_id):
    form = ExamForm(request.form)
    if form.validate_on_submit():
        exam = Exam.query.filter(Exam.id == form.exam_id.data).first()
        assert exam
        if check_answer(exam, form.code.data):
            flash(f"Exam '{exam.name}'.", "success")
        else:
            flash(f"Exam '{exam.name}'.", "danger")
        return redirect(url_for("exam.exam", exam_id=exam_id))
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
