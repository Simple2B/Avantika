import json
import os
from flask_login import current_user

from app.logger import log
from .models import Tab

CONFIG_TABS = "tabs.json"


def get_allowed_tabs():
    """
    It gets tabs to be displayed on UI looking up the current user's roles.
    It returns an empty or fulfilled array of app.tab.models.Tab.
    """

    user_roles = current_user.roles if not current_user.is_anonymous else []
    if len(user_roles) > 0:
        user_role = user_roles[0].name
    else:
        return []

    client_tabs = []
    for tab in tabs:
        if user_role in tab.roles:
            client_tabs.append(tab)
    return client_tabs


def load_tabs():
    """
    It loads a config tabs.json and parses it to an array of app.tab.models.Tab.
    The config tabs.json have to be near the app module.
    """

    config_path = os.path.abspath(CONFIG_TABS)
    log(log.INFO, "Tabs config file path: {}".format(config_path))
    tab_objects = []
    try:
        with open(config_path, "r") as f:
            for tab in json.load(f):
                if "disabled" in tab:
                    continue
                tab_objects.append(Tab.from_dict(**tab))
    except OSError as ose:
        log(log.ERROR, "OS error: {}".format(ose))
    except json.JSONDecodeError as jsde:
        log(log.ERROR, "JSON decode error: {}".format(jsde))

    return tab_objects


tabs = load_tabs()
