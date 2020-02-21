from .bref_util import get_player_info, validate_input, numberize_df, convert_url
from urllib.parse import quote, urlencode
import pandas as pd

BASE_URL = "https://widgets.sports-reference.com/wg.fcgi?"
WEB_BASE_URL = "https://www.baseball-reference.com/"

class Player():
    
    def __init__(self, fuzzy_name):
        p = get_player_info(fuzzy_name, verbose=True)
        self.key = p.key
        self.name = p["name"]
        self.first_year = int(p.years[:4])
        self.last_year = int(p.years[-4:])
        self.is_active = p.is_active == 1
        self.years_active = list(range(self.first_year, self.last_year + 1))
        self.pit_or_bat_default = self._pit_or_bat()
        
    def __repr__(self):
        return f"< {self.name}, {self.first_year} - {self.last_year}, {'active' if self.is_active else 'not active'} >"
    
    def _pit_or_bat(self):
        df = self.overview().sum()
        return "p" if df.P / df.G > 0.5 else "b"
        
    def overview(self, table_type="appearances"):
        """
        get data that's normally found on the overview page of a player page
        """
        path = f"/players/{self.key[0]}/{self.key}.shtml"
        # validate inputs
        valid_table_types = ["pitching_standard", "pitching_value", "batting_standard",
                            "batting_value", "standard_fielding", "appearances",
                            "batting_postseason", "pitching_postseason"]
        validate_input(table_type, valid_table_types)
        
        # grab the table   
        # scheme - always http
        # netloc - class would know
        # path - will be built by the method
        # params - none
        # query - also built by the method - added to the data url
        # fragment - empty
        
        
        query_dict = {
            'css': 1,
            'site': 'br',
            'url': quote(path),
            'div': f'div_{table_type}'
        } 
        
        
        player_overview_url = f"{BASE_URL}{urlencode(query_dict)}"
        #print(player_overview_url)
        
        try:
            df = pd.read_html(player_overview_url)[0].query("Lg == 'NL' or Lg == 'AL'")
            df = df.query("Tm != 'TOT'")
            df = numberize_df(df)
        except:
            raise Exception(f"error getting {table_type} for key {self.name}. "
                            "probably because the table doesn't exist on the page.")
        return df
    
    def splits(self, table_type, split_type="default", year="career"):
        """
        get data that's normally found on the splits page of the player
        """
        #constants
        url = f"https://www.baseball-reference.com/players/split.fcgi?id={self.key}&year={year}&t={split_type}"
        
        if split_type == "default":
            split_type = self.pit_or_bat_default
        
        # validate inputs
        common_tables = ['bases', 'clutc', 'count', 'half', 'hitlo', 'hmvis', 'innng',
                         'leado', 'lever', 'lineu', 'month', 'oppon', 'outs', 'plato',
                         'site', 'stad', 'times', 'total', 'traj']
        pit_only_tables = ['catch', 'defpo', 'dr', 'dr_extra', 'half_extra',
                           'hmvis_extra', 'month_extra', 'oppon_extra', 'outco',
                           'outco_extra', 'pitco', 'rs', 'rs_extra', 'site_extra',
                           'sprel', 'sprel_extra', 'stad_extra', 'tkswg', 'total_extra',
                           'ump', 'ump_extra']
        bat_only_tables = ['defp', 'gbfb', 'outcb', 'power', 'stsub']
        
        if split_type == 'p':
            valid_table_types = common_tables + pit_only_tables
        else:
            valid_table_types = common_tables + bat_only_tables
       
        # run validation
        validate_input(split_type, ["b", "p"])
        validate_input(year, self.years_active + ["career"])
        validate_input(table_type, valid_table_types)
        
        # build splits url
        splits_url = f"{convert_url(url)}&div=div_{table_type}"
    
        try:
            if str(year).lower() == "career":
                df = pd.read_html(splits_url)[0].drop("I", axis=1)
            else:
                df = pd.read_html(splits_url)[0]
        except:
            raise Exception(f"error getting {table_type} for {self.name}. "
                           " probably because the table doesn't exist on the page.")
        # make sure numbers are appropriate dtype
        df = numberize_df(df)
        df["year"] = year
        
        return df
    
    def game_logs(self, year, log_type="default"):
        """
        get data that's normally found on the game logs page of the player
        """

        
        if log_type == "default":
            log_type = self.pit_or_bat_default
        
        # run validatation
        validate_input(year, self.years_active)
        validate_input(log_type, ["b","p","f"])
        
        log_type_map = {'b' : 'batting_gamelogs',
                        'p' : 'pitching_gamelogs',
                        'f' : '_0'} # wtf bref, you couldn't find a better name?
        
        # constants
        url = f"https://www.baseball-reference.com/players/gl.fcgi?id={self.key}&t={log_type}&year={year}"
        
        # get the data
        game_log_url = f"{convert_url(url)}&div=div_{log_type_map[log_type]}"
#         print(game_log_url)
        df = (pd.read_html(game_log_url)[0]
              .query("Tm != 'Tm'")
              .dropna(subset=["Tm", "Rk"])
              .rename({"Unnamed: 4" : "H/A",
                       "Unnamed: 5" : "H/A"}, axis=1))
        
        # clean up the home/away column
        df["H/A"] = df["H/A"].fillna("H").replace("@", "A")
        df = numberize_df(df)
        # add year
        df["year"] = year
        
        # make sure numbers are appropriate dtype
        return df
    
    def vs_pitcher(self):
        """
        returns a pandas.DataFrame of vs_pitcher batting splits
        """
        url = f"https://www.baseball-reference.com/play-index/batter_vs_pitcher.cgi?batter={self.key}"
        data_url = f"{convert_url(url)}&div=div_ajax_result_table"
        df = (pd.read_html(data_url)[0])
        df = numberize_df(df)
        df["name"] = self.name
        return df
        
        
    
