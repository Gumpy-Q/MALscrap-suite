# -*- coding: utf-8 -*-
#crazy-gump
"""
Created on Fri Mar  4 21:23:02 2022

@author: qgump
"""

import requests
import pandas as pd
pd.options.mode.chained_assignment = None
from bs4 import BeautifulSoup
import numpy as np
import time
import PySimpleGUI as sg
from sys import exit

sg.theme('DefaultNoMoreNagging')
seasons=["winter","spring","summer","fall"]


            #SECTION 1 building the friend list
layout = [  [sg.Text('Who is the user you want to know their friends tastes ?')],
        [sg.Input()],
        [sg.OK(), sg.Cancel()]] 

window = sg.Window('Get path', layout)

event, values = window.read()
window.close()

if event==sg.WIN_CLOSED or event=='Cancel':
    exit()  

username=values[0]
friendlist=[]

formatting=['title','MAL_id','type','release-season','release-year',username+' score','friends_mean_score','nb_who_watched_it','friend_who_watched_it','type']
scrap=pd.DataFrame(dict.fromkeys(formatting,[]))

headers=({'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:53.0) Gecko/20100101 Firefox/53.0','Accept-Language':'fr-FR,q=0.5'})
r=requests.get('https://myanimelist.net/profile/'+username+'/friends',headers)
soup=BeautifulSoup(r.content,'html.parser')

friends=soup.find_all('div',{'class':'di-tc va-t pl8 data'})

for friend in friends:
    friendlist.append(friend.find('a').text)
    
friendlist.append(username)
    
                #SECTION 2 Choosing the time period
#choose start year and season. I choose to limit the range from 1917 (first recorded anime on MAL) to present year+1
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

