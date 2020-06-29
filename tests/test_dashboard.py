import pytest
from enum import Enum
from flask import url_for
from app import db, create_app
from app.auth.models import User, Role, UserRoles
from .test_app import login, logout

app = create_app(environment="testing")
app.config["TESTING"] = True
app.config["SERVER_NAME"] = "localhost"


class Admin(Enum):
    LOGIN = "admin"
    PASSW = "admin"
    ROLE = "Admin"


class Student(Enum):
    LOGIN = "student"
    PASSW = "student"
    ROLE = "Student_PI_reg"


class Test(Enum):
    LOGIN = "test"
    PASSW = "test"
    ROLE = "Student_PA_prem"


class NewUser(Enum):
    LOGIN = "test"
    PASSW = "test"
    ROLE = "Student_J_pre"


USER_TEST_IDS = None

CORRECT_ID = 1


@pytest.fixture
def client():
    try:
        with app.test_client() as client:
            app_ctx = app.app_context()
            app_ctx.push()
            db.create_all()
            create_user(Admin.LOGIN.value, Admin.PASSW.value, Admin.ROLE.value)
            create_user(Student.LOGIN.value, Student.PASSW.value, Student.ROLE.value)
            USER_TEST_IDS = create_user(Test.LOGIN.value, Test.PASSW.value, Test.ROLE.value)  # noqa
            yield client
    finally:
        db.session.remove()
        db.drop_all()
        app_ctx.pop()


# open dashboard form
def test_index(client):
    # not logged -> redirect
    logout(client)
    response = client.get(url_for("dashboard.index"))
    assert response.status_code == 302
    assert response.location == url_for("main.index")
    # if logged, not admin -> redirect
    login(client, Student.LOGIN.value, Student.PASSW.value)
    response = client.get(url_for("dashboard.index"))
    assert response.status_code == 302
    assert response.location == url_for("main.index")
    logout(client)
    # if logged as admin -> OK
    login(client, Admin.LOGIN.value, Admin.PASSW.value)
    response = client.get(url_for("dashboard.index"))
    assert response.status_code == 200
    logout(client)


# open add client form
def test_user_add(client):
    # not logged -> redirect
    logout(client)
    response = client.get(url_for("dashboard.user_add"))
    assert response.status_code == 302
    assert response.location == url_for("main.index")
    # if logged, not admin -> redirect
    login(client, Student.LOGIN.value, Student.PASSW.value)
    response = client.get(url_for("dashboard.user_add"))
    assert response.status_code == 302
    assert response.location == url_for("main.index")
    logout(client)
    # if logged as admin -> OK
    login(client, Admin.LOGIN.value, Admin.PASSW.value)
    response = client.get(url_for("dashboard.user_add"))
    assert response.status_code == 200
    logout(client)


# open update client form
def test_user_update(client):
    # not logged -> redirect
    logout(client)
    response = client.get(url_for("dashboard.user_update", CORRECT_ID))
    assert response.status_code == 302
    assert response.location == url_for("main.index")
    # if logged, not admin -> redirect
    login(client, Student.LOGIN.value, Student.PASSW.value)
    response = client.get(url_for("dashboard.user_update", CORRECT_ID))
    assert response.status_code == 302
    assert response.location == url_for("main.index")
    logout(client)
    # if logged as admin -> OK
    login(client, Admin.LOGIN.value, Admin.PASSW.value)
    response = client.get(url_for("dashboard.user_update", USER_TEST_IDS["user_id"]))
    assert response.status_code == 200
    logout(client)


