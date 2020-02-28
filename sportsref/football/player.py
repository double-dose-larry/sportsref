from .pfr_page import PFRPage
from .util import *

all_player_df = get_players()

class Player():
    
    def __init__(self, fuzzy_name):
        p = get_player_info(fuzzy_name, all_player_df, verbose=True)
        self.key = p.key
        self.name = p["name"]
        self.first_year = int(p.years[:4])
        self.last_year = int(p.years[-4:])
        self.is_active = p.is_active == 1
        self.years_active = list(range(self.first_year, self.last_year + 1))

        
    def __repr__(self):
        return f"< {self.name}, {self.first_year} - {self.last_year}, {'active' if self.is_active else 'not active'} >"
        
    def overview(self, table="appearances"):
        # get player overview page
        path = f"/players/{self.key[0]}/{self.key}.htm"
        overview_page = PFRPage(path)
        
        # validate input
        validate_input(table, overview_page.tables)
        
        # pull and clean dataframe
        try:
            df = overview_page.get_df(table)
            df = numberize_df(df)
        except:
            raise Exception(f"error getting {table_type} for key {self.name}. "
                            "probably because the table doesn't exist on the page.")
        return df