# MALscraPy
Using Python with BeautifulSoup as scraping module, this script gathers information from the anime in a range of seasons you can specify at https://myanimelist.net/anime/season

Access to the last dataset on my Kaggle [here](https://www.kaggle.com/crazygump/myanimelist-scrappind-a-decade-of-anime)

### Example of results
| Title | MAL-id | Type | Studio | Release-season | Release-year | Release-date | Source-material | Episodes | Score | Members | Genres |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Attack No.1 | 1550 | TV (New) | Tokyo Movie Shinsha | winter | 1970 | 1969-12-07 19:00:00 | Manga | 104 | 6.74 | 7103 | ['Drama', 'Sports'] |

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

# MergeData
A simple script to merge data from two list you have scrap. A way to avoid scraping from 1917 each year ^^

## Want to run the script without knowing much about Python ?
Use the latest executable [here](https://github.com/Gumpy-Q/MALscraPy/releases/)

### Run it
Get two csv file with the data from MALscrapy.
When you will run the exe, follow the instructions in the GUI.

## Want to run, read or modify the script with Python ?
You need to install [Python (3.9 used)]( https://www.python.org/downloads/) and its following modules:
* [Pandas](https://pandas.pydata.org/docs/getting_started/install.html)
* [PySimpleGUI](https://pysimplegui.readthedocs.io/en/latest/#install)

A file with the data at the right format (see Exemple of results for MALscraPy)

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
Get a csv file with the data from MALscrapy.
When you will run the exe, follow the instructions in the GUI.

## Want to run, read or modify the script with Python ?
You need to install [Python (3.9 used)]( https://www.python.org/downloads/) and its following modules:
* [Numpy](https://numpy.org/install/)
* [Pandas](https://pandas.pydata.org/docs/getting_started/install.html)
* [PySimpleGUI](https://pysimplegui.readthedocs.io/en/latest/#install)
* [Matplotlib](https://matplotlib.org/stable/users/installing.html)
* [Seaborn](https://seaborn.pydata.org/installing.html)

A file with the data at the right format (see Exemple of results for MALscraPy)

# Otakulyzer
You want to play with your own data now ? You can !

### Use it to your heart content but...
Please leave the credits on the plots if you want to share them

### Example of results

![Anime from YYYY watched by crazy-gump](https://github.com/Gumpy-Q/MALscraPy/blob/main/Plots/crazy-gump_year_evolution2011-2021.png?raw=true)
![The same but we look also to the season](https://github.com/Gumpy-Q/MALscraPy/blob/main/Plots/crazy-gump_season_evolution-2011-2021.png?raw=true)
![Which studio did you watch more anime during thos last years?](https://github.com/Gumpy-Q/MALscraPy/blob/main/Plots/crazy-gump_studio-2011-2021.png?raw=true)
![Manga adaptation lover or original hipster ?](https://github.com/Gumpy-Q/MALscraPy/blob/main/Plots/crazy-gump_source-2011-2021.png?raw=true)
![Your score distribution](https://github.com/Gumpy-Q/MALscraPy/blob/main/Plots/crazy-gump_score_distribution-2011-2021.png?raw=true)
![Are you "mainstream" or you have underground taste](https://github.com/Gumpy-Q/MALscraPy/blob/main/Plots/crazy-gump_score_viewers-2011-2021.png?raw=true)
![How long are your anime (don't lie, it's 12 episodes since a long time)](https://github.com/Gumpy-Q/MALscraPy/blob/main/Plots/crazy-gump_episode_TV%20(New)-2011-2021.png?raw=true)
![Compare your taste with other MAL users](https://github.com/Gumpy-Q/MALscraPy/blob/main/Plots/crazy-gump_score_vs_MAL-1986-2021.png?raw=true)

## Want to run the script without knowing much about Python ?
Use the latest executable [here (at least 2.0)](https://github.com/Gumpy-Q/MALscraPy/releases/)

### Run it
Get a csv file with the data from MALscrapy.
Get your MAL export : [here](https://myanimelist.net/panel.php?go=export)
When you will run the exe, follow the instructions in the GUI.

## Want to run, read or modify the script with Python ?
You need to install [Python (3.9 used)]( https://www.python.org/downloads/) and its following modules:
* [Numpy](https://numpy.org/install/)
* [Pandas](https://pandas.pydata.org/docs/getting_started/install.html)
* [PySimpleGUI](https://pysimplegui.readthedocs.io/en/latest/#install)
* [Matplotlib](https://matplotlib.org/stable/users/installing.html)
* [Seaborn](https://seaborn.pydata.org/installing.html)
* [lxml](https://lxml.de/installation.html)

A file with the data at the right format (see Exemple of results for MALscraPy)
Your MAL export : [here](https://myanimelist.net/panel.php?go=export)


#MyFriendAnimeList
Side project suggested to me so you can get a list of the anime your MAL friend have watched and the mean score they have given to it.
The best way to catch up the good anime from a season you could not invest time in.

### Example of results
| Title | MAL-id | Type | Release-season | Release-year | crazy-gump score | friends mean score | nb who watched it | friends who watched it |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Wu Liuqi Zhi Xuanwu Guo Pian | 45556 | ONA | Winter | 2021 | | 9 | 1 | Djidji; |
| Pui Pui Molcar | 44235 | TV | Winter | 2021 | 8 | 9 | 1 | Yokanime; |
| Mushoku Tensei: Isekai Ittara Honki Dasu | 39535 | TV | Winter | 2021 | 6 | 8,5 | 2 | Zccdcccc;Djidji; |

## Want to run the script without knowing much about Python ?
Use the latest executable [here](https://github.com/Gumpy-Q/MALscraPy/releases/)

### Run it
A MAL username
When you will run the exe, follow the instructions in the GUI.

## Want to run, read or modify the script with Python ?
You need to install [Python (3.9 used)]( https://www.python.org/downloads/) and its following modules:
* [Numpy](https://numpy.org/install/)
* [Pandas](https://pandas.pydata.org/docs/getting_started/install.html)
* [PySimpleGUI](https://pysimplegui.readthedocs.io/en/latest/#install)

