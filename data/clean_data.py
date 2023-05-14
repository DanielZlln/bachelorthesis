import pandas as pd
from dateutil.relativedelta import relativedelta
from datetime import datetime, timedelta, date

def load_data():
    neutor_xlsx = pd.read_excel('/Users/danielzellner/Documents/Studium/Bachelorthesis/src/Zaehlstelle_Neutor_2020_Stundenauswertung.xlsx', 
                                sheet_name=None, 
                                skiprows=2,
                                skipfooter=1,
                                engine='openpyxl')

    df_neutor = pd.concat(neutor_xlsx.values(), ignore_index=True)
        
    df_neutor['Datum'] = pd.to_datetime(df_neutor['Zeit']).dt.date
    df_neutor['Zeit'] = pd.to_datetime(df_neutor['Zeit']).dt.time
    
    df_neutor = df_neutor.drop(columns='Unnamed: 0')
    
    return df_neutor
    
def neutor_weekday():
    
    df_neutor = load_data()
    
    # Variable fuer Neutor und mean
    
    df_neutor_weekday = df_neutor.groupby('Datum', dropna=False).agg({'Neutor': 'sum', 
                                                                      'Neutor FR stadteinwärts': 'sum',
                                                                      'Neutor FR stadtauswärts': 'sum'})
    df_neutor_weekday.index = pd.to_datetime(df_neutor_weekday.index)
    df_neutor_weekday['Wochentag'] = df_neutor_weekday.index.day_name()
    
    df_neutor_weekday = df_neutor_weekday.reset_index()
    
    return df_neutor_weekday

def neutor_last_week():
    to_day = date.today()
    new_to_day = to_day + relativedelta(years=-3)
    last_week = date.today() - timedelta(days=7)
    new_date = last_week + relativedelta(years=-3)


    df_neutor_last_week = (df_neutor_weekday['Datum'] >= new_date) & (df_neutor_weekday['Datum'] < last_week) & (df_neutor_weekday['Datum'] < new_to_day)
    df_neutor_last_week = df_neutor_weekday.loc[df_neutor_last_week]
    
    return df_neutor_last_week


if __name__ == "__main__":
    df_neutor = load_data()
    df_neutor_weekday = neutor_weekday()
    df_neutor_last_week = neutor_last_week()