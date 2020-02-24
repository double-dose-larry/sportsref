from .util import *
from .team_abbr_parser import TeamAbbrParser
from .page import Page

all_player_df = get_players()
all_fran_df = get_frans()

class BRPage(Page):
    "baseball-reference.com page"
    def __init__(self, path, query_dict={}):
        super().__init__("br", path, query_dict)


class Player():
    
    def __init__(self, fuzzy_name):
        p = get_player_info(fuzzy_name, all_player_df, verbose=True)
        self.key = p.key
        self.name = p["name"]
        self.first_year = int(p.years[:4])
        self.last_year = int(p.years[-4:])
        self.is_active = p.is_active == 1
        self.years_active = list(range(self.first_year, self.last_year + 1))
        self.pit_or_bat_default =  self._pit_or_bat()
        
    def __repr__(self):
        return f"< {self.name}, {self.first_year} - {self.last_year}, {'active' if self.is_active else 'not active'} >"
    
    def _pit_or_bat(self):
        df = self.overview().sum()
        return "p" if df.P / df.G > 0.5 else "b"
        
    def overview(self, table="appearances"):
        # get player overview page
        path = f"/players/{self.key[0]}/{self.key}.shtml"
        overview_page = BRPage(path)
        
        # validate input
        validate_input(table, overview_page.tables)
        
        # pull and clean dataframe
        try:
            df = overview_page.get_df(table).query("Lg == 'NL' or Lg == 'AL'")
            df = df.query("Tm != 'TOT'")
            df = numberize_df(df)
        except:
            raise Exception(f"error getting {table_type} for key {self.name}. "
                            "probably because the table doesn't exist on the page.")
        return df
    
    def splits(self, table, split_type="default", year="career"):
        # set defaults
        if split_type == "default":
            split_type = self.pit_or_bat_default
        
        # get player splits page
        path = "players/split.fcgi"
        query_dict = {
            'year' : year,
            'id' : self.key,
            't' : split_type
        }
        splits_page = BRPage(path, query_dict)
        # validate input
        validate_input(split_type, ["b", "p"])
        validate_input(year, self.years_active + ["career"])
        validate_input(table, splits_page.tables)
            
        # pull and clean dataframe
        try:
            if str(year).lower() == "career":
                df = splits_page.get_df(table).drop("I", axis=1)
            else:
                df = splits_page.get_df(table)
        except:
            raise Exception(f"error getting {table_type} for {self.name}. "
                           " probably because the table doesn't exist on the page.")
        df = numberize_df(df)
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
        df = numberize_df(df)
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
        df = vs_page.get_df("ajax_result_table").query("Name != 'Name'")
        df = numberize_df(df)
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