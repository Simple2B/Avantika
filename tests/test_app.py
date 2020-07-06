import pytest
from flask import url_for
from app import db, create_app
from app.tab import load_tabs
from app.auth.models import User, Role, UserRoles

app = create_app(environment="testing")
app.config["TESTING"] = True
app.config["SERVER_NAME"] = "localhost"

LOGIN_ADMIN = "admin"
PASSW_ADMIN = "admin"
ROLE_ADMIN = "Admin"

LOGIN_STUDENT = "student"
PASSW_STUDENT = "student"
ROLE_STUDENT = "Student_PI_reg"


@pytest.fixture
def client():
    with app.test_client() as client:
        app_ctx = app.app_context()
        app_ctx.push()
        db.create_all()
        create_user(LOGIN_ADMIN, PASSW_ADMIN, ROLE_ADMIN)
        create_user(LOGIN_STUDENT, PASSW_STUDENT, ROLE_STUDENT)
        yield client
        db.session.remove()
        db.drop_all()
        app_ctx.pop()


def register(user_name, password="password"):
    # noinspection PyArgumentList
    user = User(username=user_name, password=password)
    user.save()
    return user.id


def login(client, user_id, password="password"):
    return client.post(
        "/login", data=dict(user_id=user_id, password=password), follow_redirects=True,
    )


def logout(client):
    return client.get("/logout", follow_redirects=True)


def test_index_page(client):
    response = client.get("/")
    assert response.status_code == 200


def test_login_page(client):
    response = client.get("/login")
    assert response.status_code == 200


def test_login_and_logout(client):
    # Access to logout view before login should fail.
    response = logout(client)
    assert b"Please log in to access this page." in response.data
    # New user will be automatically logged in.
    register("sam")
    login(client, "sam")
    # Should successfully logout the currently logged in user.
    response = logout(client)
    assert b"You were logged out." in response.data
    # Incorrect login credentials should fail.
    response = login(client, "sam@example.com")
    assert b"Wrong user ID or password." in response.data
    # Correct credentials should login
    response = login(client, "sam")
    assert b"Login successful." in response.data


def test_get_tabs_not_logged(client):
    logout(client)
    url = url_for("main.index")
    response = client.get(url)
    tabs = load_tabs()
    for tab in tabs:
        assert f"{tab.name}".encode("utf-8") not in response.data


def test_get_tabs_admin(client):
    login(client, LOGIN_ADMIN, PASSW_ADMIN)
    url = url_for("main.index")
    response = client.get(url)
    logout(client)
    tabs = load_tabs()
    for tab in tabs:
        assert f"{tab.name}".encode("utf-8") in response.data


def test_get_tabs_user(client):
    login(client, LOGIN_STUDENT, PASSW_STUDENT)
    # get datan
    url = url_for("main.index")
    response = client.get(url)
    logout(client)
    tabs = load_tabs()
    allowed_tabs = [tab for tab in tabs if ROLE_STUDENT in tab.roles]
    restricted_tabs = [tab for tab in tabs if ROLE_STUDENT not in tab.roles]
    for a_tab in allowed_tabs:
        assert f"{a_tab.name}".encode("utf-8") in response.data
    for r_tab in restricted_tabs:
        assert f"{r_tab.name}".encode("utf-8") not in response.data


def create_user(username, password, role_name):
    admin = User(username=username)
    admin.password = password
    admin.save()
    admin_role = Role(name=role_name)
    admin_role.save()
    join_admin_to_role = UserRoles(user_id=admin.id, role_id=admin_role.id)
    join_admin_to_role.save()
