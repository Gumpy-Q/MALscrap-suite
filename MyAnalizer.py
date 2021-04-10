# -*- coding: utf-8 -*-
"""
Created on Thu Apr  8 09:32:36 2021

@author: qgump
"""

import pandas as pd
import numpy as np
import time

import matplotlib.pyplot as plt
from matplotlib import style
import matplotlib.ticker as ticker
import matplotlib.colors as colors

import seaborn as sb

seasons=['winter','spring','summer','fall']
anime_types=['TV (New)','TV (Continuing)','Special','OVA','ONA','Movie']
style.use('ggplot') 

path='Data/MAL-all-from-winter1970-to-spring2021.csv'

raw=pd.read_csv(path)

raw['release-year']=raw['release-year'].astype(int) #I make sure they are integer as sometime it's interpreted as float
raw['episodes']=raw['episodes'].astype(int)

font='xx-large'
enlarge_fig=(15,10)

def production(df,min_year,max_year,anitypes):
    
    season_analyze=df.value_counts(['release-year','release-season','type']).reset_index(name='count') #count occurence and build the dataframe with a new column 'count'

    select_years=season_analyze[(season_analyze['release-year']<=max_year) & (season_analyze['release-year']>=min_year)] #remove years out of study scope
    
    years=np.linspace(select_years['release-year'].min(),select_years['release-year'].max(),select_years['release-year'].max()-select_years['release-year'].min()+1).astype(int) #I want a list of the years
    
    fig, axes = plt.subplots(2,2,figsize=enlarge_fig) #building a subplot for the 4 seasons
    axes = axes.flatten()
    

    bottom=pd.DataFrame({'years':years,'cumul':[0]*len(years)})#this data frame will accumulate the value to build the stacked barplot
    ymax=0
    
    for season,ax in zip(seasons,axes): #Season and plot goes together so I zip them
        df_season=select_years[select_years['release-season']==season].sort_values('release-year') #reducing the DataFrame to the season studied
        bottom['cumul']=[0]*len(years) #initialize bottom for each season
        print('--------------'+season)
        
        for anime_type in anitypes:
            df_type=df_season[df_season['type']==anime_type]
            df_type.reset_index(drop=True, inplace=True)
            print(anime_type)
            
            if len(df_type)!=len(bottom):
                temp_bottom=pd.merge(bottom,df_type,left_on='years',right_on='release-year') #if there is a lack of type of anime for a season, I reduce the bottom dataframe to an extract of it (if not shape mis shape between count and bottom)
                                        
                ax.bar(df_type['release-year'],df_type['count'],label=anime_type,bottom=temp_bottom['cumul'])
                
                temp_bottom['cumul']=temp_bottom['cumul']+temp_bottom['count'] #Create the cumul for the temp bottom
                
                for year,cumul in zip(temp_bottom['years'],temp_bottom['cumul']):
                    bottom.loc[bottom['years']==year,['cumul']]=cumul #put the value in temp bottom to the actual bottom
                
            else:
                ax.bar(df_type['release-year'],df_type['count'],label=anime_type,bottom=bottom['cumul'])
                bottom['cumul']=bottom['cumul']+df_type['count'] #way easier when each year are full
            
            
            ax.set_ylabel('count',fontsize=font)
            ax.xaxis.label.set_size(font)
            ax.set_title(season,fontsize=font)
            ax.axis(xmax=select_years['release-year'].max()+1,xmin=select_years['release-year'].min()-1)
            ax.tick_params('x',labelrotation=45, labelsize=font)
            ax.tick_params('y', labelsize=font)
            ax.xaxis.set_major_locator(ticker.MultipleLocator(base=round((max_year-min_year)/5)))
            ax.ticklabel_format(axis='x', style='plain', useOffset=False) #If I don't do this plt want to put the label to engineering notation
            handles, labels = ax.get_legend_handles_labels() #I store the legend
        
        ymax=max(bottom['cumul'].max(),ymax) #after each season I retrieve the maximum value to limit plot axis
        
    for ax in axes:
        ax.axis(ymax=ymax+5) #And then I set the limit
    
    fig.suptitle('Evolution of the production',fontsize=font)
    fig.tight_layout()
    fig.legend(handles, labels, bbox_to_anchor=(1,0.6), loc="upper left",fontsize='small')

    return fig

