# -*- coding: utf-8 -*-
"""
Created on Thu Apr  8 09:32:36 2021

@author: qgump
"""
                #SECTION 1 INITIALIZION
import pandas as pd
import time
import numpy as np

import matplotlib.pyplot as plt
from matplotlib import style
from matplotlib.patches import Patch
from matplotlib.ticker import PercentFormatter
from matplotlib.ticker import MaxNLocator

import seaborn as sb
import requests
from bs4 import BeautifulSoup

import PySimpleGUI as sg

from sys import exit
from ast import literal_eval


seasons=['winter','spring','summer','fall']
anime_types=['TV (New)','TV (Continuing)','Special','OVA','ONA','Movie']
plot_list=['Watching seasons','Watching years','Studio watching','TV (New) length','Score distribution','Score vs viewers','Score vs MAL means','Source repartition','Genre evolution','Theme evolution']

formatting=['series_animedb_id','my_score','my_status']

style.use('ggplot')
sg.theme('DefaultNoMoreNagging') 

font='xx-large'
lgd_position='center right'
adjust={'bottom':0.11,'right':0.82,'wspace':0.35} #This array is used to adjust the limit of my 'normal' plots
enlarge_fig=(18,10) #This is the size of my figures
nb_ticks=7
rotation_ticks=45
contrast_colors=['#e6194B', '#3cb44b', '#ffe119', '#4363d8', '#f58231', '#911eb4', '#42d4f4', '#f032e6', '#bfef45', '#fabed4', '#469990', '#dcbeff', '#9A6324', '#fffac8', '#800000', '#aaffc3', '#808000', '#ffd8b1', '#000075', '#a9a9a9', '#ffffff', '#000000']


                #SECTION 2 FUNCTIONS DEFINITION
#Only a simple function to open any format of DataFramable content
def opener(path,ext):
    if ext=='csv':
        df=pd.read_csv(path)
    elif ext=="json":
        df=pd.read_json(path)
    elif ext=="html":
        df=pd.read_html(path)
    elif ext=="xlsx":
        df=pd.read_Excel(path)
    elif ext=="xml":
        df=pd.read_xml(path)
        
    return df

#This function scrap one season for anime type                
def userseasonscrap(season,year,user):
    scrap=pd.DataFrame(dict.fromkeys(formatting,[]))
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
                if (ID in scrap['series_animedb_id'].values)==False: #check if the the anime is part of the current friend list data
                    friendict['my_score'].append(int(user_list['score'][ind])) 
                    friendict['series_animedb_id'].append(ID)
                    if user_list['status'][ind]==2:
                        friendict['my_status'].append('Completed')
                    if user_list['status'][ind]==4:
                        friendict['my_status'].append('Dropped')
                    if user_list['status'][ind]==1:
                        friendict['my_status'].append('Watching')
                    if user_list['status'][ind]==3:
                        friendict['my_status'].append('On-Hold')
                                       
    return friendict

#This function can create a stackbar plot in a given figure
def stackbarcolor(df_plot,cat_list,ax,plot_name,colors_list,cat_key,tosum_key,ylabel_name,max_year,min_year,ymax=1):
    df_plot['bottom']=0 #intiate the bottom to stack with    
    
    for cat_value,color in zip(cat_list,colors_list): #I want to attribute a color for each source that will be consistent for each category
            print('implementing '+cat_value)
            df_cat=df_plot[df_plot[cat_key]==cat_value] #reducing data to only a value in the category to discriminate
            df_cat.reset_index(drop=True, inplace=True) 
                                  
            ax.bar(df_cat['release-year'],df_cat[tosum_key],label=cat_value,bottom=df_cat['bottom'],color=color,edgecolor='black') #add a category to the plot
            
            #sum percent at bottom for each year/anime-type configuration so the graph become stacked                
            for year in df_cat['release-year']:
                df_plot.loc[df_plot['release-year']==year,['bottom']]=df_cat.loc[df_cat['release-year']==year,[tosum_key]].values+df_cat.loc[df_cat['release-year']==year,['bottom']].values 
                
    ax.set_ylabel(ylabel_name,fontsize=font)
    ax.xaxis.label.set_size(font)
    ax.set_title(plot_name,fontsize=font)
    ax.axis(xmax=df_plot['release-year'].max()+1,xmin=df_plot['release-year'].min()-1)
    ax.tick_params('x',labelrotation=rotation_ticks, labelsize=font)
    ax.tick_params('y', labelsize=font)
    ax.ticklabel_format(axis='x', style='plain', useOffset=False) #If I don't do this plot wants to put the label to engineering notation
    ax.xaxis.set_major_locator(MaxNLocator(integer=True,nbins=nb_ticks,prune='both')) #give instruction how to handle the tick label: integer, nb of label, remove egde label
            
    ymax=max(df_plot['bottom'].max(),ymax) #after each season I retrieve the maximum value to limit plot axis
    
    return ymax

def signature(fig):
    fig.text(0,0.005,' Data collected with MALscraPy & Plot made with Otakulyzer | Scripts available at http://github.com/Gumpy-Q',fontsize=font, backgroundcolor='grey',style='italic',color='white')

def colo_patch(cat,color_list):
    contrast_colors=color_list[0:len(cat)+1]
    custom_patches=[]
    for color in contrast_colors:
        custom_patches.append(Patch(facecolor=color, edgecolor='b')) 
    
    return custom_patches

