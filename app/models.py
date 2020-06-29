from app import db
from .auth.models import User, AnonymousUser  # noqa
from app.utils import ModelMixin

# Define your models here.
# You can also define them inside a package and import them here.
# This is only a convenience so that all your models are available from a single module.


class ExamType(db.Model, ModelMixin):
    '''
    It represents a type of exam like: regular, premium
    '''
    __tablename__ = "exam_types"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), unique=True, nullable=False)
    role_id = db.Column(db.Integer(), db.ForeignKey("roles.id", ondelete="CASCADE"))
