import pytest
from flask import url_for
from app import db, create_app
from app.tab import load_tabs
from .common import login, logout, register, create_user

app = create_app(environment="testing")
app.config["TESTING"] = True
app.config["SERVER_NAME"] = "localhost.localdomain"

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
        db.drop_all()
        db.create_all()
        create_user(LOGIN_ADMIN, PASSW_ADMIN, ROLE_ADMIN)
        create_user(LOGIN_STUDENT, PASSW_STUDENT, ROLE_STUDENT)
        yield client
        db.session.remove()
        db.drop_all()
        app_ctx.pop()


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
