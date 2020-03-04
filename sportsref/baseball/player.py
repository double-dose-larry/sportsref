from .br_page import BRPage
from .util import *

all_player_df = get_players()

class Player():
    
    def __init__(self, fuzzy_name, verbose=True):
        p = get_player_info(fuzzy_name, all_player_df, verbose=verbose)
        self.key = p.key
        self.name = p["name"]
        self.first_year = int(p.years[:4])
        self.last_year = int(p.years[-4:])
        self.is_active = p.is_active == 1
        self.years_active = list(range(self.first_year, self.last_year + 1))

    def __repr__(self):
        actv = 'active' if self.is_active else 'not active'
        return f"< {self.name}, {self.first_year} - {self.last_year}, {actv} >"
    
    def _pit_or_bat(self):
        df = self.overview().sum()
        return "p" if df.P / df.G > 0.5 else "b"
        
    def overview(self):
        path = f"players/{self.key[0]}/{self.key}.shtml"
        return BRPage(path)
    
    def splits_pages(self, year="", split_type=""):
        validate_input(split_type, ["b", "p"])
        validate_input(year, self.years_active + ["career"])
        path = "players/split.fcgi"
        query_dict = {
                'year' : year,
                'id' : self.key,
                't' : split_type
            }
        return BRPage(path, query_dict)
    
    def game_logs_pages(self, year="", log_type=""):
        validate_input(year, self.years_active + ["career", "post"])
        validate_input(log_type, ["b","p","f"])
        path = "/players/gl.fcgi"
        query_dict = {
            'id': self.key,
            't' : log_type,
            'year' : year,
            'post' : 1 if year == "post" else 0
        }
        return BRPage(path, query_dict)
    
    def advanced_pages(self, page=""):
        query_pages = ["hr_log",  "vs_pitcher", "vs_batter"]
        validate_input(page, ['bat', 'pitch', 'field'] + query_pages)
        
        if page in query_pages:
            path, query_dict = {
                'hr_log' : ("players/event_hr.fcgi", {
                    'id' : self.key,
                    't' : adv_type[0]}),
                'vs_pitcher' : ("play-index/batter_vs_pitcher.cgi", 
                                {'batter' : self.key}),
                'vs_batter' : ("play-index/batter_vs_pitcher.cgi", 
                               {'pitcher' : self.key})
            }
            return BRPage(path, query_dict)
        else:
            path = f"players/{self.key[0]}/{self.key}-{page}.shtml"
            return BRPage(path)