from datetime import datetime

from flask_login import AnonymousUserMixin
from flask_user import UserMixin
from sqlalchemy.ext.hybrid import hybrid_property
from werkzeug.security import generate_password_hash, check_password_hash

from app import db
from app.utils import ModelMixin


class User(db.Model, UserMixin, ModelMixin):

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(60), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.now)
    roles = db.relationship("Role", secondary="user_roles")

    @hybrid_property
    def password(self):
        return self.password_hash

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    @classmethod
    def authenticate(cls, user_id, password):
        user = cls.query.filter(cls.username == user_id).first()
        if user is not None and check_password_hash(user.password, password):
            return user
        return None

    def __repr__(self):
        return f"<User: {self.username}>"


class AnonymousUser(AnonymousUserMixin):
    pass


class Role(db.Model, ModelMixin):
    """
    User roles:
        Python Basic: Student_PB_reg, Student_PB_prem, Student_PB_prem_outsider
        Python Intermediate: Student_PI_reg, Student_PI_prem, Student_PI_prem_outsider
        Python Advanced: Student_PA_reg, Student_PA_prem, Student_PA_prem_outsider
        Java Basic: Student_J_reg, Student_J_pre, Student_J_pre_outsider
        HTML/CSS/JS: Student_HTML_reg, Student_HTML_prem, Student_HTML_prem_outsider
    """

    __tablename__ = "roles"

    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(50), unique=True)
    exam_types = db.relationship("ExamType")


class UserRoles(db.Model, ModelMixin):
    """Maping Users to the Roles"""

    __tablename__ = "user_roles"

    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey("users.id", ondelete="CASCADE"))
    role_id = db.Column(db.Integer(), db.ForeignKey("roles.id", ondelete="CASCADE"))
