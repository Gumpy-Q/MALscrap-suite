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
from datetime import timedelta
from sys import exit
import os

try:
    os.chdir("Data")
    path =os.getcwd()
except:
    os.chdir("/share/CACHEDEV1_DATA/Public/Jupyter/MAL_scrap/Data")
    path =os.getcwd()

seasons=["winter","spring","summer","fall"]
formatting=['title','MAL_id','type','studio','release-season','release-year','release-date','source-material','genres','themes','demographics','episodes','score','members']
anime_types=['TV (New)','TV (Continuing)','ONA','OVA','Movie','Special']

default_url='https://myanimelist.net/anime/season'

cur_month=time.localtime().tm_mon
cur_year=time.localtime().tm_year
#A little reminder:  Winter starts in january Spring starts in april  Summer starts in july Fall starts in october


                #SECTION 2 CHOICES

begin=time.time() #Take the time value to give total computation time later
datavalid=False

if cur_month>9 :
    end_season="summer"
elif cur_month>6 :
    end_season="spring"
elif cur_month>3 :
    end_season="winter"
else :
    end_season="fall"
    cur_year-=1
     

end_year=cur_year
end_season_index=seasons.index(end_season) 

print("-----------------------------------------------------------------------------")
print("Scraped during "+end_season+" "+str(end_year))
print("-----------------------------------------------------------------------------")

while datavalid==False:
         
    start_year=end_year-1
    start_season="fall"
    start_season_index=seasons.index(start_season) 
    
    try:
        start_year=int(start_year) #check if input is integer without breaking
        if start_year<1917 or start_year>time.localtime().tm_year+1:
            print('Invalid input. Must be YYYY in range [1917;'+str(time.localtime().tm_year)+']')
        
        elif end_year==start_year:
            
            if start_season_index<=end_season_index: #position of end season in seasons list must be greater than position of start season or equal
                datavalid=True
            else:
                print('Invalid input.\n End and start in same the year but end season is sooner than start.')        
        else:
            datavalid=True
    except:
        print('Invalid input. Must be YYYY in range [1917;'+str(time.localtime().tm_year)+']')   


#choose what kind of anime to scrap
type_to_scrap=anime_types
   
#choosing delay between season scrap
sleep_time=2



                #SECTION 3 scraper fonction