#To vizualize the sum of anime product each year for each season
def production_season(df,min_year,max_year,anitypes,color_list): 
    
    season_analyze=df.value_counts(['release-year','release-season','type']).reset_index(name='count') #count occurence and build the dataframe with a new column 'count'

    select_years=season_analyze[(season_analyze['release-year']<=max_year) & (season_analyze['release-year']>=min_year)] #remove years out of study scope
    select_years=select_years[select_years['type'].isin(anitypes)] #remove anime types not in selection

    #Building a legend with my selected colors    
    contrast_colors=color_list[0:len(anitypes)+1]
    custom_patches=[]
    for color in contrast_colors:
        custom_patches.append(Patch(facecolor=color, edgecolor='b')) 


    fig, axes = plt.subplots(2,2,figsize=enlarge_fig) #building a subplot for the 4 seasons
    axes = axes.flatten()
    
    ymax=0
    
    print('------------ plotting evolution of production by season ------------')
    
    for season,ax in zip(seasons,axes): #Season and plot go together so I zip them
        df_season=select_years[select_years['release-season']==season].sort_values('release-year') #reducing the DataFrame to the season studied

        print('--------------'+season)
        
        ymax=stackbarcolor(df_season,anitypes,ax,season,contrast_colors,'type','count','Number of anime watched',max_year,min_year,ymax)
        
    for ax in axes:
        ax.axis(ymax=ymax+5) #I set the limit with the value return by my function
        ax.ticklabel_format(axis='x', style='plain', useOffset=False)
    
    signature(fig)
    fig.suptitle('Evolution of '+username+' seasons viewing trend',fontsize=font)
    fig.legend(custom_patches, anitypes, loc=lgd_position,fontsize=font)
    
    fig.tight_layout()    
    fig.subplots_adjust(right=adjust['right'],bottom=adjust['bottom'],wspace=adjust['wspace'])
       
    fig.savefig(savepath+'/'+username+'_season_evolution-'+str(start_year)+'-'+str(end_year))
    fig.show()
    return fig

#To vizualize the sum of anime product each year
def production_year(df,min_year,max_year,anitypes,color_list): 
    
    select_years=df.drop_duplicates(subset=['title','release-year','type']) #remove TV duplicates notably for long runer with multiple apparition per year, only keep one/year.
    select_years=select_years.value_counts(['release-year','type']).reset_index(name='count') #count occurence and build the dataframe with a new column 'count'

    select_years=select_years[(select_years['release-year']<=max_year) & (select_years['release-year']>=min_year)] 
    select_years=select_years[select_years['type'].isin(anitypes)]
    
    
    custom_patches=[]
    custom_patches=colo_patch(anitypes,color_list)
    
    print('------------ plotting evolution of production by year ------------')    
    
    fig, ax = plt.subplots(1,figsize=enlarge_fig)
    
    ymax=0
     
    df_year=select_years.sort_values('release-year')
        
    ymax=stackbarcolor(df_year,anitypes,ax,'',contrast_colors,'type','count','Number of anime watched from this year',max_year,min_year,ymax)
        
    ax.axis(ymax=ymax+5) #I set the limit
    
    signature(fig)
    fig.suptitle('Evolution of '+username+' viewing trend',fontsize=font)
    fig.legend(custom_patches, anitypes, loc=lgd_position,fontsize=font)

    fig.tight_layout()    
    fig.subplots_adjust(right=adjust['right'],bottom=adjust['bottom'])
       
    fig.savefig(savepath+'/'+username+'_year_evolution'+str(start_year)+'-'+str(end_year))
    fig.show()

    return fig

#Give the evolution of the source material for each type of anime
def source(df,min_year,max_year,anitypes,color_list,thresold=0): 
        
    select_years=df[(df['release-year']<=max_year) & (df['release-year']>=min_year)] #remove years out of study scope
    select_years=select_years[select_years['type'].isin(anitypes)] 
    select_years=select_years.drop_duplicates(subset=['title','release-year','type']) #remove TV duplicates notably for long runer with multiple apparition per year, only keep one/year.
    
    select_years.loc[select_years['source-material'] == '-', 'source-material'] = "Unknown in MAL" #replace the default value when source is not assigned to an anime
    
    select_years=select_years.value_counts(['release-year','type','source-material']).reset_index(name='count') #transform the long list to a count for each config
    
    #getting the sum and repartition for each release-year/type couple
    select_sum=select_years.groupby(['release-year','type'])['count'].sum().reset_index(name='sum')
    select_years=pd.merge(select_years,select_sum,on=('release-year','type')) 
    select_years['percent']=select_years['count']/select_years['sum']
    
    #This thresold is useful to limit the kind of source which are not very used
    select_years.loc[select_years['percent']<(thresold/100),'source-material']='Other' 
    select_years=select_years.groupby(['release-year','type','source-material'])['percent'].sum().reset_index(name='percent') # The new 'other' are put together and  their repartition summed
    
    #build a descending list by percent of source material
    sources=select_years.sort_values('percent',ascending=False)['source-material'].unique()    

    custom_patches=[]
    custom_patches=colo_patch(sources,color_list)
    
    print('------------ plotting evolution of source material ------------')    
                
    if len(anitypes)>1:
        
        if len(anitypes)>4:
            fig, axes = plt.subplots(2,3,figsize=enlarge_fig) #building a subplot for the 6 anime types
            axes = axes.flatten()
        elif len(anitypes)==2:
            fig, axes = plt.subplots(1,2,figsize=enlarge_fig) #building a subplot for the 2 anime types
            axes = axes.flatten()
        else:
            fig, axes = plt.subplots(2,2,figsize=enlarge_fig) #building a subplot for the 4 anime types
            axes = axes.flatten()
            
        for anime_type,ax in zip(anitypes,axes): #Anime types and plots go together so I zip them
            df_type=select_years[select_years['type']==anime_type].sort_values('release-year') #I need the year to be at the right order for the stacking
            print('--------------'+anime_type)
            
            stackbarcolor(df_type,sources,ax,anime_type,contrast_colors,'source-material','percent','Part of the diffusion',max_year,min_year)
            for ax in axes:
                ax.set(ylim=(0,1))
                ax.yaxis.set_major_formatter(PercentFormatter(xmax=1, decimals=0, symbol='%', is_latex=False)) #Format the axis to percent format
                
    else:
        fig, ax = plt.subplots(1,1,figsize=enlarge_fig) #building a subplot for the one choosen
        df_type=select_years.sort_values('release-year') #I need the year to be at the right order for the stacking
        anime_type=anitypes[0]
        print('--------------'+anime_type)
          
        stackbarcolor(df_type,sources,ax,anime_type,contrast_colors,'source-material','percent','Part of the diffusion',max_year,min_year)
        ax.set(ylim=(0,1))
        ax.yaxis.set_major_formatter(PercentFormatter(xmax=1, decimals=0, symbol='%', is_latex=False))

    fig.legend(custom_patches, sources, loc=lgd_position,fontsize=font)
    signature(fig)
    fig.suptitle('Source of the adaptation (if less than '+str(thresold)+'% -> Other) watched by '+username,fontsize=font)          
   
    fig.tight_layout()    
    fig.subplots_adjust(right=adjust['right'],bottom=adjust['bottom'],wspace=adjust['wspace'])
       
    fig.savefig(savepath+'/'+username+'_source-'+str(start_year)+'-'+str(end_year))
    fig.show()
    
    return fig

