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


class ChoiceExamForm(FlaskForm):
    exam_id = HiddenField("id")
    name = StringField("Question:")
    instruction = TextAreaField("Instruction")
    answer = RadioField("Answer")
    submit = SubmitField("Submit")


class ChoiceCreateExamForm(FlaskForm):
    name = StringField("Question:", validators=[DataRequired(), Length(5, 30)])
    lang = SelectField(
        "Lang",
        default="py",
        choices=[("py", "python"), ("java", "java"), ("html", "html")],
    )
    exam_type = SelectField("Type", default="choice", choices=[("choice", "choice")])
    exam_level = SelectField(
        "Question Level:",
        choices=[
            ("Python Basics reg", "Python Basics reg"),
            ("Python Basics prem", "Python Basics prem"),
            ("Python Inter", "Python Inter"),
            ("Python Inter Prem", "Python Inter Prem"),
            ("Python adv", "Python adv"),
            ("Python adv prem", "Python adv prem"),
            ("HTML, CSS, JS reg", "HTML, CSS, JS reg"),
            ("HTML, CSS, JS prem", "HTML, CSS, JS prem"),
            ("Java Basics reg", "Java Basics reg"),
            ("Java Basics prem", "Java Basics prem"),
        ],
    )
    instruction = TextAreaField("Instruction")
    answer = TextAreaField("Answer")
    correct_answer = StringField("Correct Answer")
    submit = SubmitField("Create")
