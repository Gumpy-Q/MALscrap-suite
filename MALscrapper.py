# -*- coding: utf-8 -*-
"""
Created on Tue Apr  6 14:06:41 2021

@author: qgump
"""
                #SECTION 1 INITIALIZATION
import requests
import pandas as pd
from bs4 import BeautifulSoup
import numpy as np
import time
from datetime import datetime

begin=time.time()
seasons=["winter","spring","summer","fall"]
formatting={'title':[],'MAL_id':[],'type':[],'studio':[],'release-season':[],'release-year':[],'realase-date':[],'source-material':[],'episodes':[]}
anime_types=['TV (New)','ONA','OVA','Movie','Special']

default_url='https://myanimelist.net/anime/season'

print("This script is going to scrap anime informations from MyAnimeList for a period of time you will determine later.")
print('____________________________')
print('Data will be retrieve in this format:')
print(formatting)
time.sleep(2)
print('____________________________')
print("A slight reminder: \n Winter starts in january \n Spring starts in april \n Summer starts in july \n Fall starts in october")
print('____________________________')

                #SECTION 2 CHOICES
#choose start year. I choose to limite the range to 1917 (first recorded anime on MAL) to present year+1
datavalid=False
while datavalid==False:
    print('____________________________')
    start_year=input("From which year do you want to scrap ? ")
    try:
        start_year=int(start_year) #check if input is integer without breaking
        if start_year<1917 or start_year>time.localtime().tm_year:
            print('Invalid input. Must be YYYY in range [1917;'+str(time.localtime().tm_year+1)+']')
        else:
            datavalid=True
    except:
        print('Invalid input. Must be YYYY in range [1917;'+str(time.localtime().tm_year+1)+']')

#season is an input I will check if in the season list
datavalid=False
while datavalid==False:
    print('____________________________')
    start_season=str(input("From which season of "+str(start_year)+" do you want to scrap ? ")).lower()
         
    if start_season in seasons:
        start_season_index=seasons.index(start_season) #I will need the position of start season in the list later
        datavalid=True
    else:
        print('Invalid input. Must be one of the following:')
        print(seasons)

#Check if end year is in the acceptable range
datavalid=False
while datavalid==False:
    print('____________________________')
    end_year=input("To which year do you want to scrap ? ")
    try:
        end_year=int(end_year)
        if end_year<start_year or end_year>time.localtime().tm_year:
            print('Invalid input. Must be YYYY in range ['+str(start_year)+';'+str(time.localtime().tm_year)+']')
        else:
            datavalid=True
    except:
        print('Invalid input. Must be YYYY in range ['+str(start_year)+';'+str(time.localtime().tm_year)+']')
 
#Check if end season is: in list, not earlier than start season if in the same year
datavalid=False
while datavalid==False:
    print('____________________________')
    end_season=input("To which season of "+str(start_year)+" do you want to scrap ? ").lower()
    
    if end_season in seasons:
        end_season_index=seasons.index(end_season)
        if start_year==end_year:
            if start_season_index<=end_season_index: #position of end season must be greater than position of start season or equal
                datavalid=True
            else:
                print('Invalid input. End and start in same year but end season is sooner than start.')
        else:
            datavalid=True
    else:
        print('Invalid input. Must be one of the following:')
        print(seasons)

print('____________________________')
print("This is the list of content you can find in MyAnimeList: ",anime_types)
type_to_scrap=[]

datavalid=False
while datavalid==False:
    type_chosen=input("Write one type you want to scrap (be careful of case !) or all for all of them: ")
    if type_chosen in anime_types:
       type_to_scrap=type_chosen
       datavalid=True       
    elif type_chosen=="all":
       type_to_scrap=anime_types
       datavalid=True    
    else:
       print('____________________________')
       print('Invalid input. Must be all or (be careful of case !): ')
       print(anime_types)
    
print('____________________________')

                #SECTION 3 scrapper fonction