#Plot the evolution of top 3 studios of each year 
def production_studio(df,min_year,max_year,anitypes,color_list): 
        
    select_years=df[(df['release-year']<=max_year) & (df['release-year']>=min_year)] #remove years out of study scope
    select_years=select_years[select_years['type'].isin(anitypes)] #limite to anime types
    select_years=select_years.drop_duplicates(subset=['title','release-year','type']) #remove TV duplicates notably for long runer with multiple apparition per year, only keep one/year.
    select_years['studio']=select_years['studio'].apply(lambda x: x.strip("[]").split(", "))
    select_years=select_years.explode('studio')
    select_years['studio']=select_years['studio'].apply(lambda x: x.strip("''"))
    
    #remove the anime with studio not registered in MAL
    select_years=select_years[select_years['studio'] != '          -' ] 
    select_years=select_years[select_years['studio'] != '-']
    
    select_years=select_years.value_counts(['release-year','type','studio']).reset_index(name='count') #transform the long list to a count for each config
    
    print('Selecting studios, please wait this is a long task')
    
    #Build the top 3 studio list of each year and put them in on unique list
    studios=[]
    for year in range(min_year,max_year+1):
        for anitype in anitypes:
            studio_list=select_years[(select_years['release-year']==year) & (select_years['type']==anitype)].sort_values('count',ascending=False)['studio'].head(3).values.tolist() #building the top 3 lists for each year and anime type
            for studio in studio_list:
                studios.append(studio[0:15])              
        
    studios = list(dict.fromkeys(studios))   #tricks to remove duplicate from a list
  
    custom_patches=[]
    custom_patches=colo_patch(studios,color_list)
        
    print('------------ plotting evolution of Studio watching ------------')    
               
    if len(anitypes)>1:
        
        if len(anitypes)>4:
            fig, axes = plt.subplots(2,3,figsize=enlarge_fig) #building a subplot for the 6 anime types
            axes = axes.flatten()
        elif len(anitypes)==2:
            fig, axes = plt.subplots(1,2,figsize=enlarge_fig) #building a subplot for the 2 anime types
            axes = axes.flatten()
        else:
            fig, axes = plt.subplots(2,2,figsize=enlarge_fig) #building a subplot for the 4 anime types
            axes = axes.flatten()
            
        for anime_type,ax in zip(anitypes,axes): #Season and plot go together so I zip them
            df_type=select_years[select_years['type']==anime_type].sort_values('release-year') #reducing the DataFrame to the anime types studied I need the year to be at the right order for the stacking
            print('--------------'+anime_type)
            
            ymax=stackbarcolor(df_type,studios,ax,anime_type,contrast_colors,'studio','count','Anime produced by',max_year,min_year)
            ax.axis(ymax=ymax+5) #I set the limit
            ax.ticklabel_format(axis='x', style='plain', useOffset=False)         
                
    else:
        fig, ax = plt.subplots(1,1,figsize=enlarge_fig) #building a subplot for the one choosen
        df_type=select_years.sort_values('release-year') #reducing the DataFrame to the season studied I need the year to be at the right order for the stacking
        anime_type=anitypes[0]
        print('--------------'+anime_type)
          
        ymax=stackbarcolor(df_type,studios,ax,anime_type,contrast_colors,'studio','count','Anime produced by',max_year,min_year)
        ax.axis(ymax=ymax+5) #I set the limit
        ax.ticklabel_format(axis='x', style='plain', useOffset=False)
        

    fig.legend(custom_patches, studios, loc=lgd_position,fontsize=font)
    signature(fig)
    fig.suptitle('Evolution of the production of '+username+' top 3 studios of each year',fontsize=font)          
   
    fig.tight_layout()    
    fig.subplots_adjust(right=adjust['right']-0.1,bottom=adjust['bottom'],wspace=adjust['wspace'])
       
    fig.savefig(savepath+'/'+username+'_studio-'+str(start_year)+'-'+str(end_year))
    fig.show()
    
    return fig


#This function is showing the repartition of anime's length in the year
def episode(df,min_year,max_year,anitype,max_shown): 
    select_years=df[(df['type']==anitype) & (df['episodes']>0) & (df['release-year']>=min_year) & (df['release-year']<=max_year)] #Limit my dataframe 
    select_years=select_years.drop_duplicates(subset=['title']) #remove TV duplicates notably for long runer with multiple apparition per year, only keep one/year.
    
    print('------------ plotting evolution of anime length ------------')
    
    fig, ax =plt.subplots(figsize=enlarge_fig)
    ax=sb.violinplot(x='release-year',y='episodes',data=select_years,bw_method=0.1,cut=0, density_norm='area',width=0.7,inner='stick',orient='v') 
    
    ax.tick_params('x',labelrotation=rotation_ticks, labelsize=font)
    ax.tick_params('y', labelsize=font)
    ax.set_ylabel('Number of episodes per anime watched',fontsize=font)
    ax.set_xlabel('Diffusion year',fontsize=font)
    ax.xaxis.label.set_size(font)
    ax.set(ylim=(0,max_shown))
    ax.set_title('Repartition of anime length watched by '+username+': '+ anitype,fontsize=font)
    ax.xaxis.set_major_locator(MaxNLocator(integer=True,nbins=nb_ticks,prune='both'))
    
    signature(fig)
    
    fig.tight_layout()    
    fig.subplots_adjust(bottom=adjust['bottom']+0.03)
    
    fig.savefig(savepath+'/'+username+'_episode_'+anitype+'-'+str(start_year)+'-'+str(end_year))
    fig.show()
    
    return fig  

