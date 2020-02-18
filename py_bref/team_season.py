from .bref_util import get_fran_info, validate_input, numberize_df, convert_url
from .franchises import Franchise
from .team_abbr_parser import TeamAbbrParser
import pandas as pd

class TeamSeason():
    
    def __init__(self, fran, year):
        self.franchise = fran
        self.year = year
        self.abbr = TeamAbbrParser(f"https://www.baseball-reference.com/teams/{fran.abbr}/").team_year_abbr_map[year]
        
    def __repr__(self):
        return f"< {self.abbr}, year {self.year} >"
    
    def stats(self, table="team_batting"):
        """
        available tables:  ['team_batting', 'team_pitching', 'appearances', 'standard_fielding',
                             'players_value_batting', 'players_value_pitching']
        """
        valid_table_types =  ['team_batting', 'team_pitching', 'appearances', 'standard_fielding',
                             'players_value_batting', 'players_value_pitching']
        validate_input(table, valid_table_types)
        
        url = f"https://www.baseball-reference.com/teams/{self.abbr}/{self.year}.shtml"
        
        team_url = f"{convert_url(url)}&div=div_{table}"
        # filter
        
        df = pd.read_html(team_url)[0].query("Name != 'Name'")
        filtr = (df.Name.str.contains("Totals")) | (df.Name.str.contains("Rank in"))
        df = df[~filtr]
        df = numberize_df(df)
        return df
    
    def schedule_results(self):
        """
        gets game logs for the season
        """
        
        url = f"https://www.baseball-reference.com/teams/{self.abbr}/{self.year}-schedule-scores.shtml"
        data_url = f"{convert_url(url)}&div=div_team_schedule"
        
        df = pd.read_html(data_url)[0]
        clean_up_filter = (df.Tm != 'Tm')
        df_clean = df[clean_up_filter]
        df_clean_renamed = df_clean.rename({'Unnamed: 4' : "H/A"}, axis=1)
        df_clean_renamed = df_clean_renamed.drop('Unnamed: 2', axis=1)
        df_clean_renamed["H/A"] = df_clean_renamed["H/A"].fillna("H").replace('@','A')
        df_final = numberize_df(df_clean_renamed)
        return df_final