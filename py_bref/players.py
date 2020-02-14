from .bref_util import get_player_info, validate_input, numberize_df
from .constants import BASE_URL
import pandas as pd

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
        # validate inputs
        valid_table_types = ["pitching_standard", "pitching_value", "batting_standard",
                            "batting_value", "standard_fielding", "appearances",
                            "batting_postseason", "pitching_postseason"]
        validate_input(table_type, valid_table_types)
        
        # grab the table   
        player_overview_url = f"{BASE_URL}players%2F{self.key[0]}%2F{self.key}.shtml&div=div_{table_type}"
        try:
            df = pd.read_html(player_overview_url)[0].query("Lg == 'NL' or Lg == 'AL'")
            df = df.query("Tm != 'TOT'")
            df = numberize_df(df)
        except:
            raise Exception(f"error getting {table_type} for key {self.name}. "
                            "probably because the table doesn't exist on the page.")
        return df
    
    def splits(self, table_type, split_type="default", year="career"):
        
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
        splits_url = f"{BASE_URL}players%2Fsplit.fcgi%3Fid%3D{self.key}%26year%3D{year}%26t%3D{split_type}&div=div_{table_type}"
    
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
        
        if log_type == "default":
            log_type = self.pit_or_bat_default
        
        # run validatation
        validate_input(year, self.years_active)
        validate_input(log_type, ["b","p","f"])
        
        log_type_map = {'b' : 'batting_gamelogs',
                        'p' : 'pitching_gamelogs',
                        'f' : '_0'} # wtf bref, you couldn't find a better name?
        
        # get the data
        game_log_url = f"{BASE_URL}players%2Fgl.fcgi%3Fid%3D{self.key}%26t%3D{log_type}%26year%3D{year}&div=div_{log_type_map[log_type]}"
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
        
        
    