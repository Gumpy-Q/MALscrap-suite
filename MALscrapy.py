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
import PySimpleGUI as sg
from sys import exit


seasons=["winter","spring","summer","fall"]
formatting=['title','MAL_id','type','studio','release-season','release-year','realase-date','source-material','episodes']
anime_types=['TV (New)','TV (Continuing)','ONA','OVA','Movie','Special']

default_url='https://myanimelist.net/anime/season'
sg.theme('DefaultNoMoreNagging')

layout=[[sg.Text("This script is going to scrap anime informations from MyAnimeList for a period of time you will determine later.")],
[sg.Text('____________________________')],
[sg.Text('Data will be retrieved in this format:')],
[[sg.Text('  ')] + [sg.Text(h+'  |') for h in formatting]],
[sg.Text('____________________________')],
[sg.Text("A little reminder: \n Winter starts in january \n Spring starts in april \n Summer starts in july \n Fall starts in october")],
[sg.OK()]]
window = sg.Window('Introduction', layout)
window.read()
window.close()

                #SECTION 2 CHOICES
#choose start year. I choose to limite the range to 1917 (first recorded anime on MAL) to present year+1
begin=time.time()

datavalid=False
while datavalid==False:
    layout = [[sg.Text('From which year do you want to scrap ? ')],
            [sg.Text('Must be YYYY in range [1917;'+str(time.localtime().tm_year+1)+']')],
            [sg.Text('From'),sg.Spin([i for i in range(1917,time.localtime().tm_year+2)], initial_value=time.localtime().tm_year-10),sg.Text('season'),sg.Combo(seasons,default_value='winter')], 
            [sg.OK(), sg.Cancel()]] 
    window = sg.Window('Start point selection', layout)
    event, values = window.read()
    window.close()

  
    if event==sg.WIN_CLOSED or event=='Cancel':
         exit()
         
    start_year=values[0]
    start_season=values[1]
    start_season_index=seasons.index(start_season)
    
    try:
        start_year=int(start_year) #check if input is integer without breaking
        if start_year<1917 or start_year>time.localtime().tm_year+1:
            sg.popup('Invalid input. Must be YYYY in range [1917;'+str(time.localtime().tm_year+1)+']')
        else:
            datavalid=True
    except:
        sg.popup('Invalid input. Must be YYYY in range [1917;'+str(time.localtime().tm_year+1)+']')

        
datavalid=False
while datavalid==False:
    layout = [[sg.Text('Until which year do you want to scrap ? ')],
            [sg.Text('Must be YYYY in range [1917;'+str(time.localtime().tm_year+1)+']')],
            [sg.Text('Until'),sg.Spin([i for i in range(start_year,time.localtime().tm_year+2)], initial_value=start_year),sg.Text('season'),sg.Combo(seasons,default_value='fall')], 
            [sg.OK(), sg.Cancel()]] 
    window = sg.Window('End point selection', layout)
    event, values = window.read()
    window.close()
    
    if event==sg.WIN_CLOSED or event=='Cancel':
         exit()
         
    end_year=values[0]
    end_season=values[1]
    end_season_index=seasons.index(end_season)
    
    try:
        end_year=int(end_year) #check if input is integer without breaking
        if end_year<1917 or end_year<start_year:
            sg.popup('Invalid input. Must be YYYY in range ['+start_year+';'+str(time.localtime().tm_year+1)+']')
        elif end_year==start_year:
            if start_season_index<=end_season_index: #position of end season must be greater than position of start season or equal
                datavalid=True
            else:
                sg.popup('Invalid input. End and start in same the year but end season is sooner than start.')
            
        else:
            datavalid=True
    except:
        sg.popup('Invalid input. Must be YYYY in range [1917;'+str(time.localtime().tm_year+1)+']')


