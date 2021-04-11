# MALscraPy
Want to scrap MAL for specific seasons ? Here it is  
Access to last data on my Kaggle [here](https://www.kaggle.com/crazygump/myanimelist-scrappind-a-decade-of-anime)

## Want run the script without knowing much about Python ?
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

### Known issue
When showing the plot from IDLE or python command prompt, the legends don't appear. It works in a Notebook and with Spyder.
