import os
import pytest
from typing import List, AnyStr
from app.tab.utils import load_tabs

TABS_CONFIG = "tabs.json"
BACKUP_TABS_CONFIG = "backup_tabs.json"


@pytest.fixture
def client():
    # create backup of a tabs.json: tabs.json --> backup_tabs.json
    backup()
    yield None
    # recover from backup: backup_tabs.json --> tabs.json
    recover()


def test_load_tabs(client):
    # wrong config path --> empty array
    delete_json(TABS_CONFIG)
    tabs = load_tabs()
    assert not tabs
    delete_json(TABS_CONFIG)
    # invalid json --> empty array
    create_invalid_json()
    tabs = load_tabs()
    assert len(tabs) == 0
    delete_json(TABS_CONFIG)
    # correct --> array of definite length
    create_valid_json()
    tabs = load_tabs()
    assert len(tabs) == 4
    delete_json(TABS_CONFIG)


def create_valid_json():
    json_str = """[{
        "href": "/dashboard",
        "name": "Admin Dashboard",
        "roles": [
            "Admin"
        ]
    },
    {
        "href": "/exam_lang/py",
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
        "href": "/exam_lang/py",
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
        "href": "/exam_lang/py",
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
    write_file(TABS_CONFIG, json_str)


def create_invalid_json():
    json_str = """[{
        "href": "/dashboard",
        "name": "Admin Dashboard",
        "roles": [
            "Admin"
        ]
    },
    {
        "href": "/exam_lang/py",
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
        "href": "/exam_lang/py",
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
        "href": "/exam_lang/py",
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
    write_file(TABS_CONFIG, json_str)


def delete_json(file_name):
    if os.path.exists(file_name):
        os.remove(file_name)


def backup():
    data = read_file(TABS_CONFIG)
    write_file(BACKUP_TABS_CONFIG, data)


def recover():
    data = read_file(BACKUP_TABS_CONFIG)
    write_file(TABS_CONFIG, data)
    delete_json(BACKUP_TABS_CONFIG)


def write_file(name, lines):
    abs_path = os.path.abspath(name)
    with open(abs_path, "w") as f:
        f.writelines(lines)


def read_file(name) -> List[AnyStr]:
    abs_path = os.path.abspath(name)
    with open(abs_path, "r") as f:
        lines = f.readlines()
    return lines
