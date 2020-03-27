from ..page import Page

class BRPage(Page):
    "baseball-reference.com page"
    def __init__(self, path, query_dict={}, verbose=True):
        super().__init__("www.baseball-reference.com", path, query_dict, verbose)