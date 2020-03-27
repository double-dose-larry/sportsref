from ..page import Page

class PFRPage(Page):
    "football-reference.com page"
    def __init__(self, path, query_dict={}):
        super().__init__("www.pro-football-reference.com", path, query_dict)