#This function scrap one season for anime type                
def seasonscrap(season,year,anime_type):
    url=default_url+"/"+str(year)+'/'+season    #url to scrap
    headers=({'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:53.0) Gecko/20100101 Firefox/53.0','Accept-Language':'fr-FR,q=0.5'})
    r=requests.get(url,headers)
    soup=BeautifulSoup(r.content,'html.parser')

    #initializing the dictionary    
    season_scrap={}
    for key in formatting:
        season_scrap[key]=[]  
    
    season_types=soup.find_all('div',{'class':'anime-header'}) #anime-header has the name of each section for anime type
           
    for season_type in season_types:    
        if season_type.string in anime_type: #I want to scrap only the type of anime choosen by user
            animes=season_type.find_next_siblings("div",attrs={'class': lambda e: e.startswith('js-anime') if e else False}) #This is the div of each anime. statswith can detect the div with a class starting with .... as MAL use different naming with the same start thankfully
            
            for anime in animes:
                #those are defined in the scraping
                season_scrap['type'].append(season_type.string)
                season_scrap['release-season'].append(season)
                season_scrap['release-year'].append(year)
                                
                #those are directly in the text of each anime
                season_scrap['title'].append(anime.find("h2",{'class':'h2_anime_title'}).text)

                #Those damn span class item...
                item_class=anime.find('div',{'class':'synopsis js-synopsis'}).find_all('div',{'class':'property'})                
                
                studios=[]
                for studio in item_class[0].find_all('span',{'class':'item'}):
                    studios.append(studio.text)
                season_scrap['studio'].append(studios)    
                
                season_scrap['source-material'].append(item_class[1].find('span',{'class':'item'}).text)
                                
                themes=[]
                demographics=''
                
                if len(item_class)==3:
                    if item_class[2].find('span',{'class':'caption'})=='Theme':
                        for theme in item_class[2].find_all('span',{'class':'item'}):
                            themes.append(theme.text)
                    if item_class[2].find('span',{'class':'caption'})=='Demographic':
                        demographics.append(item_class[2].find('span',{'class':'item'}).text)
                if len(item_class)==4:
                    for theme in item_class[2].find_all('span',{'class':'item'}):
                        themes.append(theme.text)
                    demographics=item_class[3].find('span',{'class':'item'}).text
                
                season_scrap['themes'].append(themes)    
                season_scrap['demographics'].append(demographics)
                
                
                ID=anime.find("h2",{'class':'h2_anime_title'}).find("a").get('href')[30:] #the id is in the url of the hypertext link on the name of the anime. The ID begins at position 30 in the link
                ID=ID[:ID.find('/')] #ID can have different length thus I will only take characters before the '/'
                season_scrap['MAL_id'].append(ID)
                
                #Release date exists in two formats: Mon. DD, YYYY, HH:MM (JST) or Mon. DD, YYYY
                #There is also a lot of spaces and \n so I remove them before extracting the date to a datetime object with strptime
                anime_info=anime.find('div',{'class':'info'}).find_all('span',{'class':'item'})   
                try:
                    release=datetime.strptime(anime_info[0].text.replace('  ','').replace('\n',''),'%b %d, %Y, %H:%M (JST)')
                except:
                    try:
                        release=datetime.strptime(anime_info.text.replace('  ','').replace('\n',''),'%b %d, %Y')    
                    except:
                        release=None
                        
                season_scrap['release-date'].append(release)
                
                anime_genres=[]
                genres=anime.find_all('span',{'class':'genre'})
                for genre in genres:
                    anime_genres.append(genre.text.replace('\n',''))
                    
                season_scrap['genres'].append(anime_genres)
                
                #I want only the number of episode/OVA/Movie, if it's not given then I return a 0 
                eps=''.join(filter(lambda i: i.isdigit(), anime_info[1].find_all('span')[0].text)) #Get only digit value in a list of char
                try:
                    season_scrap['episodes'].append(int(eps))
                except:
                    season_scrap['episodes'].append(int(0))
                
                score=anime.find('div',{'title':'Score'}).text.replace('\n','').replace(' ','')
                try:
                    season_scrap['score'].append(float(score))
                except:
                    season_scrap['score'].append(float(0))
                
                #adapt members from K and M notation to integer
                members=anime.find('div',{'class':'scormem-item member'}).text.replace(',','').replace(' ','').replace('\n','')
                if 'K' in members:
                    members=int(float(members[:-1])*(10**3))
                elif 'M' in members:
                    members=int(float(members[:-1])*(10**6))
                else:
                    members=int(members)
                try:
                    season_scrap['members'].append(members)
                except:
                    season_scrap['members'].append(int(0))                
                
            print('Finished scraping '+season_type.string+' of '+season+' '+str(year))
        else: 
            continue
    print('____________________________')
    print('anime for this season: '+str(pd.DataFrame(season_scrap).shape[0]))
    print('Script will sleep for '+str(sleep_time) +'  seconds')
    print('____________________________')
    return season_scrap



                #SECTION 4 COMPILATION OF SCRAPING
years=np.arange(start_year,end_year+1,1) #building a vector of years from start to end year
scrap=pd.DataFrame(dict.fromkeys(formatting,[])) #initializing my DataFrame

season_scraped=0

#I need to give and test the seasons I want to scrape depending if: start year, end year, start=end
for year in years:   
    if year==start_year:
        
        if year==end_year:
            seasons_to_scrap=seasons[start_season_index:end_season_index+1] #if start=end then I just want the season between
        else:
            seasons_to_scrap=seasons[start_season_index:] #I remove the season before start season for start year

    elif year==end_year:
        seasons_to_scrap=seasons[:end_season_index+1] #I remove season after end season if end year
    
    else:
        seasons_to_scrap=seasons #For other years between start and end, I want all of them
        
    for season_to_scrap in seasons_to_scrap:
        #show progress of scraping
             
        df_n=pd.DataFrame(seasonscrap(season_to_scrap,year,type_to_scrap)) #I bluid a DataFrame around my data freshly scraped

        season_scraped+=1
        

        scrap=pd.concat([scrap,df_n],ignore_index=True) #add the new data to the end of the data Frame
        
        time.sleep(sleep_time)
              

latest_filename="/MAL-all-latest.csv"

df0=pd.read_csv(path+latest_filename)

    

df=pd.concat([df0,scrap])
df.drop_duplicates(subset=["MAL_id","release-year","release-season"], keep='last', inplace=True, ignore_index=True)    

if len(df["type"].unique())==6:
    type_chosen="all"
else:
    type_chosen="custom"

end_year=int(df["release-year"].max())
start_year=int(df["release-year"].min())
start_season=df["release-season"].head(1).values[0]
end_season=df["release-season"].tail(1).values[0]

filename='/MAL-'+type_chosen+'-from-'+start_season+str(start_year)+'-to-'+end_season+str(end_year)


df.to_csv(path+filename+'.csv',index=False)
df.to_csv(path+latest_filename,index=False)        

print('File saved as \n' + path+''+filename+'.csv')
print('File saved as \n' + path+''+latest_filename)