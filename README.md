## sportsref

easily pull stats from [sports-reference](https://www.sports-reference.com) web sites

`sportsref` is designed to be used in an interactive python environment, such as IPython or JupyterNotebook

The api tries to mirror the web experience:

* each subject area (i.e. player, season, league) is represented by an object.
* each object has methods representing the pages available. 
  * for example [Ozzie Albies](https://www.baseball-reference.com/players/a/albieoz01.shtml) player page has the following menu of pages
  ![albies pages](http://imageurl)
  * if the menu is a dropdown, [such as the Splits menu on the player page]() the method takes an additional parameter or two
* the methods return Page objects which know about all the tables on that page
* use the Page.get_df("table_name") to get a pandas.DataFrame of the table you want.

The examples.ipynb JupyterNotebook has a few examples demonstrating a workflow.


## Install

clone the repo then

```python
pip install .
```

## Usage

grab data from baseball-reference.com via a nice OOP interface.

Generally speaking, the idea is to allow to grab any table that is seen on baseball-reference.com as a clean pandas dataframe.
The objects are loosely based on the pages available for each type of "thing" on the website.

For example, for a player you'll see start with the "Overview" page that contains several tables, such as **Standard Batting** and **Player Value--Batting**. The Player object provides away to grab those tables like so:

```python
from sportsref.baseball import Player
jiman = Player("Ji-Man Choi")
# returns a pandas df of the "Standard Batting" table
display(jiman.overview().get_df("batting_standard")) 
# returns a pandas df of the "Player Value--Batting" table
display(jiman.overview().get_df("batting_value"))
```


        
        
