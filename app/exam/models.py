import enum
import json
from sqlalchemy import Enum

from app import db
from app.utils import ModelMixin
from app.logger import log


class Exam(db.Model, ModelMixin):

    __tablename__ = "exams"

    class Language(enum.Enum):
        py = "python"
        java = "java"
        js = "javascript"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), unique=True, nullable=False)
    lang = db.Column(Enum(Language), default=Language.py)
    instruction = db.Column(db.String(1024), nullable=False)
    solution = db.Column(db.String(1024), nullable=False)
    template = db.Column(db.String(1024), nullable=False)
    verification = db.Column(db.String(1024), nullable=True)
    type_id = db.Column(db.Integer(), db.ForeignKey("exam_types.id"))
    exam_type = db.relationship("ExamType")

    def __repr__(self):
        return f"<Exam: {self.name}>"

    def to_dict(self):
        return dict(
            name=self.name,
            lang=self.lang.name,
            instruction=self.instruction.split("\n"),
            solution=self.solution.split("\n"),
            template=self.template.split("\n"),
            exam_type=self.exam_type.name,
        )

    def from_dict(self, **args):
        self.name = args["name"]
        self.lang = Exam.Language[args["lang"]] if "lang" in args else Exam.Language.py
        self.instruction = (
            "\n".join(args["instruction"]) if "instruction" in args else ""
        )
        self.solution = "\n".join(args["solution"]) if "solution" in args else ""
        self.template = "\n".join(args["template"]) if "template" in args else ""
        if "exam_type" in args:
            self.exam_type = ExamType.query.filter(
                ExamType.name == args["exam_type"]
            ).first()
        else:
            log(log.ERROR, "Exam [%s] has not type", self.name)
        if "verification" in args:
            self.verification = "\n".join(args["verification"])
        return self

    @staticmethod
    def load_all_exams():
        with open('exams.json', 'r') as f:
            for exam in json.load(f):
                if not Exam.query.filter(Exam.name == exam['name']).first():
                    Exam(name=exam['name']).from_dict(**exam).save()


class ExamType(db.Model, ModelMixin):
    """
    It represents a type of exam like: regular, premium

    """

    __tablename__ = "exam_types"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), unique=True, nullable=False)


class RoleExamType(db.Model, ModelMixin):
    """
    Connection of id exam_types with role id of users
    """

    __tablename__ = "role_exam_types"

    id = db.Column(db.Integer(), primary_key=True)
    exam_type_id = db.Column(
        db.Integer(), db.ForeignKey("exam_types.id", ondelete="CASCADE")
    )
    role_id = db.Column(db.Integer(), db.ForeignKey("roles.id", ondelete="CASCADE"))
