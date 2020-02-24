import re
import urllib.request
import urllib.parse
import pandas as pd

site_map = {
    "br" : "www.baseball-reference.com",
    "hr" : "www.hockey-reference.com",
    "pfr": "www.pro-football-reference.com",
    "cfb": "www.sports-reference.com",
    "bbr": "www.basketball-reference.com",
    "cbb": "www.sports-reference.com"
}


class Page():
    """Page object represents a sports-reference entity page, such as player or franchise or leauge or team_season or leauge_season.
    A Page requires a site abbreviation ("br" for baseball-reference.com, "cfb" for college-football-reference.com) and a path.
    A Page knows what stats tables are on the page and will return pandas DataFrames when asked.
    
    >>> page_player = Page(site="br", path="/players/split.fcgi", query_dict = dict(id='albieoz01',year='2019',t='b'))
    >>> print(page_player.web_url)
    https://www.baseball-reference.com/players/split.fcgi?id=albieoz01&year=2019&t=b
    >>> print(page_player.get_df('total').shape)
    (1, 29)
    
    >>> print(Page("hr", "/teams/MTL/2020_games.html").get_df("games").shape)
    (86, 16)
    
    >>> print(Page("cfb", "cfb/players/clyde-edwards-helaire-1/splits/2017/").get_df("splits").shape)
    (39, 14)
    
    >>> print(Page("bbr", "players/l/lopezro01/gamelog/2012").get_df("pgl_basic").shape)
    (69, 30)
    
    >>> print(Page("cbb", "cbb/schools/kansas/2018-gamelogs.html").get_df("sgl-basic").shape)
    (41, 40)
    """
    
    def __init__(self, site, path, query_dict={}):
        self._cached_tables = None
        self.site = site
        self.path = path
        self.query_dict = query_dict
        self.query_string = urllib.parse.urlencode(self.query_dict)
        self.web_url = urllib.parse.urlunsplit([
            'https',            # scheme
            site_map[self.site],# network location
            self.path,          # path
            self.query_string,  # query
            '',                 # fragment
        ])
        
    @property    
    def tables(self):
        if not self._cached_tables:
            self._cached_tables = self._enumerate_tables()
        return self._cached_tables
    
    def __repr__(self):
        return f"< Page, web_url : '{self.web_url}' >"
    
    def _enumerate_tables(self):
        table_id_pattern = re.compile('table_container"\s*id="div_(\w+)"')
        with urllib.request.urlopen(self.web_url) as res:
            return table_id_pattern.findall(str(res.read()))
    
    def get_data_url(self, table):

        qs = urllib.parse.urlencode({
            'css' : 1,
            'site': self.site,
            'url' :  self.web_url.split(site_map[self.site])[-1],
            'div' : f'div_{table}',
        })
        
        return urllib.parse.urlunsplit([
            'https',                       # scheme
            "widgets.sports-reference.com",# network location
            "/wg.fcgi",                    # path
            qs,                            # query
            '',                            # fragment
        ])
        
    def get_df(self, table):
        data_url = self.get_data_url(table)
        return pd.read_html(self.get_data_url(table))[0]


