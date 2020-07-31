from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, HiddenField, TextAreaField, SelectField
from wtforms.validators import DataRequired, Length


class ExamForm(FlaskForm):
    exam_id = HiddenField("id", validators=[DataRequired()])
    name = StringField("Exam:", validators=[DataRequired(), Length(5, 30)])
    instruction = TextAreaField("Instruction")
    code = TextAreaField("Code")
    submit = SubmitField("Go")


class CreateExamForm(FlaskForm):
    name = StringField("Exam:", validators=[DataRequired(), Length(5, 30)])
    lang = SelectField(
        "Lang",
        default="py",
        choices=[("py", "python"), ("java", "java"), ("html", "html")],
    )
    exam_type = SelectField("Type", default="code", choices=[("code", "code")])
    exam_level = SelectField(
        "Exam Level:",
        choices=[
            ("Python Basics reg", "Python Basics reg"),
            ("Python Basics prem", "Python Basics prem"),
            ("Python Inter", "Python Inter"),
            ("Python Inter Prem", "Python Inter Prem"),
            ("Python adv", "Python adv"),
            ("Python adv prem", "Python adv prem"),
        ],
    )
    instruction = TextAreaField("Instruction")
    solution = TextAreaField("Solution")
    template = TextAreaField("Template")
    verification = TextAreaField("Verification")
    submit = SubmitField("Create")


class SolutionForm(ExamForm):
    solution = TextAreaField("Solution")
