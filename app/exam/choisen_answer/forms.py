from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    SubmitField,
    HiddenField,
    TextAreaField,
    SelectField,
    RadioField,
)
from wtforms.validators import DataRequired, Length


class ChoiseExamForm(FlaskForm):
    exam_id = HiddenField("id", validators=[DataRequired()])
    name = StringField("Exam:", validators=[DataRequired(), Length(5, 30)])
    instruction = TextAreaField("Instruction")
    answers = RadioField("Answer")
    submit = SubmitField("Go")


class ChoiseCreateExamForm(FlaskForm):
    name = StringField("Exam:", validators=[DataRequired(), Length(5, 30)])
    lang = SelectField(
        "Lang",
        default="py",
        choices=[("py", "python"), ("java", "java"), ("html", "html")],
    )

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
    answers = RadioField("Answer")
    correct_index = TextAreaField("Template")
    submit = SubmitField("Create")
