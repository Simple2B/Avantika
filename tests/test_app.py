import pytest
import os
from app import db, create_app
from app.models import User
from app.tab import load_tabs


app = create_app(environment="testing")
app.config["TESTING"] = True


@pytest.fixture
def client():
    with app.test_client() as client:
        app_ctx = app.app_context()
        app_ctx.push()
        db.create_all()
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


def test_registration_page(client):
    response = client.get("/register")
    assert response.status_code == 200


def test_login_page(client):
    response = client.get("/login")
    assert response.status_code == 200


# def test_registration(client):
#     # Valid data should register successfully.
#     assert register("alice")
#     # Password/Confirmation mismatch should fail.
#     response = register("alice")
#     assert b"The given data was invalid." in response.data


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


def test_load_tabs(client):
    # wrong config path --> empty array
    tabs = load_tabs()
    assert len(tabs) == 0
    delete_json()
    # invalid json --> empty array
    create_invalid_json()
    tabs = load_tabs()
    assert len(tabs) == 0
    delete_json()
    # correct --> array of definite length
    create_valid_json()
    tabs = load_tabs()
    assert len(tabs) == 4
    delete_json()


def test_get_allowed_tabs(client):
    # unlogged user

    # logged user#1 --> definite tabs

    # logged user 2  --> other tabs
    pass


def create_valid_json():
    json_str = """[{
        "href": "exam.exam",
        "name": "Admin Dashboard",
        "roles": [
            "Admin"
        ]
    },
    {
        "href": "exam.exam",
        "name": "Python Basic",
        "roles": [
            "Admin",
            "Student_PB_reg",
            "Student_PB_prem",
            "Student_PB_prem_outsider",
            "Student_PI_reg",
            "Student_PI_prem",
            "Student_PI_prem_outsider",
            "Student_PA_reg",
            "Student_PA_prem",
            "Student_PA_prem_outsider"
        ]
    },
    {
        "href": "exam.exam",
        "name": "Python Intermediate",
        "roles": [
            "Admin",
            "Student_PI_reg",
            "Student_PI_prem",
            "Student_PI_prem_outsider",
            "Student_PA_reg",
            "Student_PA_prem",
            "Student_PA_prem_outsider"
        ]
    },
    {
        "href": "exam.exam",
        "name": "Python Advanced",
        "roles": [
            "Admin",
            "Student_PA_reg",
            "Student_PA_prem",
            "Student_PA_prem_outsider"
        ]
    }
    ]
    """
    with open("tabs.json", "w+") as f:
        f.writelines(json_str)


def create_invalid_json():
    json_str = """[{
        "href": "exam.exam",
        "name": "Admin Dashboard",
        "roles": [
            "Admin"
        ]
    },
    {
        "href": "exam.exam",
        "name": "Python Basic",
        "roles": [
            "Admin",
            "Student_PB_reg",
            "Student_PB_prem",
            "Student_PB_prem_outsider",
            "Student_PI_reg",
            "Student_PI_prem",
            "Student_PI_prem_outsider",
            "Student_PA_reg",
            "Student_PA_prem",
            "Student_PA_prem_outsider"
        ]
    },
    {
        "href": "exam.exam",
        "name": "Python Intermediate",
        "roles": [
            "Admin",
            "Student_PI_reg",
            "Student_PI_prem",
            "Student_PI_prem_outsider",
            "Student_PA_reg",
            "Student_PA_prem",
            "Student_PA_prem_outsider"
        ]
    },
    {
        "href": "exam.exam",
        "name": "Python Advanced",
        "roles": [
            "Admin",
            "Student_PA_reg",
            "Student_PA_prem",
            "Student_PA_prem_outsider"
        ]
    },
    ]
    """
    with open("tabs.json", "w+") as f:
        f.writelines(json_str)


def delete_json():
    if os.path.exists("tabs.json"):
        os.remove("tabs.json")
