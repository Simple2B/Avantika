from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, HiddenField, TextAreaField
from wtforms.validators import DataRequired, Length


class ExamForm(FlaskForm):
    exam_id = HiddenField("id", validators=[DataRequired()])
    name = StringField("Exam:", validators=[DataRequired(), Length(5, 30)])
    instruction = TextAreaField("Instruction")
    code = TextAreaField("Code")
    submit = SubmitField("Go")
