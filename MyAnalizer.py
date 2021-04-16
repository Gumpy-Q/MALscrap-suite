# -*- coding: utf-8 -*-
"""
Created on Thu Apr  8 09:32:36 2021

@author: qgump
"""

import pandas as pd
import time

import matplotlib.pyplot as plt
from matplotlib import style
import matplotlib.ticker as ticker
from matplotlib.patches import Patch
from matplotlib.ticker import PercentFormatter
from matplotlib.ticker import MaxNLocator

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
picked_colors=['#e6194B', '#3cb44b', '#ffe119', '#4363d8', '#f58231', '#911eb4', '#42d4f4', '#f032e6', '#bfef45', '#fabed4', '#469990', '#dcbeff', '#9A6324', '#fffac8', '#800000', '#aaffc3', '#808000', '#ffd8b1', '#000075', '#a9a9a9', '#ffffff', '#000000']


def stackbarcolor(df_plot,cat_list,ax,plot_name,colors_list,cat_key,tosum_key,ylabel_name,max_year,min_year,ymax=0):
    df_plot['bottom']=0    
    
    for cat_value,color in zip(cat_list,colors_list): #I want to attribute a color for each source that will be consistent for each type of anime
            print('implementing '+cat_value)
            df_cat=df_plot[df_plot[cat_key]==cat_value] #reducing the the source
            df_cat.reset_index(drop=True, inplace=True)
                                  
            ax.bar(df_cat['release-year'],df_cat[tosum_key],label=cat_value,bottom=df_cat['bottom'],color=color,edgecolor='black')
            
            #sum percent at bottom for each year/anime-type configuration so the graph become stacked                
            for year in df_cat['release-year']:
                df_plot.loc[df_plot['release-year']==year,['bottom']]=df_cat.loc[df_cat['release-year']==year,[tosum_key]].values+df_cat.loc[df_cat['release-year']==year,['bottom']].values 
                
            ax.set_ylabel(ylabel_name,fontsize=font)
            ax.xaxis.label.set_size(font)
            ax.set_title(plot_name,fontsize=font)
            ax.axis(xmax=df_plot['release-year'].max()+1,xmin=df_plot['release-year'].min()-1)
            ax.tick_params('x',labelrotation=45, labelsize=font)
            ax.tick_params('y', labelsize=font)
            ax.set(xlim=(min_year-1,max_year+1))
            ax.ticklabel_format(axis='x', style='plain', useOffset=False) #If I don't do this plt want to put the label to engineering notation
            ax.xaxis.set_major_locator(MaxNLocator(integer=True,nbins=7,prune='both')) #give instruction how to handle the tick label: integer, nb of label, remove egde label
            
    ymax=max(df_plot['bottom'].max(),ymax) #after each season I retrieve the maximum value to limit plot axis
    
    return ymax

def production_season(df,min_year,max_year,anitypes,color_list): #To vizualize the sum of anime product each year for each season
    
    season_analyze=df.value_counts(['release-year','release-season','type']).reset_index(name='count') #count occurence and build the dataframe with a new column 'count'

    select_years=season_analyze[(season_analyze['release-year']<=max_year) & (season_analyze['release-year']>=min_year)] #remove years out of study scope
    select_years=select_years[select_years['type'].isin(anitypes)]
    
    picked_colors=color_list[0:len(anitypes)+1]
    
    custom_patches=[]

    fig, axes = plt.subplots(2,2,figsize=enlarge_fig) #building a subplot for the 4 seasons
    axes = axes.flatten()
    
    ymax=0
    
    #avoid colors mismatch when getting legend
    for color in picked_colors:
        custom_patches.append(Patch(facecolor=color, edgecolor='b')) 
    
    print('------------ plotting evolution of production by season ------------')
    
    for season,ax in zip(seasons,axes): #Season and plot goes together so I zip them
        df_season=select_years[select_years['release-season']==season].sort_values('release-year') #reducing the DataFrame to the season studied

        print('--------------'+season)
        
        ymax=stackbarcolor(df_season,anitypes,ax,season,picked_colors,'type','count','Count',max_year,min_year,ymax)
        
    for ax in axes:
        ax.axis(ymax=ymax+5) #And then I set the limit
        ax.ticklabel_format(axis='x', style='plain', useOffset=False)
    
    fig.text(0,-0.02,'Data collected with MALscraPy & Plot made with MyAnalizer | Scripts available at http://github.com/Gumpy-Q',fontsize=font, backgroundcolor='grey',style='italic',color='white')
    fig.suptitle('Evolution of the production',fontsize=font)
    fig.tight_layout()
    fig.legend(custom_patches, anitypes, bbox_to_anchor=(1,0.6), loc="upper left",fontsize=font)
    return fig

