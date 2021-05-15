# MALscraPy
Using Python with BeautifulSoup as scraping module, this script gathers information from the anime in a range of seasons you can specify at https://myanimelist.net/anime/season

Access to the last dataset on my Kaggle [here](https://www.kaggle.com/crazygump/myanimelist-scrappind-a-decade-of-anime)

### Example of results
| Title | MAL-id | Type | Studio | Realase-season | Release-year | Release-date | Source-material | Episodes | Score | Members |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Attack No.1 | 1550 | TV (New) | Tokyo Movie Shinsha | winter | 1970 | 1969-12-07 19:00:00 | Manga | 104 | 6.74 | 7103 |

## Want to run the script without knowing much about Python ?
Use the latest executable [here](https://github.com/Gumpy-Q/MALscraPy/releases/)

### Run it
When you will run the exe, follow the instructions in GUI.

Beware: scraping large temporal range might be a bit RAM intensive (600 MB for 2020 to 2010)

This may not be the fastest way to scrap MAL but it gets the job done (3m45s for 2020 to 2010)

## Want to run, read or modify the script with Python ?
### Requisites
You need to install [Python (3.9 used)]( https://www.python.org/downloads/) and its following modules:
* [Requests](https://docs.python-requests.org/en/latest/user/install/#install) 
* [BeautifulSoup4](https://www.crummy.com/software/BeautifulSoup/bs4/doc/#installing-beautiful-soup)
* [Numpy](https://numpy.org/install/)
* [Pandas](https://pandas.pydata.org/docs/getting_started/install.html)
* [PySimpleGUI](https://pysimplegui.readthedocs.io/en/latest/#install)

# MyAnalizer
Want to visualize the juicy data you have just scraped ? Here it is !

As for now this scripts can draw these kinds of plots:
* Evolution of production (year & season)
* Top 3 studio production over the year
* Number of studio in activity
* Source material of anime production
* Score distribution
* Score correlation to popularity
* MAL viewers evolution
* Length of anime aired (New production & Production continuing release)

### Use it to your heart content but...
Please leave the credits on the plots if you want to share them

### Example of results

![Evolution of the anime production from 1970 to 2021](https://github.com/Gumpy-Q/MALscraPy/blob/main/Plots/year_evolution1970-2020.png?raw=true)
![Evolution of the anime production with seasons from 1990 to 2021](https://github.com/Gumpy-Q/MALscraPy/blob/main/Plots/season_evolution-1990-2021.png?raw=true)
![Evolution of top 3 studio production from 1990 to 2021](https://github.com/Gumpy-Q/MALscraPy/blob/main/Plots/studio-1990-2021.png?raw=true)
![Evolution of number of studio in activity from 1990 to 2021](https://github.com/Gumpy-Q/MALscraPy/blob/main/Plots/studio_quantity-1990-2021.png?raw=true)
![Source of the anime adaptation from 2000 to 2021](https://github.com/Gumpy-Q/MALscraPy/blob/main/Plots/source-2000-2021.png?raw=true)
![Community score from 2000 to 2021](https://github.com/Gumpy-Q/MALscraPy/blob/main/Plots/score_distribution-2000-2021.png?raw=true)
![Score and viewers from 1990 to 2021](https://github.com/Gumpy-Q/MALscraPy/blob/main/Plots/score_viewers-1990-2021.png?raw=true)
![MAL viewers from 2000 to 2021](https://github.com/Gumpy-Q/MALscraPy/blob/main/Plots/viewers_distribution-2000-2021.png?raw=true)
![New anime length from 1990 to 2021](https://github.com/Gumpy-Q/MALscraPy/blob/main/Plots/episode_TV%20(New)-1990-2021.png?raw=true)
![Continued anime length from 1990 to 2021](https://github.com/Gumpy-Q/MALscraPy/blob/main/Plots/episode_TV%20(Continuing)-1990-2021.png?raw=true)



## Want to run the script without knowing much about Python ?
Use the latest executable [here](https://github.com/Gumpy-Q/MALscraPy/releases/)

### Run it
Get a csv file with the data
When you will run the exe, follow the instructions in GUI.

## Want to run, read or modify the script with Python ?
You need to install [Python (3.9 used)]( https://www.python.org/downloads/) and its following modules:
* [Numpy](https://numpy.org/install/)
* [Pandas](https://pandas.pydata.org/docs/getting_started/install.html)
* [PySimpleGUI](https://pysimplegui.readthedocs.io/en/latest/#install)
* [Matplotlib](https://matplotlib.org/stable/users/installing.html)
* [Seaborn](https://seaborn.pydata.org/installing.html)

A file with the data at the right format (see Exemple of results for MALscraPy  


