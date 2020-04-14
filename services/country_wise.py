
#from services.processes import data # deploy
from services.fetch import get  # deploy
file_loc = ''  # deploy
'''
# production
file_loc = '.' # production
from fetch import get  # production
'''
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

#print(grouped)