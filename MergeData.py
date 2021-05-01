# -*- coding: utf-8 -*-
"""
Created on Thu Apr 29 23:07:08 2021

@author: qgump
"""

import pandas as pd
import PySimpleGUI as sg
from sys import exit

input_format=["html","json","csv","xlsx"]

datavalid=False
while datavalid==False:
    layout = [  [sg.Text('Original file:')],
            [sg.Input(), sg.FileBrowse()],
            [sg.Text('File with new data:')],
            [sg.Input(), sg.FileBrowse()],
            [sg.Text('Accepted format:'+str(input_format))],
            [sg.OK(), sg.Cancel()]] 
    
    window = sg.Window('Get path', layout)
    
    event, values = window.read()
    window.close()
    
    if event==sg.WIN_CLOSED or event=='Cancel':
        exit()  
    
        
    ext0=values[0][values[0].find(".")+1:]
    ext1=values[1][values[1].find(".")+1:]
    
    if (ext0 in input_format) or (ext1 in input_format):
        datavalid=True
    else:
        sg.popup('Invalid input. Must be in format: \n'+str(input_format))
        
def opener(path,ext):
    if ext=='csv':
        df=pd.read_csv(path)
    elif ext=="json":
        df=pd.read_json(path)
    elif ext=="html":
        df=pd.read_html(path)
    elif ext=="xlsx":
        df=pd.read_Excel(path)
        
    return df
    
df0=opener(values[0],ext0)
df1=opener(values[1],ext1)

df=pd.concat([df0,df1])
df.drop_duplicates(subset=["MAL_id","release-year","release-season"], keep='last', inplace=True, ignore_index=True)    

if len(df["type"].unique())==6:
    type_chosen="all"
else:
    type_chosen="custom"

start_year=int(df["release-year"].max())
end_year=int(df["release-year"].min())
start_season=df["release-season"].head(1).values[0]
end_season=df["release-season"].tail(1).values[0]

filename='/MAL-'+type_chosen+'-from-'+start_season+str(start_year)+'-to-'+end_season+str(end_year)

datavalid=False
while datavalid==False:    
    
    layout = [  [sg.Text('Path to save')],
            [sg.Input(default_text='Data'), sg.FolderBrowse()],
            [sg.Text('Output format:'),sg.Combo(input_format,default_value='csv')],
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
            df.to_html(path+filename+'.html',index=False)
        elif output_format=='json':
            df.to_json(path+filename+'.json')
        elif output_format=='csv':
            df.to_csv(path+filename+'.csv',index=False)
        elif output_format=='excel':
            df.to_excel(path+filename+'.xlsx',index=False)
        datavalid=True
    except:
        sg.popup('Unable to save at this path')
        

sg.popup('File saved as \n' + path+''+filename+'.'+output_format)           