def episode(df,min_year,max_year):
    select_year=df[(df['type']=='TV (New)') & (df['episodes']>0) & (df['release-year']>=min_year) & (df['release-year']<=max_year)] #Limit my dataframe
    
    fig, ax =plt.subplots()
    ax=sb.violinplot(x='release-year',y='episodes',data=select_year,bw=.05,cut=0, scale='width',inner='quartile',orientation='h') 
    ax.set_xticklabels(ax.get_xticklabels(),rotation=45)
    ax.set(ylim=(0,60))
    ax.xaxis.set_major_locator(ticker.MultipleLocator(base=round((max_year-min_year)/10))) # I want to limit the number of label shown
    
    fig.tight_layout()
    return fig    

def sauce(df,min_year,max_year,anitypes):
    
    if len(anitypes) == 6:
        anitypes=['TV (New)', 'Special', 'OVA', 'ONA', 'Movie']
        
    select_years=df[(df['release-year']<=max_year) & (df['release-year']>=min_year)] #remove years out of study scope
    select_years=select_years[select_years['type'].isin(anitypes)]
    
    select_years.loc[select_years['source-material'] == '-', 'source-material'] = "Unknown in MAL"
    
    select_years=select_years.value_counts(['release-year','type','source-material']).reset_index(name='count')
    
    select_sum=select_years.groupby(['release-year','type'])['count'].sum().reset_index(name='sum')
    select_years=pd.merge(select_years,select_sum,on=('release-year','type'))
    select_years['percent']=select_years['count']/select_years['sum']
    
    # select_years=select_years[select_years['percent']>0.05]
    
    sauces=select_years['source-material'].unique()    
    
    colors_list = list(colors._colors_full_map.values())
    random_list=np.random.choice(np.arange(len(colors_list)), len(sauces),replace=False)
    random_color=[]
    for color in random_list:
        random_color.append(colors_list[color])
    
    years=np.linspace(select_years['release-year'].min(),select_years['release-year'].max(),select_years['release-year'].max()-select_years['release-year'].min()+1).astype(int) #I want a list of the years
    
    for year in years:
        df_year=select_years[select_years['release-year']==year]
        for anitype in anitypes:
            df_type=df_year[df_year['type']==anitype]
            for sauce in sauces:
                if sauce not in df_type['source-material'].values:
                    add_sauce=pd.DataFrame({'release-year':[year],'type':[anitype],'source-material':[sauce],'count':[0],'sum':[0],'percent':[0]})
                    select_years=pd.concat([select_years,add_sauce])
                    select_years.reset_index(drop=True,inplace=True)


    bottom=pd.DataFrame({'years':years,'cumul':[0]*len(years)})#this data frame will accumulate the value to build the stacked barplot
    font='medium' 
                       
    if len(anitypes)==5:
        fig, axes = plt.subplots(2,3,figsize=enlarge_fig) #building a subplot for the 5 anime type
        axes = axes.flatten()
        
        for anime_type,ax in zip(anitypes,axes): #Season and plot goes together so I zip them
            df_type=select_years[select_years['type']==anime_type].sort_values('release-year') #reducing the DataFrame to the season studied I need the year to be at the right order for the stacking
            bottom['cumul']=[0]*len(years) #initialize bottom for each season
            print('--------------'+anime_type)
            
            for sauce,color in zip(sauces,random_color):
                df_sauce=df_type[df_type['source-material']==sauce]
                df_sauce.reset_index(drop=True, inplace=True)
                print(sauce)
                
                if len(df_sauce)!=len(bottom):
                    temp_bottom=pd.merge(bottom,df_sauce,left_on='years',right_on='release-year') #if there is a lack of type of anime for a season, I reduce the bottom dataframe to an extract of it (if not shape mis shape between count and bottom)
                                            
                    ax.bar(df_sauce['release-year'],df_sauce['percent'],label=sauce,bottom=temp_bottom['cumul'],color=color)
                    
                    temp_bottom['cumul']=temp_bottom['cumul']+temp_bottom['percent'] #Create the cumul for the temp bottom
                    
                    for year,cumul in zip(temp_bottom['years'],temp_bottom['cumul']):
                        bottom.loc[bottom['years']==year,['cumul']]=cumul #put the value in temp bottom to the actual bottom
                    
                else:
                    ax.bar(df_sauce['release-year'],df_sauce['percent'],label=sauce,bottom=bottom['cumul'],color=color)
                    bottom['cumul']=bottom['cumul']+df_sauce['percent'] #way easier when each year are full
                
                ax.set_ylabel('percent',fontsize=font)
                ax.xaxis.label.set_size(font)
                ax.set_title(anime_type,fontsize=font)
                ax.axis(xmax=select_years['release-year'].max()+1,xmin=select_years['release-year'].min()-1)
                ax.tick_params('x',labelrotation=45, labelsize=font)
                ax.tick_params('y', labelsize=font)
                ax.axis(ymax=1)
                ax.ticklabel_format(axis='x', style='plain', useOffset=False) #If I don't do this plt want to put the label to engineering notation
                ax.xaxis.set_major_locator(ticker.MultipleLocator(base=round((max_year-min_year)/5)))
                handles, labels = ax.get_legend_handles_labels() #I store the legend
    
    else:
        fig, ax = plt.subplots(1,1,figsize=enlarge_fig) #building a subplot for the one choosen
        df_type=select_years.sort_values('release-year') #reducing the DataFrame to the season studied I need the year to be at the right order for the stacking
        bottom['cumul']=[0]*len(years) #initialize bottom for each season
        print('--------------'+anitypes[0])
        
        for sauce,color in zip(sauces,random_color):
            df_sauce=df_type[df_type['source-material']==sauce]
            df_sauce.reset_index(drop=True, inplace=True)
            print(sauce)
            
            if len(df_sauce)!=len(bottom):
                temp_bottom=pd.merge(bottom,df_sauce,left_on='years',right_on='release-year') #if there is a lack of type of anime for a season, I reduce the bottom dataframe to an extract of it (if not shape mis shape between count and bottom)
                                        
                ax.bar(df_sauce['release-year'],df_sauce['percent'],label=sauce,bottom=temp_bottom['cumul'],color=color)
                
                temp_bottom['cumul']=temp_bottom['cumul']+temp_bottom['percent'] #Create the cumul for the temp bottom
                
                for year,cumul in zip(temp_bottom['years'],temp_bottom['cumul']):
                    bottom.loc[bottom['years']==year,['cumul']]=cumul #put the value in temp bottom to the actual bottom
                
            else:
                ax.bar(df_sauce['release-year'],df_sauce['percent'],label=sauce,bottom=bottom['cumul'],color=color)
                bottom['cumul']=bottom['cumul']+df_sauce['percent'] #way easier when each year are full
            
            ax.set_ylabel('percent',fontsize=font)
            ax.xaxis.label.set_size(font)
            ax.set_title(anitypes[0],fontsize=font)
            ax.axis(xmax=select_years['release-year'].max()+1,xmin=select_years['release-year'].min()-1)
            ax.tick_params('x',labelrotation=45, labelsize=font)
            ax.tick_params('y', labelsize=font)
            ax.axis(ymax=1)
            ax.ticklabel_format(axis='x', style='plain', useOffset=False) #If I don't do this plt want to put the label to engineering notation
            ax.xaxis.set_major_locator(ticker.MultipleLocator(base=round((max_year-min_year)/5)))
            handles, labels = ax.get_legend_handles_labels() #I store the legend
    
    fig.suptitle('Source of the adaptation',fontsize=font)          
    fig.tight_layout()
    fig.legend(handles, labels, bbox_to_anchor=(1,0.6), loc="upper left",fontsize='small')
    return fig

