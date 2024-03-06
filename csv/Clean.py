import pandas as pd
df1 = pd.read_csv('csv/pm25.csv')
df1['PM25'] = df1['PM25'].fillna(df1['PM25'].mean())
df1['O3'] = df1['O3'].fillna(df1['O3'].mean())
df1['PM25'] = df1['PM25'].round(1)
df1['O3'] = df1['O3'].round(1)
data = df1.drop(columns=['PM10','CO', 'NO2', 'SO2'])
data.to_csv('csv/pm25_new.csv', index=False)