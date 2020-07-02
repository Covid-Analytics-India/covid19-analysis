file_loc = ''  # deploy
# file_loc = '../.' # production

import pandas as pd
gov_data = pd.read_csv(file_loc + './data/covid_19_india.csv')
gov_data['Date'] = pd.to_datetime(gov_data['Date'],dayfirst=True)
gov_data = gov_data.rename(columns={"Confirmed": "Total Confirmed cases", 'Cured': "Cured/Discharged/Migrated", "State/UnionTerritory" : "Name of State / UT", "Deaths":"Death"})

gov_data['Active'] = 1
for i in gov_data.index:
    gov_data['Active'][i] = (gov_data['Total Confirmed cases'][i] - (gov_data['Cured/Discharged/Migrated'][i] + gov_data['Death'][i] ))

grouped = gov_data.groupby('Date')['Date', 'Total Confirmed cases'].sum().reset_index()

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

bef_lockdown = confirmed_death_recovered[confirmed_death_recovered['Date'] < '2020-03-25' ]
# print(bef_lockdown)
bef_lockdown_dates = pd.Series(bef_lockdown['Date']).to_list()
bef_lockdown_cases = pd.Series(bef_lockdown['tot_active']).to_list()

after_lockdown = confirmed_death_recovered[confirmed_death_recovered['Date'] >= '2020-03-25' ]
after_lockdown_dates = pd.Series(after_lockdown['Date']).to_list()
after_lockdown_cases = pd.Series(after_lockdown['tot_active']).to_list()
# print("TIme ", int(max(grouped["tot_confirmed"])))
maxCases = int(max(confirmed_death_recovered["tot_active"]))
shapes = [
    {
      "type": 'line',
      "x0": 1586822400,
      "y0": 0,
      "x1": 1586822400,
      "y1": maxCases,
      "line": {
        "color": 'rgb(55, 128, 191)',
        "width": 3,
        "dash": 'dashdot'
      }
    },
    {
      "type": 'line',
      "x0": 1588464000,
      "y0": 0,
      "x1": 1588464000,
      "y1": maxCases,
      "line": {
        "color": 'rgb(55, 128, 191)',
        "width": 3,
        "dash": 'dashdot'
      }
    },
    {
      "type": 'line',
      "x0": 1589673600,
      "y0": 0,
      "x1": 1589673600,
      "y1": maxCases,
      "line": {
        "color": 'rgb(55, 128, 191)',
        "width": 3,
        "dash": 'dashdot'
      }
    },
    {
      "type": 'line',
      "x0": 1590883200,
      "y0": 0,
      "x1": 1590883200,
      "y1": maxCases,
      "line": {
        "color": 'rgb(55, 128, 191)',
        "width": 3,
        "dash": 'dashdot'
      }
    }
]
# print(bef_lockdown_cases)
# print(after_lockdown_cases)

