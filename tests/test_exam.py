import pytest
from flask import url_for
from app import db, create_app
from app.exam.models import Exam
from app.exam.controller import check_answer, goto_next_exam

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
    all_exams = (
        Exam.query.filter(Exam.lang == Exam.Language.py)
        .filter(Exam.exam_type == Exam.Type.code)
        .all()
    )
    for exam in all_exams:
        assert check_answer(exam, exam.solution), f"Bad solution in [{exam.name}]"


def test_py_exam_sleep_in_code(client):
    exam = (
        Exam.query.filter(Exam.lang == Exam.Language.py)
        .filter(Exam.exam_type == Exam.Type.code)
        .first()
    )
    code_with_sleep = "from time import sleep\nsleep(5)\n"
    code_text = code_with_sleep + exam.solution
    assert not check_answer(exam, code_text), "Test passed with sleep(5)"


def test_goto_next_exam(client):
    res = goto_next_exam(3)
    assert res
    assert "4" in res.location


def test_all_button_presents(client):
    exam = (
        Exam.query.filter(Exam.lang == Exam.Language.py)
        .filter(Exam.exam_type == Exam.Type.code)
        .first()
    )
    res = client.get(url_for("exam.exam_py", exam_id=exam.id))
    assert b">Go<" in res.data
    assert b">&lt;&lt;Prev<" in res.data
    assert b">Next&gt;&gt;<" in res.data
