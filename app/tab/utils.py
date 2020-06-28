import json
import os
from flask_login import current_user

from app.logger import log
from .models import Tab

CONFIG_TABS = "tabs.json"


def get_allowed_tabs():
    # logic to filter tabs by client's roles
    user_role = current_user.roles[0].name if not current_user.is_anonymous else []
    client_tabs = []
    for tab in tabs:
        if user_role in tab.roles:
            client_tabs.append(tab)
    return client_tabs


def load_tabs():
    config_path = os.path.abspath(CONFIG_TABS)
    log(log.INFO, "Tabs config file path: {}".format(config_path))
    tab_objects = []
    try:
        with open(config_path, "r") as f:
            for tab in json.load(f):
                tab_objects.append(Tab.from_dict(**tab))
    except OSError as ose:
        log(log.ERROR, "OS error: {0}".format(ose))
    except json.JSONDecodeError as jsde:
        log(log.ERROR, "JSON decode error: {0}".format(jsde))

    return tab_objects


tabs = load_tabs()
