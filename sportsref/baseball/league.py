from .br_page import BaseballPage

class League():
    
    def __init__(self, league="MLB"):
        self.league = league
        
    def wins(self):
        path = f"leagues/{self.league}/"
        return BaseballPage(path)
    
    def batting(self):
        path = f"leagues/{self.league}/bat.shtml"
        return BaseballPage(path)
    
    def pitching(self):
        path = f"leagues/{self.league}/pitch.shtml"
        return BaseballPage(path)
    
    def field(self):
        path = f"leagues/{self.league}/field.shtml"
        return BaseballPage(path)
    
    def misc(self):
        path = f"leagues/{self.league}/misc.shtml"
        return BaseballPage(path)
