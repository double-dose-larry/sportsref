import re
import urllib.request
import urllib.parse
import pandas as pd
from bs4 import BeautifulSoup


class Page():
    """Page object represents a sports-reference entity page, such as player or franchise or leauge or team_season or leauge_season.
    A Page requires a site abbreviation ("br" for baseball-reference.com, "cfb" for college-football-reference.com) and a path.
    A Page knows what stats tables are on the page and will return pandas DataFrames when asked.
    
    >>> page_player = Page(site="br", path="/players/split.fcgi", query_dict = dict(id='albieoz01',year='2019',t='b'),verbose=False)
    >>> print(page_player.web_url)
    https://www.baseball-reference.com/players/split.fcgi?id=albieoz01&year=2019&t=b
    >>> print(page_player.get_df('total').shape)
    (1, 29)
    
    >>> print(Page("hr", "/teams/MTL/2020_games.html",verbose=False).get_df("games").shape)
    (86, 16)
    
    >>> print(Page("cfb", "cfb/players/clyde-edwards-helaire-1/splits/2017/",verbose=False).get_df("splits").shape)
    (39, 14)
    
    >>> print(Page("bbr", "players/l/lopezro01/gamelog/2012", verbose=False).get_df("pgl_basic").shape)
    (69, 30)
    
    >>> print(Page("cbb", "cbb/schools/kansas/2018-gamelogs.html", verbose=False).get_df("sgl-basic").shape)
    (41, 40)
    """
    
    def __init__(self, site, path, query_dict={}, verbose=True):

        self.site = site
        self.path = path
        self.query_dict = query_dict
        self.query_string = urllib.parse.urlencode(self.query_dict)
        self.web_url = urllib.parse.urlunsplit([
            'https',            # scheme
            self.site,          # network location
            self.path,          # path
            self.query_string,  # query
            '',                 # fragment
        ])
        
        self._cached_tables = self._enumerate_tables()
        self.tables = list(self._cached_tables.keys())
        if verbose:
            print(f"Available tables: {[ tbl for tbl in self.tables if tbl is not None ]}")
        
    def __repr__(self):
        return f"< Page, web_url : '{self.web_url}' >"
    
    def _enumerate_tables(self):
        with urllib.request.urlopen(self.web_url) as res:
            tables = {}
            html = res.read()
            html = str(html).replace("<!--", "").replace("-->", "")
            soup = BeautifulSoup(html, features="lxml")
            # clear out the footers
            for tf in soup.find_all("tfoot"):
                tf.decompose()
            # clear out unnecessary repeated column headers
            for tr_head in soup.find_all("tr", {'class':'thead'}): 
                tr_head.decompose()
            # stuff the dataframes into the dict
            for tbl in soup.find_all("table"):
                if not tbl is None:
                    tables[tbl.get("id")] = tbl
            return tables
    
    def get_data_url(self, table):

        qs = urllib.parse.urlencode({
            'css' : 1,
            'site': self.site,
            'url' :  self.web_url.split(self.site)[-1],
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
        tbl = self._cached_tables[table]
        return pd.read_html(str(tbl))[0]


