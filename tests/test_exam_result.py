import pytest
from app import db, create_app
from app.exam.models import Exam

from app.result.models import Result

# from app.auth.models import User
from app.result.controller import go_pass_exam, next_to_pass_exam


app = create_app(environment="testing")
app.config["TESTING"] = True
app.config["SERVER_NAME"] = "localhost.localdomain"


@pytest.fixture
def client():
    with app.test_client() as client:
        app_ctx = app.app_context()
        app_ctx.push()
        db.drop_all()
        db.create_all()
        Exam.load_all_exams()
        yield client
        db.session.remove()
        db.drop_all()
        app_ctx.pop()


def test_result_exam_passed_go(client):
    exam_id = 1
    user_id = 1
    go_pass_exam(exam_id, user_id)
    the_passed = Result.query.filter(
        exam_id == Result.exam_id, user_id == Result.user_id
    ).first()
    assert the_passed.passed


def test_result_exam_passed_next(client):
    exam_id = 1
    user_id = 1
    next_to_pass_exam(exam_id, user_id)
    the_passed = Result.query.filter(
        exam_id == Result.exam_id, user_id == Result.user_id
    ).first()
    assert not the_passed.passed
