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
        html = "html"

    class Type(enum.Enum):
        choise = "choise"
        code = "code"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), unique=True, nullable=False)
    lang = db.Column(Enum(Language), default=Language.py)
    exam_type = db.Column(Enum(Type), default=Type.code)
    instruction = db.Column(db.String(1024), nullable=False)
    solution = db.Column(db.String(1024), nullable=True)
    template = db.Column(db.String(1024), nullable=True)
    verification = db.Column(db.String(1024), nullable=True)
    deleted = db.Column(db.Boolean, default=False)
    type_id = db.Column(db.Integer(), db.ForeignKey("exam_levels.id"))
    answer = db.Column(db.String(1024), nullable=True)
    correct_answer = db.Column(db.String(60), nullable=True)
    exam_level = db.relationship("ExamLevel")
    results = db.relationship("Result")

    def __repr__(self):
        return f"<Exam: {self.name}>"

    def to_dict(self):
        return dict(
            name=self.name,
            lang=self.lang.name,
            type=self.exam_type.name,
            instruction=self.instruction.split("\n"),
            solution=self.solution.split("\n"),
            template=self.template.split("\n"),
            exam_level=self.exam_level.name,
            answer=self.answer.split("\n"),
            correct_answer=self.correct_answer.name,
        )

    def from_dict(self, **args):
        self.name = args["name"]
        self.exam_type = args["type"]
        self.lang = Exam.Language[args["lang"]] if "lang" in args else Exam.Language.py
        self.instruction = (
            "\n".join(args["instruction"]) if "instruction" in args else ""
        )
        if self.exam_type == Exam.Type.code.name:
            self.solution = "\n".join(args["solution"]) if "solution" in args else ""
            self.template = "\n".join(args["template"]) if "template" in args else ""
            if "exam_level" in args:
                self.exam_level = ExamLevel.query.filter(
                    ExamLevel.name == args["exam_level"]
                ).first()
            else:
                log(log.ERROR, "Exam [%s] has not type", self.name)
            if "verification" in args:
                self.verification = "\n".join(args["verification"])
        elif self.exam_type == Exam.Type.choise.name:
            self.answer = "\n".join(args["answers"]) if "answers" in args else ""
            self.correct_answer = args["correct_answer"]
            if "exam_level" in args:
                self.exam_level = ExamLevel.query.filter(
                    ExamLevel.name == args["exam_level"]
                ).first()
            else:
                log(log.ERROR, "Exam [%s] has not type", self.name)
        return self

    @staticmethod
    def load_all_exams():
        with open("dev_exams.json", "r") as f:
            for exam in json.load(f):
                if not Exam.query.filter(Exam.name == exam["name"]).first():
                    Exam(name=exam["name"]).from_dict(**exam).save()


class ExamLevel(db.Model, ModelMixin):
    """
    It represents a type of exam like: regular, premium
    """

    __tablename__ = "exam_levels"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), unique=True, nullable=False)


class RoleExamLevel(db.Model, ModelMixin):
    """
    Connection of id exam_levels with role id of users
    """

    __tablename__ = "role_exam_levels"

    id = db.Column(db.Integer(), primary_key=True)
    exam_level_id = db.Column(
        db.Integer(), db.ForeignKey("exam_levels.id", ondelete="CASCADE")
    )
    role_id = db.Column(db.Integer(), db.ForeignKey("roles.id", ondelete="CASCADE"))