#This function is showing the repartition of anime's score
def score_distribution(df,min_year,max_year,anitypes): 
    
    select_years=df[(df['release-year']>=min_year) & (df['release-year']<=max_year)] #Limit my dataframe
    select_years=select_years[select_years['type'].isin(anitypes)]
    select_years=select_years.drop_duplicates(subset=['title']) #remove TV duplicates notably for long runer with multiple apparition per year, only keep one/year.
    
    print('------------ plotting evolution score ------------')
    
    #Some year don't have any anime score for one type so I add a virtual one with 0 as score value
    for anime_type in anitypes:
        df_type=select_years[select_years['type']==anime_type]
        for year in range(min_year,max_year+1):
            if df_type[df_type['release-year']==year].shape[0]==0:
                select_years=pd.concat([select_years,pd.DataFrame([[0,year,anime_type]],columns=['my_score','release-year','type'])], ignore_index=True)

    
    if len(anitypes)>1:
        
        if len(anitypes)>4:
            fig, axes = plt.subplots(2,3,figsize=enlarge_fig) #building a subplot for the 6 anime types
            axes = axes.flatten()
        elif len(anitypes)==2:
            fig, axes = plt.subplots(1,2,figsize=enlarge_fig) #building a subplot for the 2 anime types
            axes = axes.flatten()
        else:
            fig, axes = plt.subplots(2,2,figsize=enlarge_fig) #building a subplot for the 4 anime types
            axes = axes.flatten()
            
        for anime_type,ax in zip(anitypes,axes): #anime types and plots go together so I zip them
            df_type=select_years[select_years['type']==anime_type] #reducing the DataFrame to the season studied I need the year to be at the right order for the stacking
            print('--------------'+anime_type)
            
            sb.violinplot(ax=ax,x='release-year',y='my_score',data=df_type,bw_method=0.1,cut=0, density_norm='area',width=0.7,inner='quartile',orient='v')

        for anime_type,ax in zip(anitypes,axes):
            ax.tick_params('x',labelrotation=rotation_ticks, labelsize=font)
            ax.tick_params('y', labelsize=font)
            ax.set_ylabel(username+' Score',fontsize=font)
            ax.set_xlabel('Diffusion year',fontsize=font)
            ax.xaxis.label.set_size(font)
            ax.set(ylim=(0,10))
            ax.set_title(anime_type,fontsize=font)
            ax.xaxis.set_major_locator(MaxNLocator(integer=True,nbins=nb_ticks,prune='both'))
    
    else:
        fig, ax = plt.subplots(1,1,figsize=enlarge_fig) #building a subplot for the one choosen
        df_type=select_years.sort_values('release-year') #reducing the DataFrame to the season studied I need the year to be at the right order for the stacking
        anime_type=anitypes[0]
        print('--------------'+anime_type)

        ax=sb.violinplot(x='release-year',y='my_score',data=df_type,bw_method=0.1,cut=0, density_norm='area',width=0.7,inner='quartile',orient='v') 
        
        ax.tick_params('x',labelrotation=rotation_ticks, labelsize=font)
        ax.tick_params('y', labelsize=font)
        ax.set_ylabel(username+' score',fontsize=font)
        ax.set_xlabel('Diffusion year',fontsize=font)
        ax.xaxis.label.set_size(font)
        ax.set(ylim=(0,10))
        ax.set_title(anime_type,fontsize=font)
        ax.xaxis.set_major_locator(MaxNLocator(integer=True,nbins=nb_ticks,prune='both')) 
    
    signature(fig)
    fig.suptitle(username+' score distribution',fontsize=font) 

    
    fig.tight_layout()    
    fig.subplots_adjust(bottom=adjust['bottom']+0.03)
    
    fig.savefig(savepath+'/'+username+'_score_distribution'+'-'+str(start_year)+'-'+str(end_year))
    fig.show()
    
    return fig

#Visualizing correlation between popularity and score
def score_viewers(df,min_year,max_year,anitypes):
    select_years=df[(df['release-year']<=max_year) & (df['release-year']>=min_year)] #remove years out of study scope
    select_years=select_years[select_years['type'].isin(anitypes)]
    select_years=select_years[(select_years['score']!=0) & (select_years['members']!=0)]
    select_years=select_years.drop_duplicates(subset=['title','release-year','type']) #remove TV duplicates notably for long runer with multiple apparition per year, only keep one/year.
    
    select_years=select_years[['my_score','members','type']]
      
    #Build a list of score range [0-4],[4-4.5],[4.5-5],...,[9.5-10]
    scores=[0]
    for i in range(0,10):
        scores+=[i+1]
 

    #get the maximum and minimum of members
    ymax=int(np.ceil(select_years['members'].max()))
    ymin=int(select_years['members'].min())
    
       
    select_years=select_years.sort_values('my_score')    

    print('------------ plotting score and viewers ------------')
    
    if len(anitypes)>1:
        
        if len(anitypes)>4:
            fig, axes = plt.subplots(2,3,figsize=enlarge_fig) #building a subplot for the 6 anime types
            axes = axes.flatten()
        elif len(anitypes)==2:
            fig, axes = plt.subplots(1,2,figsize=enlarge_fig) #building a subplot for the 2 anime types
            axes = axes.flatten()
        else:
            fig, axes = plt.subplots(2,2,figsize=enlarge_fig) #building a subplot for the 4 anime types
            axes = axes.flatten()
            
        for anime_type,ax in zip(anitypes,axes): #anime types and plots go together so I zip them
            df_type=select_years[select_years['type']==anime_type] #reducing the DataFrame to the season studied I need the year to be at the right order for the stacking
            print('--------------'+anime_type)
            
            sb.violinplot(ax=ax,x='my_score',y='members',data=df_type,bw_method=0.1,cut=0, density_norm='width',width=0.7,inner='quartile',orient='v')
            
            ax.tick_params('x',labelrotation=rotation_ticks, labelsize=font)
            ax.tick_params('y', labelsize=font)
            ax.set_ylabel('MAL Viewers',fontsize=font)
            ax.set_xlabel(username+' score',fontsize=font)
            ax.xaxis.label.set_size(font)        
            ax.set_title(anime_type,fontsize=font)
            
            #prepare for log scaling
            ax.set(ylim=((int(ymin/10**(len(str(ymin))-1)))*10**(len(str(ymin))-1),(1+int(ymax/10**(len(str(ymax))-1)))*10**(len(str(ymax))-1))) #limit axis with min and max logic for a log scale
            ax.set_yscale('log')
        
    else:
        fig, ax = plt.subplots(1,1,figsize=enlarge_fig) #building a subplot for the one choosen
       
        anime_type=anitypes[0]
        df_type=select_years[select_years['type']==anime_type]
        print('--------------'+anime_type)

        sb.violinplot(ax=ax,x='my_score',y='members',data=df_type,bw_method=0.1,cut=0, density_norm='width',width=0.7,inner='quartile',orient='v')
       
        ax.tick_params('x',labelrotation=rotation_ticks, labelsize=font)
        ax.tick_params('y', labelsize=font)
        ax.set_ylabel('MAL Viewers',fontsize=font)
        ax.set_xlabel(username+' score',fontsize=font)
        ax.xaxis.label.set_size(font)
        ax.set_title(anime_type,fontsize=font)

        ax.set(ylim=((int(ymin/10**(len(str(ymin))-1)))*10**(len(str(ymin))-1),(1+int(ymax/10**(len(str(ymax))-1)))*10**(len(str(ymax))-1)))
        ax.set_yscale('log')
    
    fig.suptitle(username+' score correlation to popularity '+str(min_year)+'-'+str(max_year),fontsize=font)
    signature(fig)
    
    fig.tight_layout()
    fig.subplots_adjust(bottom=adjust['bottom']+0.05,hspace=0.5)
    
    fig.savefig(savepath+'/'+username+'_score_viewers'+'-'+str(start_year)+'-'+str(end_year))
    fig.show()
    
    return fig    

