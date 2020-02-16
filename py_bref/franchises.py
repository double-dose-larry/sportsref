from .bref_util import get_fran_info, validate_input, numberize_df
from .constants import BASE_URL
import pandas as pd

class Franchise():
    
    def __init__(self, fuzzy_fran):
        f = get_fran_info(fuzzy_fran)
        self.abbr = f.abbr
        self.name = f.name
        self.first_year = int(f.years[:4])
        self.last_year = int(f.years[-4:])
        self.years_active = list(range(self.first_year, self.last_year + 1))
        
    def __repr__(self):
        return f"< {self.name}, {self.first_year} - {self.last_year} >"
    
    def hist(self, fran_table="franchise_years"):
        """
        available tables: ['franchise_years', 'history']
        """
        valid_table_types =  ['franchise_years', 'history']
        validate_input(fran_table, valid_table_types)
        
        fran_url = f"{BASE_URL}teams%2F{self.abbr}%2F&div=div_{fran_table}"
        df = pd.read_html(fran_url)[0].query('Tm != "Overall"')
        df = numberize_df(df)
        return df
    
    def batters(self):
        """
        all batters to play for the franchise
        """
        #  "https://widgets.sports-reference.com/wg.fcgi?css=1&site=br&url=%2Fteams%2FTBD%2Fbat.shtml&div=div_batting_register"
        fran_bats_url = f"{BASE_URL}teams%2F{self.abbr}%2Fbat.shtml&div=div_batting_register"
        df = pd.read_html(fran_bats_url)[0].query("Name != 'Name'")
        df = numberize_df(df)
        return df
    
    def pitchers(self):
        """
        all batters to play for the franchise
        """
        #  "https://widgets.sports-reference.com/wg.fcgi?css=1&site=br&url=%2Fteams%2FTBD%2Fpitch.shtml&div=div_pitching_register"
        fran_bats_url = f"{BASE_URL}teams%2F{self.abbr}%2Fpitch.shtml&div=div_pitching_register"
        df = pd.read_html(fran_bats_url)[0].query("Name != 'Name'")
        df = numberize_df(df)
        return df
    
    def draft(self, year):
        """
        get draft for each round of a year.
        """
        # TODO refactor and error proof
        # "https://widgets.sports-reference.com/wg.fcgi?css=1&site=br&url=%2Fdraft%2F%3Fteam_ID%3DSTL%26year_ID%3D2019%26draft_type%3Djunreg%26query_type%3Dfranch_year%26from_type_jc%3D0%26from_type_hs%3D0%26from_type_4y%3D0%26from_type_unk%3D0&div=div_draft_stats"
        # https://www.baseball-reference.com/draft/?team_ID=STL&year_ID=2019&draft_type=junreg&query_type=franch_year&from_type_jc=0&from_type_hs=0&from_type_4y=0&from_type_unk=0
        query = f"team_ID%3D{self.abbr}%26year_ID%3D{year}%26draft_type%3Djunreg%26query_type%3Dfranch_year%26from_type_jc%3D0%26from_type_hs%3D0%26from_type_4y%3D0%26from_type_unk%3D0"
        fran_draft_url = f"{BASE_URL}draft%2F%3F{query}&div=div_draft_stats"
        df = pd.read_html(fran_draft_url)[0]
        df = numberize_df(df)
        return df
    
    def parks(self):
        # https://widgets.sports-reference.com/wg.fcgi?css=1&site=br&url=%2Fteams%2FTBD%2Fattend.shtml&div=div_franchise_years
        fran_parks_url = f"{BASE_URL}teams%2F{self.abbr}%2Fattend.shtml&div=div_franchise_years"
        df = pd.read_html(fran_parks_url)[0]
        df = numberize_df(df)
        return df