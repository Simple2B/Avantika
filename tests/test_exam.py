import pytest
from app import db, create_app
from app.exam.models import Exam
from app.exam.controller import check_answer, goto_next_exam, check_answer_choise


app = create_app(environment="testing")
app.config["TESTING"] = True
app.config["SERVER_NAME"] = "localhost.localdomain"


@pytest.fixture
def client():
    with app.test_client() as client:
        app_ctx = app.app_context()
        app_ctx.push()
        db.create_all()
        Exam.load_all_exams()
        yield client
        db.session.remove()
        db.drop_all()
        app_ctx.pop()


def test_py_exam_check_answer(client):
    for exam in Exam.query.filter(Exam.lang == Exam.Language.py).all():
        assert check_answer(exam, exam.solution), f"Bad solution in [{exam.name}]"


def test_goto_next_exam(client):
    res = goto_next_exam(3)
    assert res
    assert "4" in res.location


def test_check_answer_choise(client):
    exam = Exam.query.all()[18]
    check_answer_choise(exam, 2)
    return 1
