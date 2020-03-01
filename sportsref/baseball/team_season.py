from .br_page import BRPage
from .util import *
from .team_abbr_parser import TeamAbbrParser

class TeamSeason():
    
    def __init__(self, fran, year):
        self.franchise = fran
        self.year = year
        self.abbr = TeamAbbrParser(f"https://www.baseball-reference.com/teams/{fran.abbr}/").team_year_abbr_map[year]
        
    def __repr__(self):
        return f"< {self.abbr}, year {self.year} >"
    
    def lineups(self):
        path = f"teams/{self.abbr}/{self.year}-lineups.shtml"
        page = BRPage(path)
        df = page.get_df(page.tables[0])
        return df
    
    def stats(self, table="team_batting"):
        #get page
        path = f"teams/{self.abbr}/{self.year}.shtml"
        page = BRPage(path)
        validate_input(table, page.tables)
        return df
    
    def schedule_results(self):
        # get page
        path = f"teams/{self.abbr}/{self.year}-schedule-scores.shtml"
        page = BRPage(path)
        # clean
        df = page.get_df("team_schedule")
        clean_up_filter = (df.Tm != 'Tm')
        df_clean = df[clean_up_filter]
        df_clean_renamed = df_clean.rename({'Unnamed: 4' : "H/A"}, axis=1)
        df_clean_renamed = df_clean_renamed.drop('Unnamed: 2', axis=1)
        df_clean_renamed["H/A"] = df_clean_renamed["H/A"].fillna("H").replace('@','A')
        return df_clean_renamed