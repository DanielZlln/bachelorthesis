from dateutil.relativedelta import relativedelta
from dateutil.parser import parse
from datetime import datetime, timedelta, date
import pandas as pd
from pathlib import Path
import os
from os import walk
import locale

def get_src_directory(script_directory):
    src_directory = script_directory.parent / 'src'
    return src_directory


for root, dirs, files in os.walk('/Users/danielzellner/Documents/Studium/Bachelorthesis/src'):
    files = [f for f in files if not f[0] == '.']



def clean_neutor_excel(file_name):
    notebook_directory = os.getcwd()
    script_directory = Path(notebook_directory)
    src_directory = get_src_directory(script_directory)
    file_path = src_directory / file_name
    neutor_xlsx = pd.read_excel(file_path, 
                                    sheet_name=None, 
                                    skiprows=2,
                                    skipfooter=1,
                                    engine='openpyxl')
    
    df_neutor = pd.concat(neutor_xlsx.values(), ignore_index=True)
    
    new_column_names = {
                        'Neutor': 'Neutor (gesamt)',
                        'FR stadteinwärts': 'Neutor FR stadteinwärts',
                        'FR stadtauswärts': 'Neutor FR stadtauswärts',
                        'Time' : 'Zeit'
                    }
    df_neutor = df_neutor.rename(columns=new_column_names)
    
    if 'Gefühlte Temperatur (°C)' in df_neutor.columns:
        df_neutor = df_neutor.drop('Gefühlte Temperatur (°C)', axis=1)
        
    if 'Unnamed: 0' in df_neutor.columns:
        df_neutor = df_neutor.drop(columns='Unnamed: 0', axis=1)

    if 'Zeit' in df_neutor.columns:
        success_date = False

        try:
            df_neutor['Datum'] = pd.to_datetime(df_neutor['Zeit'], format='%Y-%m-%d').dt.date.astype(str)
            df_neutor['Zeit'] = pd.to_datetime(df_neutor['Zeit']).dt.time
            
            success_date = True
        except ValueError:
            print('Konnte nicht in das Foramt bereinigt werden')
        
        if not success_date:
            try:
                df_neutor['Zeit'] = df_neutor['Zeit'].astype(str)
                df_neutor[['day', 'month', 'year', 'Uhrzeit']] = df_neutor['Zeit'].str.split(' ', expand=True)

                month_to_num = {'Jan.': 1, 'Febr.': 2, 'Mrz.': 3, 'Apr.': 4, 'Mai': 5, 'Jun.': 6, 'Jul.': 7, 'Aug.': 8, 'Sept.': 9, 'Okt.': 10, 'Nov.': 11, 'Dez.': 12}
                df_neutor.month = df_neutor.month.map(month_to_num)
                df_neutor.day = df_neutor.day.astype(str)
                df_neutor.day = df_neutor.day.str.replace('.','')

                df_neutor.drop(['Zeit'], axis=True, inplace=True)
                df_neutor['Zeit'] = pd.to_datetime(df_neutor['Uhrzeit'], format='%H:%M', errors='coerce').dt.time
                df_neutor['Datum'] = pd.to_datetime(df_neutor[['year', 'month', 'day']])

                df_neutor.drop(['day','month','year', 'Uhrzeit'], axis=True, inplace=True)
                
                success_date = True
            except ValueError:
                print('Konnte nicht in das Foramt bereinigt werden')

        if success_date:          
            try:
                df_neutor = df_neutor[['Datum', 'Zeit', 'Neutor (gesamt)', 'Neutor FR stadteinwärts', 'Neutor FR stadtauswärts', 'Wetter', 'Temperatur (°C)', 
                            'Luftfeuchtigkeit (%)', 'Regen (mm)', 'Wind (km/h)']]
            except (ValueError, KeyError):
                print('Falsche Spaltenbezeichnung')
            
        return df_neutor