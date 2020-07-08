import pytest
from flask import url_for
from app import db, create_app
from tests.test_app import create_user, login

LOGIN_ADMIN = "admin"
PASSW_ADMIN = "admin"
ROLE_ADMIN = "Admin"

LOGIN_STUDENT = "student124"
PASSW_STUDENT = "student"
ROLE_STUDENT = "student_PI_reg"

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
        create_user(LOGIN_ADMIN, PASSW_ADMIN, ROLE_ADMIN)
        # create_user(LOGIN_STUDENT, PASSW_STUDENT, ROLE_STUDENT)
        yield client
        db.session.remove()
        db.drop_all()
        app_ctx.pop()


def test_registration_page(client):
    response = client.get(url_for("auth.register"))
    assert response.status_code == 302
    login(client, LOGIN_ADMIN, PASSW_ADMIN)
    response = client.get(url_for("auth.register"))
    assert response.status_code == 200


def test_registration(client):
    # Valid data should register successfully.
    response = client.post(
        url_for("auth.register"),
        data=dict(
            username=LOGIN_STUDENT,
            password=PASSW_STUDENT,
            active="Active",
            role=ROLE_STUDENT,
        ),
    )
    assert response.status_code == 302
    login(client, LOGIN_ADMIN, PASSW_ADMIN)
    response = client.post(
        url_for("auth.register"),
        data=dict(
            username=LOGIN_STUDENT,
            password=PASSW_STUDENT,
            password_confirmation=PASSW_STUDENT,
            active="Active",
            role=ROLE_STUDENT,
        ),
    )
    assert response.status_code == 200

    # response = client.get(url_for("dashboard.index"))
    # # assert b"Registration successful." in response.data
    # user = User.query.filter(User.username == LOGIN_STUDENT).first()
    # assert user
    # assert user.active
    # assert ROLE_STUDENT in [role.name for role in user.roles]
