
#from services.processes import data # deploy
from services.fetch import get  # deploy
file_loc = ''  # deploy
'''
# production
file_loc = '.' # production
from fetch import get  # production
'''
from datetime import datetime
import json
from pandas.io.json import json_normalize
import pandas as pd
data = pd.read_csv( file_loc + './data/data.csv' )
grouped = data.groupby( 'Diagnosed date' )['Diagnosed date', 'confirmed'].sum().reset_index()
s = 0
grouped['tot_confirmed'] = grouped['confirmed']
for row in grouped.index:
    grouped['tot_confirmed'][row] += s
    s = grouped['tot_confirmed'][row]

diagnosed = pd.Series(grouped['Diagnosed date']).tolist()
diagnosed_date = [datetime.strptime( x, "%Y-%m-%d %H:%M:%S" ) for x in diagnosed]
day_wise_encountered = pd.Series( grouped['confirmed'] ).tolist()
day_wise_confirmed = pd.Series( grouped['tot_confirmed'] ).tolist()
