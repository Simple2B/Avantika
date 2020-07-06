from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    PasswordField,
    SubmitField,
    ValidationError,
    BooleanField,
)
from wtforms.validators import DataRequired, Length, EqualTo, InputRequired

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
    active = BooleanField("Active", validators=[InputRequired()])
    role = StringField("Role", validators=[DataRequired()])
    submit = SubmitField("Register")

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first() is not None:
            raise ValidationError("This username is taken.")
