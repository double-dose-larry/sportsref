from ..page import Page

class BRPage(Page):
    "baseball-reference.com page"
    def __init__(self, path, query_dict={}):
        super().__init__("br", path, query_dict)