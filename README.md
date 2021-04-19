# MALscraPy
Using Python with BeautifulSoup as scraping modules, this script collects information from the anime in a range of seasons you can specify at https://myanimelist.net/anime/season

Access to the last dataset on my Kaggle [here](https://www.kaggle.com/crazygump/myanimelist-scrappind-a-decade-of-anime)

### Example of results
| Title | MAL-id | Type | Studio | Realase-season | Release-year | Release-date | Source-material | Episodes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Attack No.1 | 1550 | TV (New) | Tokyo Movie Shinsha | winter | 1970 | 1969-12-07 19:00:00 | Manga | 104 |

## Want to run the script without knowing much about Python ?
Use the latest executable [here](https://github.com/Gumpy-Q/MALscraPy/releases/)

## Want to run, read or modify the script with Python ?
### Requisites
You only need to install [Python]( https://www.python.org/downloads/) and its following modules:
* [Requests](https://docs.python-requests.org/en/latest/user/install/#install) 
* [BeautifulSoup4](https://www.crummy.com/software/BeautifulSoup/bs4/doc/#installing-beautiful-soup)
* [Numpy](https://numpy.org/install/)
* [Pandas](https://pandas.pydata.org/docs/getting_started/install.html)

## Run it
When you will run the script, follow the instructions in the GUI.
Beware: scraping large temporal range might be a bit RAM intensive (500 MB for 2021 to 2010)

This is may not be the fastest way to scrap MAL (30s to scrap all 2020 anime content with 15 seconds of sleep time to avoid making MAL mad at me)


# MyAnalizer
Want to visualize the data you have just scraped ? Here it is !

### Example of results

![Evolution of the anime production from 1970 to 2021](https://github.com/Gumpy-Q/MALscraPy/blob/main/Plots/year_evolution1970-2020.png)
![Evolution of the anime production with seasons from 1990 to 2021](https://github.com/Gumpy-Q/MALscraPy/blob/main/Plots/season_evolution-1990-2021.png)
![Source of the anime adaptation from 2000 to 2021](https://github.com/Gumpy-Q/MALscraPy/blob/main/Plots/source-2000-2021.png)
![New anime length from 1990 to 2021](https://github.com/Gumpy-Q/MALscraPy/blob/main/Plots/episode_TV%20(New)-1990-2021.png)
![Continued anime length from 1990 to 2021](https://github.com/Gumpy-Q/MALscraPy/blob/main/Plots/episode_TV%20(Continuing)-1990-2021.png)


## Want to run the script without knowing much about Python ?
Use the latest executable [here](https://github.com/Gumpy-Q/MALscraPy/releases/)

## Want to run, read or modify the script with Python ?
### Requisites
Previous requisites  
A csv file with the data you scraped before  

## Run it
When you will run the script, follow the instructions in GUI.

