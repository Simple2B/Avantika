import json
from app.logger import log
from .models import Tab

CONFIG_LOCATION = '/home/belenov/simple2b/Avantika/tabs.json'


def get_allowed_tabs(client):
    return tabs


def load_tabs():
    tab_objects = []
    try:
        with open(CONFIG_LOCATION, 'r') as f:
            for tab in json.load(f):
                tab_objects.append(Tab.from_dict(**tab))
    except OSError as ose:
        log(log.ERROR, "OS error: {0}".format(ose))
    except json.JSONDecodeError as jsde:
        log(log.ERROR, "OS error: {0}".format(jsde))

    return tab_objects


tabs = load_tabs()
