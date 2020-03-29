from ..page import Page

class ProFootballPage(Page):
    def __init__(self, path, query_dict={}):
        super().__init__("www.pro-football-reference.com", path, query_dict)