from .br_page import BRPage
from .util import *
from .team_season import TeamSeason

all_fran_df = get_frans()

class Franchise():
    
    def __init__(self, fuzzy_fran):
        f = get_fran_info(all_fran_df, fuzzy_fran)
        self.abbr = f.abbr
        self.name = f.name
        self.first_year = int(f.years[:4])
        self.last_year = int(f.years[-4:])
        self.years_active = list(range(self.first_year, self.last_year + 1))
        
    def __repr__(self):
        return f"< {self.name}, {self.first_year} - {self.last_year} >"
    
    def hist(self, table="franchise_years"):
        # get page
        path = f"teams/{self.abbr}"
        hist_page = BRPage(path)
        #validate
        validate_input(table, hist_page.tables)
        # clean
        df = hist_page.get_df(table).query('Tm != "Overall"')
        df = numberize_df(df)
        return df
    
    def season(self, year):
        # validate
        validate_input(year, self.years_active)
        return TeamSeason(self, year)
    
    def batters(self):
        """all batters to play for the franchise """
        # get page
        path = f"teams/{self.abbr}/bat.shtml"
        page = BRPage(path)
        # clean df
        df = page.get_df("batting_register").query("Name != 'Name'")
        df = numberize_df(df)
        return df
    
    def pitchers(self):
        """all batters to play for the franchise"""
        path = f"teams/{self.abbr}/pitch.shtml"
        page = BRPage(path)
        # clean df
        df = page.get_df("pitching_register").query("Name != 'Name'")
        df = numberize_df(df)
        return df
    
    def draft(self, year):
        """get draft for each round of a year."""
        # get page
        path = "/draft"
        query_dict = {
            'team': self.abbr,
            'year_ID': year,
            'draft_type' : 'junreg',
            'query_type' : 'franch_year',
            'from_type_jc' : 0,
            'from_type_hs' : 0,
            'from_type_4y' : 0,
            'from_type_unk' : 0
        }
        page = BRPage(path, query_dict)
        # clean
        df = page.get_df("draft_stats")
        df = numberize_df(df)
        return df
    
    def parks(self):
        """get parks and attendance numbers by year"""
        # get page
        path = f'teams/{self.abbr}/attend.shtml'
        page = BRPage(path)
        df = page.get_df("franchise_years")
        df = numberize_df(df)
        return df
    
    def year_by_year(self, table, pit_or_bat="bat"):
        validate_input(pit_or_bat, ["pitch", "bat"])
        path = f"teams/{self.abbr}/{pit_or_bat}team.shtml"
        page = BRPage(path)
        validate_input(table, page.tables)
        df = page.get_df(table)
        df = numberize_df(df)
        return df
    
    def all_star(self, table="batting_register", pit_or_bat="bat"):
        validate_input(pit_or_bat, ["pitch", "bat"])        
        path = f"teams/{self.abbr}/{pit_or_bat}-all-star.shtml"
        page = BRPage(path)
        validate_input(table, page.tables)
        df = page.get_df(table)
        df = numberize_df(df)
        return df
    
    def managers(self):
        path = f"teams/{self.abbr}/managers.shtml"
        page = BRPage(path)
        df = page.get_df("manager_register")
        df = numberize_df(df)
        return df