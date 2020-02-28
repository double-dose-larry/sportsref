from ..page import Page

class PFRPage(Page):
    "football-reference.com page"
    def __init__(self, path, query_dict={}):
        super().__init__("pfr", path, query_dict)