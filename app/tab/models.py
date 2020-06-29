
class Tab(object):
    '''
    It represents a tab displayed on UI
    '''

    def __init__(self, name="", href="", roles=list()):
        self.name = name
        self.href = href
        self.roles = roles

    @classmethod
    def from_dict(cls, **args):
        name = args["name"]
        href = args["href"]
        roles = args["roles"]
        return cls(name, href, roles)
