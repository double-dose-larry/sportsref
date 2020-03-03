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
        self._cached_overview = None
        self.pit_or_bat_default =  self._pit_or_bat()
        
    @property
    def overview_page(self):
        if not self._cached_overview:
            path = f"/players/{self.key[0]}/{self.key}.shtml"
            self._cached_overview = BRPage(path, verbose=False)
        return self._cached_overview


    def __repr__(self):
        actv = 'active' if self.is_active else 'not active'
        return f"< {self.name}, {self.first_year} - {self.last_year}, {actv} >"
    
    def _pit_or_bat(self):
        df = self.overview().sum()
        return "p" if df.P / df.G > 0.5 else "b"
        
    def overview(self, table="appearances"):
        overview_page = self.overview_page
        validate_input(table, overview_page.tables)
        df = overview_page.get_df(table)
        return df
    
    def splits(self, table, split_type="default", year="career"):
        
        if split_type == "default":
            split_type = self.pit_or_bat_default
        
            # get player splits page
        path = "players/split.fcgi"
        query_dict = {
                'year' : year,
                'id' : self.key,
                't' : split_type
            }
        validate_input(split_type, ["b", "p"])
        validate_input(year, self.years_active + ["career"])
        splits_page = BRPage(path, query_dict)
        # validate input
        validate_input(table, splits_page.tables)
        # pull and clean dataframe
        df = splits_page.get_df(table)
        df["year"] = year
        return df
    
    def game_logs(self, year, log_type="default"):
        """
        get data that's normally found on the game logs page of the player
        """
        # set defaults
        if log_type == "default":
            log_type = self.pit_or_bat_default
        
        log_type_map = {'b' : 'batting_gamelogs',
            'p' : 'pitching_gamelogs',
            'f' : '_0'} # wtf bref, you couldn't find a better name?
        
        # run validatation
        validate_input(year, self.years_active)
        validate_input(log_type, ["b","p","f"])
        
        # get gamelog page
        path = "/players/gl.fcgi"
        query_dict = {
            'id': self.key,
            't' : log_type,
            'year' : year
        }
        game_log_page = BRPage(path, query_dict)

        # pull dataframe and clean
        df = (game_log_page.get_df(log_type_map[log_type])
              .query("Tm != 'Tm'")
              .dropna(subset=["Tm", "Rk"])
              .rename({"Unnamed: 4" : "H/A",
                       "Unnamed: 5" : "H/A"}, axis=1))
        # clean up the home/away column
        df["H/A"] = df["H/A"].fillna("H").replace("@", "A")
        df["year"] = year
        return df
    
    def vs(self, who=None):
        """
        returns a pandas.DataFrame of vs_pitcher batting splits
        """
        # validate
        validate_input(who, ["batter", "pitcher", None])
        
        # set defaults
        if not who:
            who = 'pitcher' if self.pit_or_bat_default == 'p' else 'batter'
        else:
            who = 'pitcher' if who == 'batter' else 'batter'
        
        # get vs page
        path = "play-index/batter_vs_pitcher.cgi"
        query_dict = { who : self.key}
        vs_page = BRPage(path, query_dict)
        
        # get dataframe and clean
        df = vs_page.get_df("ajax_result_table")
        df["name"] = self.name
        return df
    
    def advanced(self, table, stats_type = "default"):
        
        if stats_type == "default":
            stats_type = self.pit_or_bat_default
        
        validate_input(stats_type, ["b", "p", "f"])
        
        adv_stats_map = {
            'b' : 'bat',
            'p' : 'pitch',
            'f' : 'field'
        }
        
        path = f"players/{self.key[0]}/{self.key}-{adv_stats_map[stats_type]}.shtml"
        page = BRPage(path)
        validate_input(table, page.tables)
        # clean up
        df = page.get_df(table)
        return df
    
    def hr_log(self, table="play_by_play"):
        path = "players/event_hr.fcgi"
        query_dict = {
            'id' : self.key,
            't' : self.pit_or_bat_default
        }
        page = BRPage(path, query_dict)
        df = page.get_df(table)
        return df