anime_choose=['all']+anime_types
type_to_scrap=[]
datavalid=False
while datavalid==False:
    layout = [[sg.Text('Which type of content do you want to scrap ? ')],
            [sg.Combo(anime_choose,default_value='all')], 
            [sg.OK(), sg.Cancel()]]
    window = sg.Window('Choosing anime type', layout)
    event, values = window.read()
    window.close()
    
    if event==sg.WIN_CLOSED or event=='Cancel':
         exit()
         
    type_chosen=values[0]
    
    if type_chosen in anime_types:
       type_to_scrap.append(type_chosen)
       datavalid=True       
    elif type_chosen=="all":
       type_to_scrap=anime_types
       datavalid=True    
    else:
       sg.popup('Invalid input. Must be all or (be careful of case !): ')
       print(anime_types)
    
print('____________________________')

layout = [[sg.Text('How many seconds between two requests ? ')],
          [sg.Text('WARNING fast requests might get your IP ban (I used 2 seconds to build my datasets)')],
          [sg.Slider(range=(0,10),default_value=2,orientation='horizontal')],
          [sg.OK(), sg.Cancel()]]
window = sg.Window('Choosing anime type', layout)
event, values = window.read()
window.close()

if event==sg.WIN_CLOSED or event=='Cancel':
         exit()
    
sleep_time=values[0]



                #SECTION 3 scrapper fonction
def seasonscrap(season,year,anime_type):
    url=default_url+"/"+str(year)+'/'+season    #url to scrap
    headers=({'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:53.0) Gecko/20100101 Firefox/53.0','Accept-Language':'fr-FR,q=0.5'})
    r=requests.get(url,headers)
    soup=BeautifulSoup(r.content,'html.parser')
    
    season_scrap={}
    for key in formatting:
        season_scrap[key]=[]  #initializing the dictionary
    
    season_types=soup.find_all('div',{'class':'anime-header'}) #anime-header has the name of each section for anime type
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
                ID=''.join(filter(lambda i: i.isdigit(), ID)) #ID can have different length thus I will only take digit character
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
                    season_scrap['episodes'].append(int(0))
                
                
            print('Finish scraping '+season_type.find('div',{'class':'anime-header'}).string+' of '+season+' '+str(year))
            print('____________________________')
        else: 
            continue
    
    print('Script will sleep for '+str(sleep_time) +'  seconds')
    time.sleep(sleep_time)
    print('anime for this season: '+str(pd.DataFrame(season_scrap).shape[0]))
    return season_scrap



                #SECTION 4 COMPILATION OF SCRAPING
years=np.arange(start_year,end_year+1,1) #building a vector of years from start to end year
scrap=pd.DataFrame(dict.fromkeys(formatting,[])) #initializing my dictionary

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

scrap.reset_index(drop=True, inplace=True) #reset l'index qui est chamboulé par le concat
pd.to_numeric(scrap['release-year'], downcast='integer')              
pd.to_numeric(scrap['episodes'], downcast='integer')    

              #SECTION 5 EXPORT
output=["html","json","csv","excel"]

compute_time=round(time.time()-begin)
sg.popup('time to scrap: '+str(timedelta(seconds=compute_time))) 
path='Data/'
filename='/MAL-'+type_chosen+'-from-'+start_season+str(start_year)+'-to-'+end_season+str(end_year)

datavalid=False
while datavalid==False:
    print(output)
    layout = [  [sg.Text('Path to save')],
            [sg.Input(default_text=path), sg.FolderBrowse()],
            [sg.Text('Output format:'),sg.Combo(output,default_value='csv')],
            [sg.OK(), sg.Cancel()]] 

    window = sg.Window('Get path', layout)

    event, values = window.read()
    window.close()

    if event==sg.WIN_CLOSED or event=='Cancel':
        exit()  
    
    path=values[0]
    output_format=values[1]
    if output_format in output:
        datavalid=True
        if output_format=='html':
            scrap.to_html(path+filename+'.html',index=False)
        elif output_format=='json':
            scrap.to_json(path+filename+'.json')
        elif output_format=='csv':
            scrap.to_csv(path+filename+'.csv',index=False)
        elif output_format=='excel':
            scrap.to_excel(path+filename+'.xlsx',index=False)
        else:
            print('Invalid Input.')

sg.popup('File saved as ' + path+filename+'.'+output_format)       