def production_year(df,min_year,max_year,anitypes,color_list): #To vizualize the sum of anime product each year for each season
    
    season_analyze=df.value_counts(['release-year','type']).reset_index(name='count') #count occurence and build the dataframe with a new column 'count'

    select_years=season_analyze[(season_analyze['release-year']<=max_year) & (season_analyze['release-year']>=min_year)] #remove years out of study scope
    select_years=select_years[select_years['type'].isin(anitypes)]
    
    picked_colors=color_list[0:len(anitypes)+1]  
    custom_patches=[]    
    #avoid colors mismatch when getting legend
    for color in picked_colors:
        custom_patches.append(Patch(facecolor=color, edgecolor='b'))
    
    print('------------ plotting evolution of production by year ------------')    
    
    fig, ax = plt.subplots(1,figsize=enlarge_fig) #building a subplot for the 4 seasons
    
    ymax=0
     
    df_year=select_years.sort_values('release-year') #reducing the DataFrame to the season studied
        
    ymax=stackbarcolor(df_year,anitypes,ax,'',picked_colors,'type','count','Number of anime aired',max_year,min_year,ymax)
        
    ax.axis(ymax=ymax+5) #And then I set the limit
    
    fig.text(0,-0.02,'Data collected with MALscraPy & Plot made with MyAnalizer | Scripts available at http://github.com/Gumpy-Q',fontsize=font, backgroundcolor='grey',style='italic',color='white')
    fig.suptitle('Evolution of the production',fontsize=font)
    fig.tight_layout()
    fig.legend(custom_patches, anitypes, bbox_to_anchor=(1,0.6), loc="upper left",fontsize=font)
    return fig

def episode(df,min_year,max_year,anitype,max_shown): #This function is showing the repartition of anime'lenght in the year
    select_year=df[(df['type']==anitype) & (df['episodes']>0) & (df['release-year']>=min_year) & (df['release-year']<=max_year)] #Limit my dataframe
    
    print('------------ plotting evolution of anime length ------------')
    
    fig, ax =plt.subplots(figsize=enlarge_fig)
    ax=sb.violinplot(x='release-year',y='episodes',data=select_year,bw=.05,cut=0, scale='width',inner='quartile',orientation='h') 
    ax.tick_params('x',labelrotation=45, labelsize=font)
    ax.tick_params('y', labelsize=font)
    ax.set_ylabel('Number of episodes per anime',fontsize=font)
    ax.xaxis.label.set_size(font)
    ax.set(ylim=(0,max_shown))
    ax.set_title('Repartion of anime length : '+ anitype,fontsize=font)
    ax.xaxis.set_major_locator(MaxNLocator(integer=True,nbins=12,prune='both')) #
    
    fig.text(0,-0.02,'Data collected with MALscraPy & Plot made with MyAnalizer | Scripts available at http://github.com/Gumpy-Q',fontsize=font, backgroundcolor='grey',style='italic',color='white') 
    fig.tight_layout()
    return fig    