#choose end year and season. range from start year to present year+1        
datavalid=False
while datavalid==False:
    layout = [[sg.Text('Until which year do you want to scrap ? ')],
            [sg.Text('Must be YYYY in range ['+str(start_year)+';'+str(time.localtime().tm_year+1)+']')],
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
            
            if start_season_index<=end_season_index: #position of end season in seasons list must be greater than position of start season or equal
                datavalid=True
            else:
                sg.popup('Invalid input.\n End and start in same the year but end season is sooner than start.')
            
        else:
            datavalid=True
    except:
        sg.popup('Invalid input. Must be YYYY in range [1917;'+str(time.localtime().tm_year+1)+']')



#choosing delay between season scrap
layout = [[sg.Text('How many seconds between two requests ? ')],
          [sg.Text('WARNING fast requests might get your IP ban (I used 2 seconds to build my datasets)')],
          [sg.Slider(range=(0,10),default_value=2,orientation='horizontal')],
          [sg.OK(), sg.Cancel()]]
window = sg.Window('IP ban mitigation', layout)
event, values = window.read()
window.close()

if event==sg.WIN_CLOSED or event=='Cancel':
         exit()
    
sleep_time=values[0]



                #SECTION 3 scraper fonction
#This function scrap one season for anime type                
def friendseasonscrap(season,year,user):
    url='https://myanimelist.net/animelist/'+user+'?season_year='+str(year)+'&season='+str(season)
    headers=({'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:53.0) Gecko/20100101 Firefox/53.0','Accept-Language':'fr-FR,q=0.5'})
    r=requests.get(url,headers)
    soup=BeautifulSoup(r.content,'html.parser')

    user_list=str(soup.find('table',{'class':'list-table'}))
    user_list=user_list[user_list.find('data-items='):user_list.find('<tbody')] #get the json data
    user_list=user_list.replace('>\n','').replace('data-items=','').replace(chr(39),'').replace('&quot;',chr(34)) #replace the character that would prevent to read as json

    #dictionnary that will be merged with the final list
    friendict={}
    for key in formatting:
        friendict[key]=[]      
    
    
    if len(user_list)>0: #Check if the user list is empty
        #removing final and first double quote for some case
        if user_list[0]==chr(34) :
            user_list=user_list[1:-1]
               
        user_list=pd.read_json(user_list)
        
        #Loop in the animes inside the json
        for ind in user_list.index:
            #Remove the 0 score as they can also be a non filled value
            if user_list['score'][ind] > 0:
                ID=user_list['anime_id'][ind]
                
                #check if the current list is empty
                if len(scrap)>0:
                    if ID in scrap['MAL_id'].values: #check if the the anime is part of the current friend list data
                        
                        if user!=username:                            
                            scrap.loc[scrap['MAL_id']==ID,'friends_mean_score']+=user_list['score'][ind]
                            scrap.loc[scrap['MAL_id']==ID,'nb_who_watched_it']+=1
                            scrap.loc[scrap['MAL_id']==ID,username+' score']=None
                            scrap.loc[scrap['MAL_id']==ID,'friend_who_watched_it']+=user+';'
                        else:
                            scrap.loc[scrap['MAL_id']==ID,username+' score']=user_list['score'][ind]
                            
                    else: #if it's not then add every info
                        if user!=username: 
                            friendict['friends_mean_score'].append(int(user_list['score'][ind]))
                            friendict[username+' score'].append(None)
                            friendict['nb_who_watched_it'].append(1)
                            friendict['friend_who_watched_it'].append(user+';')
                        else:
                            friendict[username+' score'].append(int(user_list['score'][ind])) 
                            friendict['friends_mean_score'].append(None)
                            friendict['nb_who_watched_it'].append(0)  
                            friendict['friend_who_watched_it'].append(None)
                            
                        friendict['MAL_id'].append(ID)
                        friendict['release-year'].append(year)
                        friendict['release-season'].append(season)
                        friendict['title'].append(user_list['anime_title'][ind])
                        friendict['type'].append(user_list['anime_media_type_string'][ind])        
                
                else:
                    if user!=username: 
                        friendict['friends_mean_score'].append(int(user_list['score'][ind]))
                        friendict[username+' score'].append(None)
                        friendict['nb_who_watched_it'].append(1)
                        friendict['friend_who_watched_it'].append(user+';')
                    else:
                        friendict[username+' score'].append(int(user_list['score'][ind])) 
                        friendict['friends_mean_score'].append(None)
                        friendict['nb_who_watched_it'].append(0) 
                        
                    friendict['MAL_id'].append(ID)
                    friendict['release-year'].append(year)
                    friendict['release-season'].append(season)
                    friendict['title'].append(user_list['anime_title'][ind])
                    friendict['type'].append(user_list['anime_media_type_string'][ind])
                                       
    return friendict


nbfriend=len(friendlist)
years=np.arange(start_year,end_year+1,1) #building a vector of years from start to end year
layout = [[sg.Text('Current progress')],
          [sg.Output(size=(80,12))],
          [sg.ProgressBar(nbfriend*4*(1+end_year-start_year), orientation='h', size=(40, 12), key='progressbar')], #build a progress bar /!\ not accurate as it will just do number of year * 4 (seasons)
          [sg.Cancel()]]

window = sg.Window('Progress', layout)
progress_bar = window['progressbar']
season_scraped=0



        #SECTION 4 scrapper in friend list
for friend in friendlist:
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
            event,values=window.read(timeout=5+sleep_time)
            if event==sg.WIN_CLOSED or event=='Cancel':
                window.close()
                exit()
            
            test=friendseasonscrap(season_to_scrap,year,friend)
            df_n=pd.DataFrame(test) #I bluid a DataFrame around my data freshly scraped
    
            print(friend +' anime list for '+ str(season_to_scrap)+' '+str(year))
    
            season_scraped+=1
            progress_bar.UpdateBar(season_scraped)
            window.refresh()
            
            scrap=pd.concat([scrap,df_n],ignore_index=True)
               
            time.sleep(sleep_time)
            
window.close()

for ind in scrap.index:
    if scrap['nb_who_watched_it'][ind]>0:
        scrap['friends_mean_score'][ind]=scrap['friends_mean_score'][ind]/scrap['nb_who_watched_it'][ind]

scrap=scrap.sort_values(by=['friends_mean_score'],ascending=False) 

        #SECTION 5 Save the results
output=["html","json","csv","xlsx"]
filename='/MAL-friends-'+username+'-from-'+start_season+str(start_year)+'-to-'+end_season+str(end_year)

#choosing the output format and its directory
datavalid=False
while datavalid==False:    
    
    layout = [  [sg.Text('Path to save')],
            [sg.Input(), sg.FolderBrowse()],
            [sg.Text('Output format:'),sg.Combo(output,default_value='xlsx')],
            [sg.OK(), sg.Cancel()]] 
    
    window = sg.Window('Get path', layout)
    
    event, values = window.read()
    window.close()
    
    if event==sg.WIN_CLOSED or event=='Cancel':
        exit()  
    
    path=values[0]
    output_format=values[1]
    
    try:
        if output_format=='html':
            scrap.to_html(path+filename+'.html',index=False)
        elif output_format=='json':
            scrap.to_json(path+filename+'.json')
        elif output_format=='csv':
            scrap.to_csv(path+filename+'.csv',index=False)
        elif output_format=='xlsx':
            scrap.to_excel(path+filename+'.xlsx',index=False)
        datavalid=True
    except:
        sg.popup('Unable to save at this path')
        
textfile = open(path+'/'+username+"_friend list.txt", "w")
textfile.write(username + " friends list: \n")

for friend in friendlist[:-1]:
    textfile.write(friend + "\n")
textfile.close()

sg.popup('File saved as \n' + path+''+filename+'.'+output_format)  