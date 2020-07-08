import pytest
from flask import url_for
from app import db, create_app
from .test_app import login, logout, create_user

app = create_app(environment="testing")
app.config["TESTING"] = True
app.config["SERVER_NAME"] = "localhost.localdomain"


class Admin:
    LOGIN = "admin"
    PASSW = "admin"
    ROLE = "Admin"


class Student:
    LOGIN = "student"
    PASSW = "student"
    ROLE = "Student_PI_reg"


class Test:
    LOGIN = "test"
    PASSW = "test"
    ROLE = "Student_PA_prem"


class NewUser:
    LOGIN = "test"
    PASSW = "test"
    ROLE = "Student_J_pre"


USER_TEST_IDS = None

CORRECT_ID = 1


@pytest.fixture
def client():
    with app.test_client() as client:
        app_ctx = app.app_context()
        app_ctx.push()
        db.drop_all()
        db.create_all()
        create_user(Admin.LOGIN, Admin.PASSW, Admin.ROLE)
        create_user(Student.LOGIN, Student.PASSW, Student.ROLE)
        USER_TEST_IDS = create_user(Test.LOGIN, Test.PASSW, Test.ROLE)  # noqa
        yield client
        db.session.remove()
        db.drop_all()
        app_ctx.pop()


# open dashboard form
def test_index(client):
    # not logged -> redirect
    logout(client)
    response = client.get(url_for("dashboard.index"))
    assert response.status_code == 302
    # assert response.location == url_for("main.index")
    # if logged, not admin -> redirect
    login(client, Student.LOGIN, Student.PASSW)
    response = client.get(url_for("dashboard.index"))
    assert response.status_code == 302
    # assert response.location == url_for("main.index")
    logout(client)
    # if logged as admin -> OK
    login(client, Admin.LOGIN, Admin.PASSW)
    response = client.get(url_for("dashboard.index"))
    assert response.status_code == 200


def test_delete_user(client):
    login(client, Admin.LOGIN, Admin.PASSW)
    respose = client.get(url_for("auth.delete_user", user_id=56))
    assert respose.status_code == 200
