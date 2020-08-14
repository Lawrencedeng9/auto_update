# -*- coding: utf-8 -*-
"""
Created on Thu Aug 13 00:21:42 2020

@author: ThinkPad
"""

import os
import pandas as pd
import numpy as np
from datetime import datetime
import shutil

def generate_file_info(fold):
    files_list=[]
    file_size=[]
    
    for root, dirs, files in os.walk(fold):
        for name in files:
            file_size.append(os.path.getsize(os.path.join(root, name)))
            files_list.append(os.path.join(root, name)[len(fold)+1:])
    
    file_df=pd.DataFrame(
            {
            'initial_files_name':files_list,
            'initial_file_size':file_size,
                    }
            )      
    
    return file_df

def align_folder(fold,map_fold):
    for root, dirs, files in os.walk(fold):
        for dir in dirs:
            try:
                os.mkdir(os.path.join(map_fold,dir))
            except FileExistsError:
                pass

def drop_timestamp(str_1):
    locate=int(str_1.find('_idx'))
    str_1=str_1.replace(str_1[locate-1:locate+18],'')
    return str_1
def get_timestamp(str_1):
    locate=int(str_1.find('_idx'))
    return int(str_1[locate+4:locate+18])
def add_timestamp(str_3):
    locate=str_3.find('.')
    timestamp=datetime.now().strftime('%Y%m%d%H%M%S')
    insert_str=' _idx'+timestamp
    tem_list=list(str_3)
    tem_list.insert(locate,insert_str)
    return ''.join(tem_list)   

fold=r'C:\Users\ThinkPad\Desktop\mapping_folder'
map_fold=r'F:\OneDrive - TSCN\mapping_folder'
align_folder(fold,map_fold)

df_1=generate_file_info(fold)
df_2=generate_file_info(map_fold)
df_2['adjusted_file_name']=df_2['initial_files_name'].apply(drop_timestamp)
df_2['modified_time']=df_2['initial_files_name'].apply(get_timestamp)

df_3=df_2.sort_values('modified_time',ascending=False).groupby('adjusted_file_name', as_index=False).first()[['adjusted_file_name','initial_file_size']]

df_4=pd.merge(df_1,df_3,how='left',left_on='initial_files_name',right_on='adjusted_file_name')
df_4['action']=np.nan

df_4.loc[df_4['adjusted_file_name'].isna(),'action']=1
df_4.loc[df_4['initial_file_size_y']!=df_4['initial_file_size_x'],'action']=1

df_5=df_4.loc[df_4['action']==1,:].copy()
df_5['suffix_file_path']=df_5['initial_files_name'].apply(add_timestamp)

def move_file(source,target):
    for i in range(len(source)):
        src=os.path.join(fold,source[i])
        dst=os.path.join(map_fold,target[i])
        shutil.copy(src, dst)

move_file(list(df_5['initial_files_name']),list(df_5['suffix_file_path']))