# MALscraPy
Using Python with BeautifulSoup as scraping modules, this script collects information from the anime in a range of seasons you can specify at https://myanimelist.net/anime/season

Access to the last dataset on my Kaggle [here](https://www.kaggle.com/crazygump/myanimelist-scrappind-a-decade-of-anime)

## Want to run the script without knowing much about Python ?
### Requisites
You only need to install [Python]( https://www.python.org/downloads/) and its following modules:
* [Requests](https://docs.python-requests.org/en/latest/user/install/#install) 
* [BeautifulSoup4](https://www.crummy.com/software/BeautifulSoup/bs4/doc/#installing-beautiful-soup)
* [Numpy](https://numpy.org/install/)
* [Pandas](https://pandas.pydata.org/docs/getting_started/install.html)

### Run it
When you will run the script, follow the instructions in the command prompt.
Beware: scraping large temporal range might be a bit RAM intensive (800 MB for 2021 to 2010)

This is may not be the fastest way to scrap MAL (30s to scrap all 2020 anime content with 15 seconds of sleep time to avoid making MAL mad at me)

# MyAnalizer
Want to visualize the data you have just scraped ? Here it is !

## Want to run it ?
### Requisites
Previous requisites  
A csv file with the data you scraped before  
Change the path in the script until I take the time to prompt for it  

### Run it
When you will run the script, follow the instructions in the command prompt.

### Example of results

![Evolution of the anime production from 1970 to 2021](https://github.com/Gumpy-Q/MALscraPy/blob/main/production%2070%20to%2021.png)
![Source of the anime adaptation from 2000 to 2021](https://github.com/Gumpy-Q/MALscraPy/blob/main/source%2000%20to%2021.png)
![New anime length from 1990 to 2021](https://github.com/Gumpy-Q/MALscraPy/blob/main/episode%20new%2090%20to%2021.png)
![Continued anime length from 1990 to 2021](https://github.com/Gumpy-Q/MALscraPy/blob/main/episode%20continue%2090%20to%2021.png)


### Known issue
When showing the plot from IDLE or python command prompt, the legends don't appear. It works in a Notebook and with Spyder.
