from .br_page import BRPage
from .util import *

class Season():
    
    def __init__(self, year, league="MLB"):
        self.year = year
        self.league = league
        
    def overview(self, table):
        path = f"leagues/{self.league}/{self.year}.shtml"
        page = BRPage(path)
        validate_input(table, page.tables)
        df = page.get_df(table)
        return df
    
    def standings(self, table):
        path = f"/leagues/{self.league}/{self.year}-standings.shtml"
        page = BRPage(path)
        validate_input(table, page.tables)
        df = page.get_df(table)
        return df
        
    def standard_stats(self, table = "", stat_type = "batting"):
        validate_input(stat_type, ["batting", "pitching", "fielding"])
        path = f"leagues/{self.league}/{self.year}-standard-{stat_type}.shtml"
        page = BRPage(path)
        validate_input(table, page.tables)
        df = page.get_df(table)
        return df
    
    def spring_tr(self, table=""):
        path = f"leagues/{self.league}/{self.year}-spring-training-batting.shtml"
        page = BRPage(path)
        validate_input(table, page.tables)
        df = page.get_df(table)
        return df