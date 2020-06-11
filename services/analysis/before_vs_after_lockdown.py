file_loc = ''  # deploy
# file_loc = '../.' # production

import pandas as pd
gov_data = pd.read_csv(file_loc + './data/covid_19_india.csv')
gov_data['Date'] = pd.to_datetime(gov_data['Date'],dayfirst=True)
gov_data = gov_data.rename(columns={"Confirmed": "Total Confirmed cases", 'Cured': "Cured/Discharged/Migrated", "State/UnionTerritory" : "Name of State / UT", "Deaths":"Death"})

grouped = gov_data.groupby('Date')['Date', 'Total Confirmed cases'].sum().reset_index()
s = 0
grouped['tot_confirmed'] = grouped['Total Confirmed cases']
for row in grouped.index:
  grouped['tot_confirmed'][row] += s
  s = grouped['tot_confirmed'][row]


bef_lockdown = grouped[grouped['Date'] < '2020-03-25' ]
bef_lockdown_dates = pd.Series(bef_lockdown['Date']).to_list()
bef_lockdown_cases = pd.Series(bef_lockdown['tot_confirmed']).to_list()

after_lockdown = grouped[grouped['Date'] >= '2020-03-25' ]
after_lockdown_dates = pd.Series(after_lockdown['Date']).to_list()
after_lockdown_cases = pd.Series(after_lockdown['tot_confirmed']).to_list()
# print("TIme ", int(max(grouped["tot_confirmed"])))
shapes = [
    {
      "type": 'line',
      "x0": 1586822400,
      "y0": 0,
      "x1": 1586822400,
      "y1": int(max(grouped["tot_confirmed"])),
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
      "x1": 1591528967,
      "y1": int(max(grouped["tot_confirmed"])),
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
      "y1": int(max(grouped["tot_confirmed"])),
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
      "y1": int(max(grouped["tot_confirmed"])),
      "line": {
        "color": 'rgb(55, 128, 191)',
        "width": 3,
        "dash": 'dashdot'
      }
    }
]
# print(shapes)

