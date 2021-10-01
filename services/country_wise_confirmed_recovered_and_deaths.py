from datetime import datetime

import pandas as pd
pd.options.mode.chained_assignment = None

#file_loc = '.' # production
file_loc = ''  # deploy

gov_data = pd.read_csv(file_loc + './data/covid_19_india.csv')

# for govt data
gov_data['Date'] = pd.to_datetime(gov_data['Date'],dayfirst=True)
gov_data = gov_data.rename(columns={"Confirmed": "Total Confirmed cases", 'Cured': "Cured/Discharged/Migrated", "State/UnionTerritory" : "Name of State / UT", "Deaths":"Death"})
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

confirmed_death_recovered['tot_active'] = confirmed_death_recovered['Total Confirmed cases'] - confirmed_death_recovered['Death'] - confirmed_death_recovered['Cured/Discharged/Migrated']



dates = pd.Series(confirmed_death_recovered['Date']).tolist()
day_wise_encountered = pd.Series(confirmed_death_recovered['day_conf']).tolist()
day_wise_confirmed_overall = pd.Series( confirmed_death_recovered['Total Confirmed cases']).tolist()


confirmed_death_recovered['tot_active'] = confirmed_death_recovered['Total Confirmed cases'] - confirmed_death_recovered['Death'] - confirmed_death_recovered['Cured/Discharged/Migrated']
recovery_daywise = pd.Series(confirmed_death_recovered['day_rec']).tolist()
recovery_cumulative = pd.Series(confirmed_death_recovered['Cured/Discharged/Migrated']).tolist()
dates = pd.Series(confirmed_death_recovered['Date']).tolist()

death_cumulative = pd.Series(confirmed_death_recovered['Death']).tolist()
death_day_wise = pd.Series(confirmed_death_recovered['day_death']).tolist()
