import pandas as pd
from datetime import datetime
pd.options.mode.chained_assignment = None

#file_loc = '.' # production
file_loc = ''  # deploy

death_and_recovered = pd.read_csv(file_loc + './data/death_and_recovered.csv' )
grouped = death_and_recovered.groupby('Date')[['Date', 'recovered']].sum().reset_index()
s = 0
grouped['tot_recovered'] = grouped['recovered']
for row in grouped.index:
    grouped['tot_recovered'][row] += s
    s = grouped['tot_recovered'][row]

#print(grouped)
# recovery_daywise = death_and_recovered.groupby('Date')['recovered'].sum().reset_index() # actual in notebook
recovery_daywise = pd.Series(grouped['recovered']).tolist()  # found similar
recovery_cumulative = pd.Series(grouped['tot_recovered']).tolist()
dates = pd.Series(grouped['Date']).tolist()
recovery_dates = [datetime.strptime(x, "%Y-%m-%d %H:%M:%S") for x in dates]
# print(recovery_cumulative)
# print(recovery_daywise)
# print(recovery_dates)
