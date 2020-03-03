from .br_page import BRPage
from .util import *

class League():
    
    def __init__(self, league="MLB"):
        self.league = league
        
    def wins(self):
        path = f"leagues/{self.league}/"
        return BRPage(path)
    
    def batting(self):
        path = f"leagues/{self.league}/bat.shtml"
        return BRPage(path)
    
    def pitching(self):
        path = f"leagues/{self.league}/pitch.shtml"
        return BRPage(path)
    
    def field(self):
        path = f"leagues/{self.league}/field.shtml"
        return BRPage(path)
    
    def misc(self):
        path = f"leagues/{self.league}/misc.shtml"
        return BRPage(path)
