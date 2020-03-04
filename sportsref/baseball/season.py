from .br_page import BRPage
from .util import *

class Season():
    
    def __init__(self, year, league="MLB"):
        self.year = year
        self.league = league
        
    def overview(self):
        path = f"leagues/{self.league}/{self.year}.shtml"
        return BRPage(path)
    
    def minor_leagues(self):
        path = "register/league.cgi"
        query_dict = {'year' : self.year}
        return BRPage(path, query_dict)
    
    def standings(self):
        path = f"/leagues/{self.league}/{self.year}-standings.shtml"
        return BRPage(path)
        
    def fielding_pages(self, page=""):
        positions = ["p","c", "1b", "2b", "3b", 
                     "ss", "lf", "rf","cf", "of"]
        validate_input(page, ["standard-fielding", "appearances"] + positions)
        if page in positions:
            page = f"specialpos_{page}"
        path = f"leagues/{self.league}/{self.year}-{page}-fielding.shtml"
        return BRPage(path)
    
    def batting_pages(self, page=""):
        query_pages = ["compare", "splits", "minors", "yesterday"]
        validate_input(page, ["standard", "value", "advanced","win_probability",
                              "ratio", "baserunning", "situational", "pitches",
                              "cumulative", "neutral"] + query_pages)
        if page in query_pages:
            path, query_dict = {
                'compare' : ("leagues/team_compare.cgi", {'lg' : self.league, 'year' : self.year}),
                'splits' : ("leagues/split.cgi", {'lg' : self.league, 'year' : self.year}),
                'minors' : ("register/leader.cgi", {'type' : "bat", 'year' : self.year}),
                'yesterday': ("leagues/daily.fcgi", {'type' : "b"})
            }.get(page)
            return BRPage(path, query_dict)
        else:
            path = f"leagues/{self.league}/{self.year}-{page}-batting.shtml"
            return BRPage(path)
        
    def pitching_pages(self, page=""):
        query_pages = ["splits", "minors", "yesterday"]
        validate_input(page, ["standard", "value", "batting", "win_probability",
                              "starter", "reliever", "ratio", "pitches",
                              "basesituation", "cumulative", "neutral"] + query_pages)
        if page in query_pages:
            path, query_dict = {
                'splits' : ("leagues/split.cgi", {'t' : "p", 'lg' : self.league, 'year' : self.year}),
                'minors' : ("register/leader.cgi", {'type' : "pitch", 'year' : self.year}),
                'yesterday': ("leagues/daily.fcgi", {'type' : "p"})
            }.get(page)
            return BRPage(path, query_dict)
        else:
            path = f"leagues/{self.league}/{self.year}-{page}-pitching.shtml"
            return BRPage(path)
        
    def managers(self):
        path = f"leagues/{self.league}/{self.year}-managers.shtml"
        return BRPage(path)
    
    def other_pages(self, page=""):
        query_pages = ["draft", "last_n_day_leaders"]
        validate_input(page, ["misc", "debuts", "rookies", "finalyear", "births",
                              "deaths", "transactions", "free-agents", "opening-day-rosters",
                              "team-starting-lineups", "team-pitching-staffs",
                              "projections", "playoff-odds"] + query_pages)
        if page in query_pages:
            path, query_dict = {
                'draft' : ("draft/" ,
                           {'draft_type' : "junreg",
                            'query_type' : 'year_round',
                            'draft_round' : 1,
                            'year_ID' : self.year}),
                'last_n_day_leaders' : ("leagues/daily.fcgi",
                                       {'type' : "b",
                                        'dates' : "lastndays",
                                        'lastndays': 21})
            }.get(page)
            return BRPage(path, query_dict)
        else:
            path = f"leagues/{self.league}/{self.year}-{page}.shtml"
            return BRPage(path)