## sportsref

easily pull stats from [sports-reference](https://www.sports-reference.com) web sites

`sportsref` is designed to be used in an interactive python environment, such as IPython or JupyterNotebook

The api tries to mirror the web experience:

* each subject area (i.e. player, season, league) is represented by an class.
* each class has methods representing the pages available. 
  * for example [Ozzie Albies](https://www.baseball-reference.com/players/a/albieoz01.shtml) player page has the following menu of pages
  ![albies pages](https://raw.githubusercontent.com/double-dose-larry/sportsref/master/docs/img/ozzie_albies.jpg)
  * if the menu is a dropdown, ![such as the Splits menu on the player page](https://raw.githubusercontent.com/double-dose-larry/sportsref/master/docs/img/menu_example.jpg) the method takes an additional parameter or two
* the methods return a Page object which know about all the tables on that page
* use the Page.get_df("table_name") to get a pandas.DataFrame of the table you want.

The examples.ipynb JupyterNotebook has a few examples demonstrating a workflow.


## Install

clone the repo then

```python
pip install .
```



        
        