#This function is showing the repartition of anime's score
def score_vs_world(df,min_year,max_year,anitypes): 
    
    select_years=df[(df['release-year']>=min_year) & (df['release-year']<=max_year)] #Limit my dataframe
    select_years=select_years[select_years['type'].isin(anitypes)]
    select_years=select_years.drop_duplicates(subset=['title']) #remove TV duplicates notably for long runer with multiple apparition per year, only keep one/year.
    
    print('------------ plotting your score vs the world (of MAL :p) ------------')
    
    #count the number of anime under the mean MAL score
    total=0
    hipster=0
    for my_score, mal_score in zip(select_years['my_score'],select_years['score']):
        if  my_score>mal_score:
            total+=1
            hipster+=1
        else:
            total+=1
                
    hipster_score=int(100*hipster/total)
    
    minmal_score=int(select_years['score'].min())
    minuser_score=int(select_years['my_score'].min())
    maxmal_score=int(select_years['score'].max())
    maxuser_score=int(select_years['my_score'].max())

    tickmax=max(maxmal_score,maxuser_score)
    tickmin=min(minmal_score,minuser_score)    
    
    #aspect_ratio=(1+maxmal_score-minmal_score)/(1+maxuser_score-minuser_score)+
    aspect_ratio=1

    fig, ax = plt.subplots(figsize=(15*aspect_ratio,15)) #building a subplot for the one choosen
    ax=sb.scatterplot(x='score',y='my_score',data=select_years,hue='type',s=70) 
    ax.plot([0,1,2,3,4,5,6,7,8,9,10],[0,1,2,3,4,5,6,7,8,9,10], c='black') 
        
    ax.tick_params('x', labelsize=font)
    ax.tick_params('y', labelsize=font)
    ax.set_ylabel(username+' score',fontsize=font)
    ax.set_xlabel('MAL mean score',fontsize=font)
    ax.set(xlim=(tickmin-0.5,tickmax+0.5))
    ax.set(ylim=(tickmin-0.5,tickmax+0.5))
    ax.set_box_aspect(1/aspect_ratio) 
    
    signature(fig)
    fig.suptitle(username+' score vs MAL users means: '+str(hipster_score)+'% of the score are above the mean',fontsize=font) 

    
    fig.tight_layout()
    fig.subplots_adjust(bottom=adjust['bottom'])
    
    fig.savefig(savepath+'/'+username+'_score_vs_MAL'+'-'+str(start_year)+'-'+str(end_year))
    fig.show()
    
    return fig

def genres_evolution(df,min_year,max_year,anitypes,color_list,thresold=10):
    df=df.drop_duplicates(subset=['title','release-year','type'])
    df=df[['release-year','type','genres']]
    select_years=df[(df['release-year']<=max_year) & (df['release-year']>=min_year)] #remove years out of study scope
    select_years=select_years[select_years['type'].isin(anitypes)]
    
    select_years=select_years.dropna(subset=['genres'])
    
    select_years['genres']=select_years['genres'].apply(literal_eval) #transform a string to a list
    
    select_years=select_years.explode('genres') #seperate list value to their own row
    select_years=select_years.value_counts(['release-year','type','genres']).reset_index(name='count')
    
    #Build the top genres list of each year and put them in on unique list
    genre_list=[]
    for year in range(min_year,max_year+1):
        for anitype in anitypes:
            top_genres=select_years[(select_years['release-year']==year) & (select_years['type']==anitype)].sort_values('count',ascending=False)['genres'].head(thresold).values.tolist() #building the top 3 lists for each year and anime type
            for genre in top_genres:
                genre_list.append(genre)  
                
    genre_list = list(dict.fromkeys(genre_list))
    
    select_years=select_years[select_years['genres'].isin(genre_list)]
    
    data_add=[]
      
    for year in range(min_year,max_year+1):
        for anitype in anitypes:
            for genre in genre_list:
            
                if select_years[(select_years['type']==anitype) & (select_years['release-year']==year) & (select_years['genres']==genre)].empty:
                    data_add.append([year,anitype,genre,0])
                
    df_add=pd.DataFrame(data_add,columns=['release-year','type','genres','count'])
    select_years=pd.concat([select_years,df_add], ignore_index=True)
    select_years=select_years.sort_values('genres')

    
    print('------------ plotting evolution of genre by year ------------')    
    
    custom_patches=contrast_colors[0:select_years['genres'].nunique()]
    
    if len(anitypes)>1:
        
        if len(anitypes)>4:
            fig, axes = plt.subplots(2,3,figsize=enlarge_fig) #building a subplot for the 6 anime types
            axes = axes.flatten()
        elif len(anitypes)==2:
            fig, axes = plt.subplots(1,2,figsize=enlarge_fig) #building a subplot for the 2 anime types
            axes = axes.flatten()
        else:
            fig, axes = plt.subplots(2,2,figsize=enlarge_fig) #building a subplot for the 4 anime types
            axes = axes.flatten()
            
        for anime_type,ax in zip(anitypes,axes): #anime types and plots go together so I zip them
            df_type=select_years[select_years['type']==anime_type] #reducing the DataFrame to the season studied I need the year to be at the right order for the stacking
            print('--------------'+anime_type)
            
            
            sb.lineplot(ax=ax,x='release-year',y='count',hue='genres',data=df_type,linewidth = 2, legend=False, palette=custom_patches,ci=None)
            
            ax.set(ylim=0)
            ax.xaxis.set_major_locator(MaxNLocator(integer=True))
            ax.set(xlim=(min_year,max_year))
            ax.set_ylabel('Number of anime with the genre',fontsize=font)
            ax.set_xlabel('Diffusion year',fontsize=font)
            ax.set_title(anime_type,fontsize=font)
        
    else:
        fig, ax = plt.subplots(1,1,figsize=enlarge_fig) #building a subplot for the one choosen
       
        anime_type=anitypes[0]
        df_type=select_years[select_years['type']==anime_type]
        print('--------------'+anime_type)

        sb.lineplot(ax=ax,x='release-year',y='count',hue='genres',data=df_type,linewidth = 2, legend=False, palette=custom_patches,ci=None)
        
        ax.set(ylim=0)
        ax.xaxis.set_major_locator(MaxNLocator(integer=True))
        ax.set(xlim=(min_year,max_year))
        ax.set_ylabel('Number of anime with the genre',fontsize=font)
        ax.set_xlabel('Diffusion year',fontsize=font)
        ax.set_title(anime_type,fontsize=font)
    
    genre_list.sort()
    fig.legend(genre_list, loc=lgd_position,fontsize=font)

    signature(fig) 
    fig.suptitle('Evolution of a genre watched by '+username+' (0 if they are less than top '+str(thresold)+' of the year)' ,fontsize=font)

    fig.tight_layout()    
    fig.subplots_adjust(right=adjust['right'],bottom=adjust['bottom'])
       
    fig.savefig(savepath+'/'+username+'_genres_evolution'+str(start_year)+'-'+str(end_year))
    fig.show()

    return fig

