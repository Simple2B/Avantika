from app import db
from app.utils import ModelMixin


# from app.logger import log

""" Model of result exam must have this field: id, passed (true/false), exam_id, user_id"""


class Result(db.Model, ModelMixin):

    __tablename__ = "result"


id = db.Column(db.Integer, primary_key=True)
exam_id = db.Column(db.Integer(), db.ForeignKey("exam.id"))
user_id = db.Column(db.Integer(), db.ForeignKey("user.id"))
passed = db.Column(db.Boolean, default=False)