# save new client button
def test_user_save_new(client):
    # not logged -> redirect
    logout(client)
    response = client.post(
        url_for("dashboard.user_save_new"),
        data=dict(
            name=NewUser.LOGIN.value,
            password=NewUser.PASSW.value,
            role_name=NewUser.ROLE.value
        )
    )
    assert response.status_code == 302
    assert response.location == url_for("main.index")
    # if logged, not admin -> redirect
    login(client, Student.LOGIN.value, Student.PASSW.value)
    response = client.post(
        url_for("dashboard.user_save_new"),
        data=dict(
            name=NewUser.LOGIN.value,
            password=NewUser.PASSW.value,
            role_name=NewUser.ROLE.value
        )
    )
    assert response.status_code == 302
    assert response.location == url_for("main.index")
    logout(client)
    # already in db
    login(client, Admin.LOGIN.value, Admin.PASSW.value)
    response = client.post(
        url_for("dashboard.user_save_new"),
        data=dict(
            name=Test.LOGIN.value,
            password=Test.PASSW.value,
            role_id=Test.ROLE.value
        )
    )
    assert response.status_code == 302
    assert response.location == url_for("dashboard.index")
    logout(client)
    # if logged as admin -> OK
    login(client, Admin.LOGIN.value, Admin.PASSW.value)
    response = client.post(
        url_for("dashboard.user_save_new"),
        data=dict(
            name=NewUser.LOGIN.value,
            password=NewUser.PASSW.value,
            role_name=NewUser.ROLE.value
        )
    )
    assert response.status_code == 200
    logout(client)


# save update client button
def test_user_save_update(client):
    # not logged -> redirect
    logout(client)
    response = client.post(
        url_for("dashboard.user_save_update"),
        data=dict(
            id=USER_TEST_IDS["user_id"],
            name=Test.LOGIN.value + "New",  # updated name
            password=Test.PASSW.value,
            role_id=Test.ROLE.value
        )
    )
    assert response.status_code == 302
    assert response.location == url_for("main.index")
    # if logged, not admin -> redirect
    login(client, Student.LOGIN.value, Student.PASSW.value)
    response = client.post(
        url_for("dashboard.user_save_update"),
        data=dict(
            id=USER_TEST_IDS["user_id"],
            name=Test.LOGIN.value + "New",  # updated name
            password=Test.PASSW.value,
            role_id=Test.ROLE.value
        )
    )
    assert response.status_code == 302
    assert response.location == url_for("main.index")
    logout(client)
    # already in db with the same name
    login(client, Admin.LOGIN.value, Admin.PASSW.value)
    response = client.post(
        url_for("dashboard.user_save_update"),
        data=dict(
            id=USER_TEST_IDS["user_id"],
            name=Student.LOGIN.value,
            password=Test.PASSW.value,
            role_id=Test.ROLE.value
        )
    )

    # if logged as admin -> OK
    login(client, Admin.LOGIN.value, Admin.PASSW.value)
    response = client.post(url_for("dashboard.user_save_update", data={}))
    assert response.status_code == 200
    logout(client)


def test_user_delete(client):
    # not logged -> redirect
    logout(client)
    response = client.get(url_for("dashboard.user_delete", id=CORRECT_ID))
    assert response.status_code == 302
    assert response.location == url_for("main.index")
    # if logged, not admin -> redirect
    login(client, Student.LOGIN.value, Student.PASSW.value)
    response = client.get(url_for("dashboard.user_delete", id=CORRECT_ID))
    assert response.status_code == 302
    assert response.location == url_for("main.index")
    logout(client)
    # if logged as admin -> OK
    login(client, Admin.LOGIN.value, Admin.PASSW.value)
    response = client.get(url_for("dashboard.user_delete", id=USER_TEST_IDS["user_id"]))
    assert response.status_code == 302
    assert response.location == url_for("dashboard.index")


def create_user(username, password, role_name):
    user = User(username=username)
    user.password = password
    user.save()
    user_role = Role(name=role_name)
    user_role.save()
    join_user_to_role = UserRoles(user_id=user.id, role_id=user_role.id)
    join_user_to_role.save()
    return {
        "user_id": user.id,
        "role_id": user_role.id,
        "user_roles_id": join_user_to_role.id,
    }
