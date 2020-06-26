from datetime import datetime

from flask_login import UserMixin, AnonymousUserMixin
from sqlalchemy.ext.hybrid import hybrid_property
from werkzeug.security import generate_password_hash, check_password_hash

from .. import db
from ..utils import ModelMixin


class User(db.Model, UserMixin, ModelMixin):

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(60), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.now)

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

    def __str__(self):
        return "<User: %s>" % self.username


class AnonymousUser(AnonymousUserMixin):
    pass


class Role(db.Model):
    '''User roles '''

    __tablename__ = "roles"
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(50), unique=True)


class UserRoles(db.Model):
    '''Maping Users to the Roles'''

    __tablename__ = "user_roles"
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeingKey('users.id', ondelete='CASCADE'))
    role_id = db.Column(db.Integer(), db.ForeingKey('roles.id', ondelete='CASCADE'))
