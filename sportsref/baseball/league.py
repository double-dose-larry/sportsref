from .br_page import BRPage
from .util import *

class League():
    
    def __init__(self, league="MLB"):
        self.league = league
        
    def wins(self):
        # get page
        path = f"leagues/{self.league}/"
        page = BRPage(path)
        df = page.get_df("teams_team_wins3000")
        return df
    
    def stats(self, table, stats_type="bat"):
        validate_input(stats_type, ["bat", "pitch", "field", "misc"])
        # get page
        path = f"leagues/{self.league}/{stats_type}.shtml"
        page = BRPage(path)
        validate_input(table, page.tables)
        df = page.get_df(table)
        return df