def themes_evolution(df,min_year,max_year,anitypes,color_list,thresold=10):
    df=df.drop_duplicates(subset=['title','release-year','type'])
    df=df[['release-year','type','themes']]
    select_years=df[(df['release-year']<=max_year) & (df['release-year']>=min_year)] #remove years out of study scope
    select_years=select_years[select_years['type'].isin(anitypes)]
    
    select_years=select_years.dropna(subset=['themes'])
    select_years=select_years[select_years['themes']!="[]"]
    
    select_years['themes']=select_years['themes'].apply(literal_eval) #transform a string to a list
    
    select_years=select_years.explode('themes') #seperate list value to their own row
    select_years=select_years.value_counts(['release-year','type','themes']).reset_index(name='count')
    
    #Build the top genres list of each year and put them in on unique list
    theme_list=[]
    for year in range(min_year,max_year+1):
        for anitype in anitypes:
            top_themes=select_years[(select_years['release-year']==year) & (select_years['type']==anitype)].sort_values('count',ascending=False)['themes'].head(thresold).values.tolist() #building the top 3 lists for each year and anime type
            for theme in top_themes:
                theme_list.append(theme)  
                
    theme_list = list(dict.fromkeys(theme_list))
    
    select_years=select_years[select_years['themes'].isin(theme_list)]
    
    data_add=[]
      
    for year in range(min_year,max_year+1):
        for anitype in anitypes:
            for theme in theme_list:
            
                if select_years[(select_years['type']==anitype) & (select_years['release-year']==year) & (select_years['themes']==theme)].empty:
                    data_add.append([year,anitype,theme,0])
                
    df_add=pd.DataFrame(data_add,columns=['release-year','type','themes','count'])
    select_years=pd.concat([select_years,df_add], ignore_index=True)
    select_years=select_years.sort_values('themes')

    
    print('------------ plotting evolution of genre by year ------------')    
    
    custom_patches=contrast_colors[0:select_years['themes'].nunique()]
    
    if len(anitypes)>1:
        
        if len(anitypes)>4:
            fig, axes = plt.subplots(2,3,figsize=enlarge_fig) #building a subplot for the 6 anime types
            axes = axes.flatten()
        elif len(anitypes)==2:
            fig, axes = plt.subplots(1,2,figsize=enlarge_fig) #building a subplot for the 2 anime types
            axes = axes.flatten()
        else:
            fig, axes = plt.subplots(2,2,figsize=enlarge_fig) #building a subplot for the 4 anime types
            axes = axes.flatten()
            
        for anime_type,ax in zip(anitypes,axes): #anime types and plots go together so I zip them
            df_type=select_years[select_years['type']==anime_type] #reducing the DataFrame to the season studied I need the year to be at the right order for the stacking
            print('--------------'+anime_type)
            
            
            sb.lineplot(ax=ax,x='release-year',y='count',hue='themes',data=df_type,linewidth = 2, legend=False, palette=custom_patches,ci=None)
            
            ax.set(ylim=0)
            ax.xaxis.set_major_locator(MaxNLocator(integer=True))
            ax.set(xlim=(min_year,max_year))
            ax.set_ylabel('Number of anime with the theme',fontsize=font)
            ax.set_xlabel('Diffusion year',fontsize=font)
            ax.set_title(anime_type,fontsize=font)
        
    else:
        fig, ax = plt.subplots(1,1,figsize=enlarge_fig) #building a subplot for the one choosen
       
        anime_type=anitypes[0]
        df_type=select_years[select_years['type']==anime_type]
        print('--------------'+anime_type)

        sb.lineplot(ax=ax,x='release-year',y='count',hue='themes',data=df_type,linewidth = 2, legend=False, palette=custom_patches,ci=None)
        
        ax.set(ylim=0)
        ax.set(xlim=(min_year,max_year))
        ax.xaxis.set_major_locator(MaxNLocator(integer=True))
        ax.set_ylabel('Number of anime with the theme',fontsize=font)
        ax.set_xlabel('Diffusion year',fontsize=font)
        ax.set_title(anime_type,fontsize=font)
    
    theme_list.sort()
    fig.legend(theme_list, loc=lgd_position,fontsize=font)

    signature(fig) 
    fig.suptitle('Evolution of a theme watched by '+username+' (0 if they are less than top '+str(thresold)+' of the year)' ,fontsize=font)

    fig.tight_layout()    
    fig.subplots_adjust(right=adjust['right'],bottom=adjust['bottom'])
       
    fig.savefig(savepath+'/'+username+'_themes_evolution'+str(start_year)+'-'+str(end_year))
    fig.show()

    return fig

                #SECTION 3 CHOICE
