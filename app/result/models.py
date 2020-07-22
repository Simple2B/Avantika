from app import db
from app.utils import ModelMixin


# from app.logger import log


class Result(db.Model, ModelMixin):
    """ Model of results exam must have this field: id, passed (true/false), exam_id, user_id """

    __tablename__ = "results"

    id = db.Column(db.Integer, primary_key=True)
    exam_id = db.Column(db.Integer(), db.ForeignKey("exams.id"))
    user_id = db.Column(db.Integer(), db.ForeignKey("users.id"))
    passed = db.Column(db.Boolean, default=False)
    exam = db.relationship("Exam")
    user = db.relationship("User")
