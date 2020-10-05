from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    SubmitField,
    HiddenField,
    TextAreaField,
    SelectField,
    BooleanField,
)
from wtforms.validators import DataRequired, Length


class ExamForm(FlaskForm):
    exam_id = HiddenField("id", validators=[DataRequired()])
    name = StringField("Question:", validators=[DataRequired(), Length(5, 30)])
    instruction = TextAreaField("Instruction")
    code = TextAreaField("Code")
    result = BooleanField("Result", default=False)
    submit = SubmitField("Submit")


class CreateExamForm(FlaskForm):
    name = StringField("Question:", validators=[DataRequired(), Length(5, 30)])
    lang = SelectField(
        "Lang",
        default="py",
        choices=[("py", "python"), ("java", "java"), ("html", "html")],
    )
    exam_type = SelectField("Type", default="code", choices=[("code", "code")])
    exam_level = SelectField(
        "Question Level:",
        choices=[
            ("Python Basics reg", "Python Basics Regular"),
            ("Python Basics prem", "Python Basics Premium"),
            ("Python Inter", "Python Intermediate"),
            ("Python Intermediate Premium", "Python Inter Prem"),
            ("Python adv", "Python Advanced"),
            ("Python adv prem", "Python Advanced Premium"),
            ("Java Basics reg", "Java Basics Regular"),
            ("Java Basics prem", "Java Basics Premium"),
            ("HTML, CSS, JS reg", "HTML, CSS, JS Regular"),
            ("HTML, CSS, JS prem", "HTML, CSS, JS Premium"),
        ],
    )
    instruction = TextAreaField("Instruction")
    solution = TextAreaField("Solution")
    template = TextAreaField("Template")
    verification = TextAreaField("Verification")
    submit = SubmitField("Create")


class SolutionForm(ExamForm):
    solution = TextAreaField("Solution")
