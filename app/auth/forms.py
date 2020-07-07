from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    PasswordField,
    SubmitField,
    ValidationError,
    SelectField,
)
from wtforms.validators import DataRequired, Length, EqualTo
from .models import User


class LoginForm(FlaskForm):
    user_id = StringField("Username", [DataRequired()])
    password = PasswordField("Password", [DataRequired()])
    submit = SubmitField("Login")


class RegistrationForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired(), Length(2, 30)])
    password = PasswordField("Password", validators=[DataRequired(), Length(6, 30)])
    password_confirmation = PasswordField(
        "Confirm Password",
        validators=[
            DataRequired(),
            EqualTo("password", message="Password do not match."),
        ],
    )
    role = SelectField(
        "Role:",
        default="user",
        choices=[
            ("admin", "Admin"),
            ("student_PB_reg", "Student_PB_reg"),
            ("student_PB_prem", "Student_PB_prem"),
            ("student_PB_prem_outsider", "Student_PB_prem_outsider"),
            ("student_PI_reg", "Student_PI_reg"),
            ("student_PI_prem", "Student_PI_prem"),
            ("student_PI_prem_outsider", "Student_PI_prem_outsider"),
            ("student_PA_reg", "Student_PA_reg"),
            ("student_PA_prem", "Student_PA_prem"),
            ("student_PA_prem_outsider", "Student_PA_prem_outsider"),
            ("student_J_reg", "Student_J_reg"),
            ("student_J_pre", "Student_J_pre"),
            ("student_J_pre_outsider", "Student_J_pre_outsider"),
            ("student_HTML_reg", "Student_HTML_reg"),
            ("student_HTML_prem", "Student_HTML_prem"),
            ("student_HTML_prem_outsider", "Student_HTML_prem_outsider"),
        ],
    )
    active = SelectField(
        "Active:",
        default="active",
        choices=[("not_active", "Not Active"), ("active", "Active")],
    )
    submit = SubmitField("Register")

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first() is not None:
            raise ValidationError("This username is taken.")