def seasonscrap(season,year,anime_type):
    url=default_url+"/"+str(year)+'/'+season    #url to scrap
    headers=({'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:53.0) Gecko/20100101 Firefox/53.0','Accept-Language':'fr-FR,q=0.5'})
    r=requests.get(url,headers)
    soup=BeautifulSoup(r.content,'lxml')
    
    season_scrap=formatting #initializing the dictionary
    season_types=soup.find_all('div',{'class':'anime-header'}) #anime-header has the name of each section
    season_types_parent=[]
    for season_type in season_types:
        season_types_parent.append(season_type.parent) #but it's the parent which got all the anime div
        
    for season_type in season_types_parent:    
        if season_type.find('div',{'class':'anime-header'}).string in anime_type: #I want to scrap only the type of anime choosen by user
            animes=season_type.find_all("div",{"class":"seasonal-anime js-seasonal-anime"}) #This is the div of each anime
            for anime in animes:
                #those are directly in the text
                season_scrap['title'].append(anime.find("h2",{'class':'h2_anime_title'}).text) 
                season_scrap['studio'].append(anime.find("span",{'class':'producer'}).text)
                season_scrap['source-material'].append(anime.find("span",{'class':'source'}).text)
                
                #those are defined in the scraping
                season_scrap['type'].append(season_type.find('div',{'class':'anime-header'}).string)
                season_scrap['release-season'].append(season)
                season_scrap['release-year'].append(year)
                
                ID=anime.find("h2",{'class':'h2_anime_title'}).find("a").get('href')[30:35] #the id is in the url of the hypertext link on the name of the anime. The ID is in position 30 to 35 in the link
                ID=''.join(filter(lambda i: i.isdigit(), ID))
                season_scrap['MAL_id'].append(ID)
                #Realase date exists in two formats: Mon. DD, YYYY, HH:MM (JST) or Mon. DD, YYYY
                #There is also a lot of spaces and \n so I remove them before extracting the date to a datetime object with strptime
                try:
                    release=datetime.strptime(anime.find("span",{'class':'remain-time'}).text.replace('  ','').replace('\n',''),'%b %d, %Y, %H:%M (JST)')
                except:
                    try:
                        release=datetime.strptime(anime.find("span",{'class':'remain-time'}).text.replace('  ','').replace('\n',''),'%b %d, %Y')    
                    except:
                        release=None
                        
                season_scrap['realase-date'].append(release)
                
                #I want only the number of episode/OVA/Movie, if it's not given then I put a Null value 
                eps=''.join(filter(lambda i: i.isdigit(), anime.find("div",{'class':'eps'}).text))
                try:
                    season_scrap['episodes'].append(int(eps))
                except:
                    season_scrap['episodes'].append(None) #Null is None in Python
                
            print('Finish scraping '+season_type.find('div',{'class':'anime-header'}).string+' of '+season+' '+str(year))
            print('____________________________')
        else:
            continue
           
        time.sleep(5)
    return season_scrap

                #SECTION 4 COMPILATION OF SCRAPING
years=np.arange(start_year,end_year+1,1) #building a vector of years from start to end year
scrap=pd.DataFrame(formatting) #initializing my dictionary

#I need to give the seasons I want to scrape depending if: start year, end year, start=end
for year in years:
    if year==start_year:
        if year==end_year:
            seasons_to_scrap=seasons[start_season_index:end_season_index+1] #if start=end then I just want the season between

        else:
            seasons_to_scrap=seasons[start_season_index:] #I remove the season before start season for start year

    elif year==end_year:
        seasons_to_scrap=seasons[:end_season_index+1] #I remove season after end season if end year

    else:
        seasons_to_scrap=seasons #For other years betweend start and end, I want all of them
        
    for season_to_scrap in seasons_to_scrap:
        df_n=pd.DataFrame(seasonscrap(season_to_scrap,year,type_to_scrap)) #I bluid a DataFrame around my data
        scrap=pd.concat([scrap,df_n]) #add the new data to the end of the data Frame

                #SECTION 5 EXPORT
output=["html","json","csv","excel","mysql"]

datavalid=False
while datavalid==False:
    print(output)
    output_format=input("Which output format do you want from the list upside: ").lower()
    if output_format in output:
        datavalid=True
        if output_format=='html':
            scrap.to_html('Data/MAL-from-'+start_season+str(start_year)+'-to-'+end_season+str(end_year)+'.html')
        elif output_format=='json':
            scrap.to_json('Data/MAL-from-'+start_season+str(start_year)+'-to-'+end_season+str(end_year)+'.json')
        elif output_format=='csv':
            scrap.to_csv('Data/MAL-from-'+start_season+str(start_year)+'-to-'+end_season+str(end_year)+'.csv')
        elif output_format=='excel':
            scrap.to_excel('Data/MAL-from-'+start_season+str(start_year)+'-to-'+end_season+str(end_year)+'.xlsx')
        elif output_format=='mysql':
            scrap.to_mysql('Data/MAL-from-'+start_season+str(start_year)+'-to-'+end_season+str(end_year)+'.mysql')
        else:
            print('Invalid Input.')
compute_time=round(time.time()-begin)
print(str(datetime.timedelta(seconds=compute_time)) +' time to scrap' )        