#Choosing the file
datavalid=False
while datavalid==False:
    layout = [[sg.Text('Path of the MAL scrap data file')],
            [sg.Input(), sg.FileBrowse()],
            [sg.Text('Path of your MAL xml file (generate in https://myanimelist.net/panel.php?go=export)')],
            [sg.Input(), sg.FileBrowse()], 
            [sg.Text('OR MyAnimeList username (takes longer)')],
            [sg.Input()],
            [sg.Text('Removing dropped anime ?')],
            [sg.Radio('Yes','group1',default=True),sg.Radio('No','group1',default=False)],                   
            [sg.OK(), sg.Cancel()]] 
    window = sg.Window('Get path', layout)
    event, values = window.read()
    window.close()
    if event==sg.WIN_CLOSED or event=='Cancel':
        exit()  

    scrapath=values[0]
    malpath=values[1]
    username=values[2]
    drop_drop=values[3]
    
    window.close()
    try:
        datavalid=(len(username)*len(malpath)==0)and(len(username)!=len(malpath))
    except:
        sg.popup('You need to fill the xml adress or the username, not both')
        
    if username!='':
        try:
            raw=opener(scrapath,scrapath[scrapath.find('.')+1:])
            datavalid=True
        except:
            sg.popup('Could not read file.')        
    else:    
        try:
            raw=opener(scrapath,scrapath[scrapath.find('.')+1:])
            malraw=opener(malpath,malpath[malpath.find('.')+1:])
            datavalid=True
        except:
            sg.popup('Could not read file.')

#I make sure they are integer as sometime it's interpreted as float
raw['release-year']=raw['release-year'].astype(int) 
raw['episodes']=raw['episodes'].astype(int)

first_year=raw['release-year'].min()
last_year=raw['release-year'].max()