def source(df,min_year,max_year,anitypes,color_list,thresold): 
        
    select_years=df[(df['release-year']<=max_year) & (df['release-year']>=min_year)] #remove years out of study scope
    select_years=select_years[select_years['type'].isin(anitypes)] 
    
    select_years.loc[select_years['source-material'] == '-', 'source-material'] = "Unknown in MAL" #replace the default value when source is not assigned to an anime
    
    select_years=select_years.value_counts(['release-year','type','source-material']).reset_index(name='count') #transform the long list to a count for each config
    
    #getting the sum and repartition for each release-year/type couple
    select_sum=select_years.groupby(['release-year','type'])['count'].sum().reset_index(name='sum')
    select_years=pd.merge(select_years,select_sum,on=('release-year','type')) 
    select_years['percent']=select_years['count']/select_years['sum']
    
    
    select_years.loc[select_years['percent']<(thresold/100),'source-material']='Other'
    select_years=select_years.groupby(['release-year','type','source-material'])['percent'].sum().reset_index(name='percent')
    
    
    #build a descending list by percent of source material
    sources=select_years.sort_values('percent',ascending=False)['source-material'].unique()    
       
    picked_colors=color_list[0:len(sources)]
     
    custom_patches=[]
    
    #avoid colors mismatch when getting legend
    for color in picked_colors:
        custom_patches.append(Patch(facecolor=color, edgecolor='b')) 
    
    print('plotting evolution of source material')    
                
    if len(anitypes)>1:
        fig, axes = plt.subplots(2,3,figsize=enlarge_fig) #building a subplot for the 6 anime types
        axes = axes.flatten()
        
        for anime_type,ax in zip(anitypes,axes): #Season and plot goes together so I zip them
            df_type=select_years[select_years['type']==anime_type].sort_values('release-year') #reducing the DataFrame to the season studied I need the year to be at the right order for the stacking
            print('--------------'+anime_type)
            
            stackbarcolor(df_type,sources,ax,anime_type,picked_colors,'source-material','percent','Part of the diffusion',max_year,min_year)
            for ax in axes:
                ax.set(ylim=(0,1))
                ax.yaxis.set_major_formatter(PercentFormatter(xmax=1, decimals=0, symbol='%', is_latex=False))
                
    else:
        fig, ax = plt.subplots(1,1,figsize=enlarge_fig) #building a subplot for the one choosen
        df_type=select_years.sort_values('release-year') #reducing the DataFrame to the season studied I need the year to be at the right order for the stacking
        anime_type=anitypes[0]
        print('--------------'+anime_type)
          
        stackbarcolor(df_type,sources,ax,anime_type,picked_colors,'source-material','percent','Part of the diffusion',max_year,min_year)
        ax.set(ylim=(0,1))
        ax.yaxis.set_major_formatter(PercentFormatter(xmax=1, decimals=0, symbol='%', is_latex=False))

    
    fig.text(0,-0.02,'Data collected with MALscraPy & Plot made with MyAnalizer | Scripts available at http://github.com/Gumpy-Q',fontsize=font, backgroundcolor='grey',style='italic',color='white')
    fig.suptitle('Source of the adaptation (if less than '+str(thresold)+'% -> Other)',fontsize=font)          
    fig.tight_layout()
    fig.legend(custom_patches, sources, bbox_to_anchor=(1,0.6), loc="upper left",fontsize=font)
    
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


fig_prod_m=production_season(raw,start_year,end_year,type_to_viz,picked_colors)
fig_prod_m.show()

fig_prod_y=production_year(raw,start_year,end_year,type_to_viz,picked_colors)
fig_prod_y.show()

fig_source=source(raw,start_year,end_year,type_to_viz,picked_colors,2.5)
fig_source.show()

fig_ep=episode(raw,start_year,end_year,'TV (New)',60)
fig_ep.show()

fig_ep=episode(raw,start_year,end_year,'TV (Continuing)',150)
fig_ep.show()

input('press Enter key') 