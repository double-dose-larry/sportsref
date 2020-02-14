## py_bref

grab data from baseball-reference.com via a nice OOP interface.

Generally speaking, the idea is to allow to grab any table that is seen on baseball-reference.com as a clean pandas dataframe.
The objects are loosely based on the pages available for each type of "thing" on the website.

For example, for a player you'll see start with the "Overview" page that contains several tables, such as **Standard Batting** and **Player Value--Batting**. The Player object provides away to grab those tables like so:

```python
from py_bref.players import Player
jiman = Player("Ji-Man Choi")
# returns a pandas df of the "Standard Batting" table
display(jiman.overview("batting_standard")) 
# returns a pandas df of the "Player Value--Batting" table
display(jiman.overview("batting_value"))
```

Currently implemented:

* Players
    * overview
        * appearnces
        * batting_standard
        * batting_value
        * batting_postseason
        * pitching_standard
        * pitching_value
        * pitching_postseason
    * splits
        * by year or career
        * a bunch of tables, some common, some for pitchers, some for batters
    * game logs
        * by year
* Franchises
    * history
    * batters
    * pitchers
    * draft by year
    * parks
        
Planned additions:

* Teams
    * stats
        * by season
    * schedule & results
        * by season
    * rosters
        * by season
        * coaching staff
* Seasons
    * standings
    * batting stats
        * team batting
        * individual batting
    * pitching stats
        * team pitching
        * individual pitching
        
        