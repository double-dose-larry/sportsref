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
    
    def stats(self, table="team_batting"):
        #get page
        path = f"teams/{self.abbr}/{self.year}.shtml"
        page = BRPage(path)
        validate_input(table, page.tables)
        #clean
        df = page.get_df(table).query("Name != 'Name'")
        filtr = (df.Name.str.contains("Totals")) | (df.Name.str.contains("Rank in"))
        df = df[~filtr]
        df = numberize_df(df)
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
        df_final = numberize_df(df_clean_renamed)
        return df_final