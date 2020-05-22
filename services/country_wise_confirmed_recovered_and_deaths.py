from datetime import datetime

import pandas as pd
pd.options.mode.chained_assignment = None

#file_loc = '.' # production
file_loc = ''  # deploy

gov_data = pd.read_csv(file_loc + './data/complete.csv')
'''
c = 0
for row in gov_data.index:
  if gov_data['Date'][row] == '2020-04-13':
    c += 1
    if c == 2:
      gov_data['Date'][row] = "2020-04-14"
      c=0
'''

# for govt data
gov_data['Date'] = pd.to_datetime(gov_data['Date'],dayfirst=True)
confirmed_death_recovered = gov_data.groupby('Date')['Date', 'Total Confirmed cases','Cured/Discharged/Migrated', 'Death'].sum().reset_index()

c = 0
r = 0
d = 0
confirmed_death_recovered['day_conf'] = confirmed_death_recovered['Total Confirmed cases']
confirmed_death_recovered['day_rec'] = confirmed_death_recovered['Cured/Discharged/Migrated']
confirmed_death_recovered['day_death'] = confirmed_death_recovered['Death']
for row in confirmed_death_recovered.index:
  confirmed_death_recovered['day_conf'][row] -= c
  confirmed_death_recovered['day_rec'][row] -= r
  confirmed_death_recovered['day_death'][row] -= d
  c = confirmed_death_recovered['Total Confirmed cases'][row]
  r = confirmed_death_recovered['Cured/Discharged/Migrated'][row]
  d = confirmed_death_recovered['Death'][row]


# diagnosed = pd.Series(confirmed_death_recovered['Date']).tolist()
# diagnosed_date = [datetime.strptime(x, "%Y-%m-%d %H:%M:%S") for x in diagnosed]
dates = pd.Series(confirmed_death_recovered['Date']).tolist()
day_wise_encountered = pd.Series(confirmed_death_recovered['day_conf']).tolist()
day_wise_confirmed_overall = pd.Series( confirmed_death_recovered['Total Confirmed cases']).tolist()


confirmed_death_recovered['tot_active'] = confirmed_death_recovered['Total Confirmed cases'] - confirmed_death_recovered['Death'] - confirmed_death_recovered['Cured/Discharged/Migrated']
confirmed_death_recovered[['tot_active']]
#print(confirmed_death_recovered["Cured/Discharged/Migrated"])
recovery_daywise = pd.Series(confirmed_death_recovered['day_rec']).tolist()
recovery_cumulative = pd.Series(confirmed_death_recovered['Cured/Discharged/Migrated']).tolist()
dates = pd.Series(confirmed_death_recovered['Date']).tolist()
#recovery_dates = [datetime.strptime(x, "%Y-%m-%d") for x in dates]

death_cumulative = pd.Series(confirmed_death_recovered['Death']).tolist()
death_day_wise = pd.Series(confirmed_death_recovered['day_death']).tolist()
