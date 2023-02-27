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
from sys import exit
import matplotlib.pyplot as plt
import seaborn as sb
import os

try:
    os.chdir("Data")
    path =os.getcwd()
except:
    os.chdir("/share/CACHEDEV1_DATA/Public/Jupyter/MAL_scrap/Data")
    path =os.getcwd()

font='xx-large'
lgd_position='center right'
adjust={'bottom':0.11,'right':0.82,'wspace':0.35} #This array is used to adjust the limit of my 'normal' plots
enlarge_fig=(18,10) #This is the size of my figures

seasons=["winter","spring","summer","fall"]

cur_month=time.localtime().tm_mon
cur_year=time.localtime().tm_year

            #SECTION 1 building the friend list


username=input("username of MAL user: ")
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


while datavalid==False:
         
    start_year=input("Start year as XXXX: ")
    start_season=input("Start season, input as winter or spring or summer or fall: ")
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



#choosing delay between season scrap   
sleep_time=1



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
                if ID in scrap['MAL_id'].values: #check if the the anime is part of the current friend list data

                    if user!=username:                            
                        scrap.loc[scrap['MAL_id']==ID,'friends_mean_score']+=user_list['score'][ind]
                        scrap.loc[scrap['MAL_id']==ID,'nb_who_watched_it']+=1
                        scrap.loc[scrap['MAL_id']==ID,username+' score']=None
                        scrap.loc[scrap['MAL_id']==ID,'friend_who_watched_it']+=user+';'
                    else:
                        scrap.loc[scrap['MAL_id']==ID,'friends_mean_score']+=user_list['score'][ind]
                        scrap.loc[scrap['MAL_id']==ID,username+' score']=user_list['score'][ind]
                        scrap.loc[scrap['MAL_id']==ID,'friend_who_watched_it']+=user+';'
                        scrap.loc[scrap['MAL_id']==ID,'nb_who_watched_it']+=1

                else: #if it's not then add every info
                    if user!=username: 
                        friendict['friends_mean_score'].append(int(user_list['score'][ind]))
                        friendict[username+' score'].append(None)
                        friendict['nb_who_watched_it'].append(1)
                        friendict['friend_who_watched_it'].append(user+';')
                    else:
                        friendict[username+' score'].append(int(user_list['score'][ind])) 
                        friendict['friends_mean_score'].append(int(user_list['score'][ind]))
                        friendict['nb_who_watched_it'].append(1)  
                        friendict['friend_who_watched_it'].append(user+';')
                        

                    friendict['MAL_id'].append(ID)
                    friendict['release-year'].append(year)
                    friendict['release-season'].append(season)
                    friendict['title'].append(user_list['anime_title'][ind])
                    friendict['type'].append(user_list['anime_media_type_string'][ind])
                    
                    
                                       
    return friendict

#This function is showing the repartition of anime's score

#This function is showing the repartition of anime's score
def score_vs_friend(df): 
    
    df=df[df['score']>0]
    df=df[df['friends_mean_score']>0]
    #count the number of anime under the mean MAL score
    total=0
    hipster=0
    for my_score, mal_score in zip(df['score'],df['friends_mean_score']):
        if  my_score>mal_score:
            total+=1
            hipster+=1
        else:
            total+=1
                
    hipster_score=int(100*hipster/total)
    
    minmal_score=int(df['friends_mean_score'].min())
    minuser_score=int(df['score'].min())
    maxmal_score=int(df['friends_mean_score'].max())
    maxuser_score=int(df['score'].max())

    tickmax=max(maxmal_score,maxuser_score)
    tickmin=min(minmal_score,minuser_score)    
    
    #aspect_ratio=(1+maxmal_score-minmal_score)/(1+maxuser_score-minuser_score)+
    aspect_ratio=1

    fig, ax = plt.subplots(figsize=(15*aspect_ratio,15)) #building a subplot for the one choosen
    ax=sb.scatterplot(x='friends_mean_score',y='score',data=df,hue='type_y',s=70) 
    ax.plot([0,1,2,3,4,5,6,7,8,9,10],[0,1,2,3,4,5,6,7,8,9,10], c='black') 
        
    ax.tick_params('x', labelsize=font)
    ax.tick_params('y', labelsize=font)
    ax.set_ylabel('MAL score',fontsize=font)
    ax.set_xlabel('Yokanime MAL friends mean score',fontsize=font)
    ax.set(xlim=(tickmin-0.5,tickmax+0.5))
    ax.set(ylim=(tickmin-0.5,tickmax+0.5))
    ax.set_box_aspect(1/aspect_ratio) 
    
    signature(fig)
    fig.suptitle('MAL score vs Yokanime MAL friends means: '+str(hipster_score)+'% of the score are lower than MAL score',fontsize=font) 

    
    fig.tight_layout()
    fig.subplots_adjust(bottom=adjust['bottom'])
    
    fig.savefig(path+'/'+username+'_friends_score_vs_MAL'+'-'+str(start_year)+'-'+str(end_year))
    fig.show()
    
    return fig

def signature(fig):
    fig.text(0,0.005,' Data collected with MALscraPy & Plot made with Otakulyzer | Scripts available at http://github.com/Gumpy-Q',fontsize=font, backgroundcolor='grey',style='italic',color='white')

def signature(fig):
    fig.text(0,0.005,' Data collected with MALscraPy & Plot made with Otakulyzer | Scripts available at http://github.com/Gumpy-Q',fontsize=font, backgroundcolor='grey',style='italic',color='white')


nbfriend=len(friendlist)
years=np.arange(start_year,end_year+1,1) #building a vector of years from start to end year

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
            
            test=friendseasonscrap(season_to_scrap,year,friend)
            df_n=pd.DataFrame(test) #I bluid a DataFrame around my data freshly scraped
    
            print(friend +' anime list for '+ str(season_to_scrap)+' '+str(year))
    
            season_scraped+=1
            
            scrap=pd.concat([scrap,df_n],ignore_index=True)
               
            time.sleep(sleep_time)

for ind in scrap.index:
    if scrap['nb_who_watched_it'][ind]>0:
        scrap['friends_mean_score'][ind]=scrap['friends_mean_score'][ind]/scrap['nb_who_watched_it'][ind]

scrap=scrap.sort_values(by=['friends_mean_score'],ascending=False) 

        #SECTION 5 Save the results
output=["html","json","csv","xlsx"]
filename='/MAL-vs-friends-'+username+'-from-'+start_season+str(start_year)+'-to-'+end_season+str(end_year)

malraw=pd.read_csv('MAL-all-latest.csv')

for ind in test.index:
    scrap['MAL_id'][ind]=int(scrap['MAL_id'][ind])

scrap=pd.merge(malraw,scrap,on='MAL_id')
scrap=scrap[scrap['friends_mean_score']>0]
scrap=scrap.drop_duplicates('MAL_id')

#choosing the output format and its directory
scrap.to_excel(path+filename+'.xlsx',index=False)

score_vs_friend(scrap)
        
textfile = open(path+'/'+username+"_friend list.txt", "w")
textfile.write(username + " friends list: \n")

for friend in friendlist[:-1]:
    textfile.write(friend + "\n")
textfile.close()

print('File saved as \n' + path+''+filename+'.xlsx')  
