
# deploy
file_loc = ''  # deploy

'''
# production
file_loc = '.' # production
'''

from datetime import datetime
import json
from pandas.io.json import json_normalize
import pandas as pd
pd.options.mode.chained_assignment = None # Remove warnings
data = pd.read_csv( file_loc + './data/data-copy.csv' )
confirmed_grouped = data.groupby('Diagnosed date')['Diagnosed date', 'confirmed', 'recovered', 'death'].sum().reset_index()
c=0
r=0
d=0
confirmed_grouped['tot_confirmed'] = confirmed_grouped['confirmed']
confirmed_grouped['tot_r'] = confirmed_grouped['recovered']
confirmed_grouped['tot_d'] = confirmed_grouped['death']
for row in confirmed_grouped.index:
  confirmed_grouped['tot_confirmed'][row] += c
  c = confirmed_grouped['tot_confirmed'][row]
  confirmed_grouped['tot_r'][row] += r
  r = confirmed_grouped['tot_r'][row]
  confirmed_grouped['tot_d'][row] += d
  d = confirmed_grouped['tot_d'][row]

diagnosed = pd.Series(confirmed_grouped['Diagnosed date']).tolist()
diagnosed_date = [datetime.strptime(x, "%Y-%m-%d %H:%M:%S") for x in diagnosed]
day_wise_encountered = pd.Series(confirmed_grouped['confirmed']).tolist()
day_wise_confirmed_overall = pd.Series( confirmed_grouped['tot_confirmed']).tolist()


