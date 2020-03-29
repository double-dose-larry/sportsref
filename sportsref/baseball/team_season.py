from .br_page import BaseballPage
from ..util import *
from .team_abbr_parser import TeamAbbrParser

class TeamSeason():
    
    def __init__(self, fran, year):
        self.franchise = fran
        self.year = year
        self.abbr = TeamAbbrParser(f"https://www.baseball-reference.com/teams/{fran.abbr}/").team_year_abbr_map[year]
        
    def __repr__(self):
        return f"< {self.abbr}, year {self.year} >"  
    
    def stats(self, table="team_batting"):
        path = f"teams/{self.abbr}/{self.year}.shtml"
        return BaseballPage(path)
    
    def schedule_results(self):
        path = f"teams/{self.abbr}/{self.year}-schedule-scores.shtml"
        return BaseballPage(path)
    
    def roster(self):
        path = f"teams/{self.abbr}/{self.year}-roster.shtml"
        
    def batting_pages(self, page=""):
        query_pages = ["game_logs", "splits"]
        validate_input(page, ["detailed"] + query_pages)
        
        if page in query_pages:
            path, query_dict = {
                'game_logs' : ("teams/tgl.cgi", {
                    'team' : self.abbr,
                    't': "b",
                    'year': self.year
                }),
                'splits' : ("teams/splt.cgi", {
                    'team' : self.abbr,
                    't' : "b",
                    'year' : self.year
                })
            }.get(page)
            return BaseballPage(path, query_dict)
        else:
            path = f"teams/{self.abbr}/{self.year}-batting.shtml"
            return BaseballPage(path)
        
    def pitching_pages(self, page=""):
        query_pages = ["game_logs", "splits"]
        validate_input(page, ["detailed"] + query_pages)
        
        if page in query_pages:
            path, query_dict = {
                'game_logs' : ("teams/tgl.cgi", {
                    'team' : self.abbr,
                    't': "p",
                    'year': self.year
                }),
                'splits' : ("teams/splt.cgi", {
                    'team' : self.abbr,
                    't' : "p",
                    'year' : self.year
                })
            }.get(page)
            return BaseballPage(path, query_dict)
        else:
            path = f"teams/{self.abbr}/{self.year}-pitching.shtml"
            return BaseballPage(path)
        
    def fielding(self):
        path = f"teams/{self.abbr}/{self.year}-fielding.shtml"
        return BaseballPage(path)
    
    def scoring(self):
        path = "play-index/inning_summary.cgi"
        query_dict = {
            'year' : self.year,
            'team_id' : self.abbr
        }
        return BaseballPage(path, query_dict)
    
    def other_pages(self, page=""):
        validate_input(page, ["lineups", "batting-orders"])
        path = f"teams/{self.abbr}/{self.year}-{page}.shtml"
        return BaseballPage(path)
    