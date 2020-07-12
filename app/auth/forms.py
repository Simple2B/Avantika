from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    PasswordField,
    SubmitField,
    ValidationError,
    SelectField,
    HiddenField,
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
        default="admin",
        choices=[
            ("Admin", "Admin"),
            ("Student_PB_reg", "Student_PB_reg"),
            ("Student_PB_prem", "Student_PB_prem"),
            ("Student_PB_prem_outsider", "Student_PB_prem_outsider"),
            ("Student_PI_reg", "Student_PI_reg"),
            ("Student_PI_prem", "Student_PI_prem"),
            ("Student_PI_prem_outsider", "Student_PI_prem_outsider"),
            ("Student_PA_reg", "Student_PA_reg"),
            ("Student_PA_prem", "Student_PA_prem"),
            ("Student_PA_prem_outsider", "Student_PA_prem_outsider"),
            ("Student_J_reg", "Student_J_reg"),
            ("Student_J_pre", "Student_J_pre"),
            ("Student_J_pre_outsider", "Student_J_pre_outsider"),
            ("Student_HTML_reg", "Student_HTML_reg"),
            ("Student_HTML_prem", "Student_HTML_prem"),
            ("Student_HTML_prem_outsider", "Student_HTML_prem_outsider"),
        ],
    )
    active = SelectField(
        "Active:",
        default="Active",
        choices=[("Not Active", "Not Active"), ("Active", "Active")],
    )
    submit = SubmitField("Register")

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first() is not None:
            raise ValidationError("This username is taken.")


UNCHANGED_PASSWORD = ""


class UserEditForm(RegistrationForm):
    user_id = HiddenField("user_id", validators=[DataRequired()])
    password = PasswordField("Password", default=UNCHANGED_PASSWORD,)
    password_confirmation = PasswordField(
        "Confirm Password",
        validators=[EqualTo("password", message="Password do not match.")],
        default=UNCHANGED_PASSWORD,
    )

    def validate_username(self, field):
        pass

    submit = SubmitField("Save")