#If I want to draw multiple plots with different temporal range or category, I have a loop avoiding chosing my file everytime
again=['Yes']
while again[0]=='Yes':
                        
    #Choosing the years to view in plot
    datavalid=False
    while datavalid==False:
        layout = [[sg.Text('Which years do you want to view ? ')],
                [sg.Text('Must be YYYY in range ['+str(first_year)+';'+str(time.localtime().tm_year+1)+']')],
                [sg.Text('From'),sg.Spin([i for i in range(first_year,time.localtime().tm_year+2)], initial_value=first_year),sg.Text('until'),sg.Spin([i for i in range(first_year,time.localtime().tm_year+2)], initial_value=last_year)], 
                [sg.OK(), sg.Cancel()]] 
        window = sg.Window('Interval selection', layout)
        event, values = window.read()
        window.close()
        
        if event==sg.WIN_CLOSED or event=='Cancel':
             exit()    
    
        start_year=values[0]
        end_year=values[1]
        try:
            #check if input is integer without breaking
            start_year=int(start_year)
            end_year=int(end_year)
            if start_year<1917 or start_year>time.localtime().tm_year or end_year<1917 or end_year>time.localtime().tm_year:
                sg.popup('Invalid input. Must be YYYY in range ['+str(first_year)+';'+str(last_year)+']')
            elif start_year>end_year:
                sg.popup('Start year is after end year')
            else:
                datavalid=True
        except:
            sg.popup('Invalid input. Must be YYYY in range ['+str(start_year)+';'+str(end_year)+']')
    
    years=np.arange(start_year,end_year+1,1)

    season_scraped=0

    if username=='':
            
        #Merge the two lists while keeping only the completed show
        username=malraw['user_name'][0]
        
        if drop_drop==True:
            malraw=malraw[malraw['my_status'].isin(['Completed','Watching'])]
        else:
            malraw=malraw[malraw['my_status'].isin(['Completed','Watching','Dropped'])]
    else:
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
        malraw=pd.DataFrame(dict.fromkeys(formatting,[]))
        
        layout = [[sg.Text('Current progress')],
                  [sg.Output(size=(80,12))],
                  [sg.ProgressBar(4*(1+end_year-start_year), orientation='h', size=(40, 12), key='progressbar')], #build a progress bar /!\ not accurate as it will just do number of year * 4 (seasons)
                  [sg.Cancel()]]

        window = sg.Window('Progress', layout)
        progress_bar = window['progressbar']
        season_scraped=0
        
        for year in years:              
            for season_to_scrap in seasons:
                #show progress of scraping
                event,values=window.read(timeout=5+sleep_time)
                if event==sg.WIN_CLOSED or event=='Cancel':
                    window.close()
                    exit()
                
                test=userseasonscrap(season_to_scrap,year,username)
                df_n=pd.DataFrame(test) #I bluid a DataFrame around my data freshly scraped
        
                print(username +' anime list for '+ str(season_to_scrap)+' '+str(year))
        
                season_scraped+=1
                progress_bar.UpdateBar(season_scraped)
                window.refresh()
                
                malraw=pd.concat([malraw,df_n],ignore_index=True)
                   
                time.sleep(sleep_time)
                
        window.close()    
    raw=pd.merge(raw,malraw,left_on='MAL_id',right_on='series_animedb_id')

    raw['my_score']=raw["my_score"].astype(int)         
    raw=raw.drop_duplicates(subset=['title','release-year','type','release-season'])
    
    #Choosing the type to view in plot
    type_to_viz=[]
    datavalid=False
    while datavalid==False:
        layout = [[sg.Text('Which type of content do you want to visualize ? ')],
                [[sg.CBox(anitype, default=True) for anitype in anime_types]], 
                [sg.OK(), sg.Cancel()]]
        window = sg.Window('Choosing anime type', layout)
        event, values = window.read()
        window.close()
        
        if event==sg.WIN_CLOSED or event=='Cancel':
             exit()
        
        for i in range(len(values)):
            if values[i]==True:
                type_to_viz.append(anime_types[i])
        
        if len(type_to_viz)!=0:
            datavalid=True
        else:
            sg.popup('At least one box must be checked')
    
    #Choosing the plot to draw        
    plot_to_viz=[]
    datavalid=False
    while datavalid==False:
        layout=[]
        layout += [sg.Text('Which plots do you want to draw ? ')],
               
        for i in range(int(np.ceil(len(plot_list)/2))): #Choice on 2 colums to reduce the window's width
            try:
                layout+=[sg.CBox(plot_list[2*i],size=(20,1), default=True,key=plot_list[2*i]),sg.CBox(plot_list[2*i+1],size=(20,1), default=True,key=plot_list[2*i+1])], #put to check box on the same row
            except:
                layout+=[sg.CBox(plot_list[2*i],size=(20,1), default=True,key=plot_list[2*i])], #If odd number of plots, then the last will be only one column in the row    
            
        layout+=[[sg.OK(), sg.Cancel()]]
        
        window = sg.Window('Choosing plot to view', layout)
        event, values = window.read()
        window.close()
        
        if event==sg.WIN_CLOSED or event=='Cancel':
             exit()
        
        plot_to_viz=values
        
        plots=0
        for value in plot_to_viz.values():
            if value==True: 
                datavalid=True #at least one box must be check to trigger this event
                plots+=1 #count the number of plots to draw for the progression bar

        if datavalid==False:
            sg.popup('At least one box must be checked')
           

                    #SECTION 4 PRODUCING PLOTS
    #Choosing the saving path
    layout = [[sg.Text('Path to save plots')],
              [sg.Input(), sg.FolderBrowse()],
              [sg.Ok(),sg.Cancel()]]
    
    window = sg.Window('Saving plot', layout)
    
    event,values=window.read()
    window.close()
  
    if event==sg.WIN_CLOSED or event=='Cancel':
        window.close()
        exit()  
    
    savepath=values[0]    
    
    #Building a progress bar with ouptut print in the box
    layout = [[sg.Text('Current progress')],
              [sg.Output(size=(80,12))],
              [sg.ProgressBar(plots, orientation='h', size=(40, 12), key='progressbar')],
              [sg.Cancel()]]
    
    window = sg.Window('Progress', layout)
    progress_bar = window['progressbar']
    plot_done=0
    
    
    event,values=window.read(timeout=5)
    if event==sg.WIN_CLOSED or event=='Cancel':
        window.close()
        exit()
 
    #plots drawing
    if plot_to_viz['Watching seasons']==True: #draw the plots if it's true
        fig_prod_m=production_season(raw,start_year,end_year,type_to_viz,contrast_colors)
        plot_done+=1 #increment the progress bar
        progress_bar.UpdateBar(plot_done)
    
    event,values=window.read(timeout=5)
    if event==sg.WIN_CLOSED or event=='Cancel':
        window.close()
        exit()

    
    if plot_to_viz['Watching years']==True:
        fig_prod_y=production_year(raw,start_year,end_year,type_to_viz,contrast_colors)
        plot_done+=1
        progress_bar.UpdateBar(plot_done)
    
    event,values=window.read(timeout=5)
    if event==sg.WIN_CLOSED or event=='Cancel':
        window.close()
        exit()
        

    if plot_to_viz['Studio watching']==True:
        fig_studprod=production_studio(raw,start_year,end_year,type_to_viz,contrast_colors)
        plot_done+=1
        progress_bar.UpdateBar(plot_done)   
        
    event,values=window.read(timeout=5)
    if event==sg.WIN_CLOSED or event=='Cancel':
        window.close()
        exit()  
       

    if plot_to_viz['Source repartition']==True:    
        fig_source=source(raw,start_year,end_year,type_to_viz,contrast_colors,2.5)
        plot_done+=1
        progress_bar.UpdateBar(plot_done)
    
    event,values=window.read(timeout=5)
    if event==sg.WIN_CLOSED or event=='Cancel':
        window.close()
        exit()
        
        
    if plot_to_viz['Score distribution']==True:    
        fig_score=score_distribution(raw,start_year,end_year,type_to_viz)
        plot_done+=1
        progress_bar.UpdateBar(plot_done)
    
    event,values=window.read(timeout=5)
    if event==sg.WIN_CLOSED or event=='Cancel':
        window.close()
        exit()
   
    
    event,values=window.read(timeout=5)
    if event==sg.WIN_CLOSED or event=='Cancel':
        window.close()
        exit()        
        
        
    if plot_to_viz['Score vs viewers']==True:    
        fig_popularity=score_viewers(raw,start_year,end_year,type_to_viz)
        plot_done+=1
        progress_bar.UpdateBar(plot_done)
    
    event,values=window.read(timeout=5)
    if event==sg.WIN_CLOSED or event=='Cancel':
        window.close()
        exit() 
        
    if plot_to_viz['Score vs MAL means']==True:    
        fig_taste=score_vs_world(raw,start_year,end_year,type_to_viz)
        plot_done+=1
        progress_bar.UpdateBar(plot_done)
    
    event,values=window.read(timeout=5)
    if event==sg.WIN_CLOSED or event=='Cancel':
        window.close()
        exit()        
        

    if plot_to_viz['TV (New) length']==True:    
        fig_ep=episode(raw,start_year,end_year,'TV (New)',60)
        plot_done+=1
        progress_bar.UpdateBar(plot_done)
    
    event,values=window.read(timeout=5)
    if event==sg.WIN_CLOSED or event=='Cancel':
        window.close()
        exit()
        
    if plot_to_viz['Genre evolution']==True:    
        genres_evolution(raw,start_year,end_year,type_to_viz,contrast_colors,5)
        plot_done+=1
        progress_bar.UpdateBar(plot_done)
    
    event,values=window.read(timeout=5)
    if event==sg.WIN_CLOSED or event=='Cancel':
        window.close()
        exit()
        
    if plot_to_viz['Theme evolution']==True:    
        themes_evolution(raw,start_year,end_year,type_to_viz,contrast_colors,3)
        plot_done+=1
        progress_bar.UpdateBar(plot_done)

    event,values=window.read(timeout=5)
    if event==sg.WIN_CLOSED or event=='Cancel':
        window.close()
        exit()        

    #this is the end...
    window.close()    
    sg.popup('Finished ! \nPlots saved at '+savepath)
    
    #or not ?
    layout=[[sg.Text('Do you want to draw other plots ?')],
            [sg.Yes(),sg.No()]]
    
    window=sg.Window('Again ?',layout)
    again=window.read()
    window.close()