datavalid=False
while datavalid==False:
    print('____________________________')
    start_year=input("From which year do you want to visualize ? ")
    try:
        start_year=int(start_year) #check if input is integer without breaking
        if start_year<1917 or start_year>time.localtime().tm_year:
            print('Invalid input. Must be YYYY in range [1917;'+str(time.localtime().tm_year+1)+']')
        else:
            datavalid=True
    except:
        print('Invalid input. Must be YYYY in range [1917;'+str(time.localtime().tm_year+1)+']')
       
datavalid=False
while datavalid==False:
    print('____________________________')
    end_year=input("To which year do you want to visualize ? ")
    try:
        end_year=int(end_year)
        if end_year<start_year or end_year>time.localtime().tm_year:
            print('Invalid input. Must be YYYY in range ['+str(start_year)+';'+str(time.localtime().tm_year)+']')
        else:
            datavalid=True
    except:
        print('Invalid input. Must be YYYY in range ['+str(start_year)+';'+str(time.localtime().tm_year)+']')

print('____________________________')
print("This is the list of content you can find in MyAnimeList: ",anime_types)
type_to_viz=[]
datavalid=False
while datavalid==False:
    type_chosen=input("Write one type you want to visualize (be careful of case !) or all for all of them: ")
    if type_chosen in anime_types:
       type_to_viz.append(type_chosen)
       datavalid=True       
    elif type_chosen=="all":
       type_to_viz=anime_types
       datavalid=True    
    else:
       print('____________________________')
       print('Invalid input. Must be all or (be careful of case !): ')
       print(anime_types)


fig_prod=production(raw,start_year,end_year,type_to_viz)
fig_prod.show()

fig_sauce=sauce(raw,start_year,end_year,type_to_viz)
fig_sauce.show()

fig_ep=episode(raw,start_year,end_year)
fig_ep.show()

input('press key') 