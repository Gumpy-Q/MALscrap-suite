# -*- coding: utf-8 -*-
"""
Created on Thu Apr  8 09:32:36 2021

@author: qgump
"""

import pandas as pd
import numpy as np

import matplotlib.pyplot as plt
from matplotlib import style

import seaborn as sb

seasons=['winter','spring','summer','fall']
anime_types=['TV (New)','TV (Continuing)','Special','OVA','ONA','Movie']
style.use('ggplot') 

path='Data/MAL-all-from-winter1970-to-spring2021.csv'

raw=pd.read_csv(path)

raw['release-year']=raw['release-year'].astype(int) #je leur redonne le type integer qui saute souvent...
raw['episodes']=raw['episodes'].astype(int)



season_analyze=raw.value_counts(['release-year','release-season','type']).reset_index(name='count') #value count créé un index avec entrée tout le dataframe... il faut le reset et lui donner le bon nom
min_year=int(input('year to start data: '))
max_year=int(input('year to end data: '))

select_years=season_analyze[(season_analyze['release-year']<max_year) & (season_analyze['release-year']>min_year)]

years=np.linspace(select_years['release-year'].min(),select_years['release-year'].max(),select_years['release-year'].max()-select_years['release-year'].min()+1).astype(int)
maxcount=10+select_years.groupby(['release-year','release-season']).sum().max()[0]

fig, axes = plt.subplots(2,2,)
axes = axes.flatten()

bottom={'years':years,'cumul':[0]*len(years)}
bottom=pd.DataFrame(bottom)

for season,ax in zip(seasons,axes): #permet de faire varier ensemble les deux
    df_season=select_years[select_years['release-season']==season].sort_values('release-year')
    bottom['cumul']=[0]*len(years)
    print('--------------'+season)
    for anime_type in anime_types:
        
        df_type=df_season[df_season['type']==anime_type]
        df_type.reset_index(drop=True, inplace=True)
        print(anime_type)
        if len(df_type)!=len(bottom):
            temp_bottom=pd.merge(bottom,df_type,left_on='years',right_on='release-year')
                                    
            ax.bar(df_type['release-year'],df_type['count'],label=anime_type,bottom=temp_bottom['cumul'])
            
            temp_bottom['cumul']=temp_bottom['cumul']+temp_bottom['count']
            
            for year,cumul in zip(temp_bottom['years'],temp_bottom['cumul']):
                bottom.loc[bottom['years']==year,['cumul']]=cumul
            
        else:
            ax.bar(df_type['release-year'],df_type['count'],label=anime_type,bottom=bottom['cumul'])
            bottom['cumul']=bottom['cumul']+df_type['count']
        
        
        ax.ticklabel_format(style='plain',axis='x')
        ax.set_ylabel('count')
        ax.set_title(season)
        ax.axis(ymax=maxcount+5)
        ax.axis(xmax=select_years['release-year'].max()+1,xmin=select_years['release-year'].min()-1)
        ax.tick_params('x',labelrotation=45)
        ax.ticklabel_format(axis='x', style='plain', useOffset=False)
        handles, labels = ax.get_legend_handles_labels()
        # try:
        #     bottom=bottom+df_type['count']
        # except:
        #     bottom=bottom[:-1]+df_type['count']

fig.legend(handles, labels, bbox_to_anchor=(1,0.6), loc="upper left",fontsize='small')
fig.tight_layout()
fig.show()
input('press key')    
    