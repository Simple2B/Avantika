import json
from .models import Tab

CONFIG_LOCATION = '/home/belenov/simple2b/Avantika/tabs.json'


def get_allowed_tabs(client):
    return tabs


def load_tabs():
    tab_objects = []
    with open(CONFIG_LOCATION, 'r') as f:
        for tab in json.load(f):
            tab_objects.append(Tab.from_dict(**tab))
    return tab_objects


tabs = load_tabs()
