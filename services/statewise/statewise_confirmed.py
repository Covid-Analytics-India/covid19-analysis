#file_loc = '../.' # production
from builtins import float

file_loc = ''  # deploy
import pandas as pd

statewise_data = pd.read_csv( file_loc + './data/statewise_data.csv' )
statewise_data['Confirmed'] = statewise_data['Confirmed'].astype( float )
state_grouped = statewise_data.groupby( ['State'] )['Confirmed'].sum().reset_index()
statewise_confirmed_grouped = state_grouped[state_grouped['State'] != 'Total'].sort_values( 'Confirmed',ascending=False )[:40][::-1]
statewise_confirmed_grouped = statewise_confirmed_grouped.sort_values('Confirmed', ascending=False)

statewise_confirmed = pd.Series( statewise_confirmed_grouped['Confirmed'] ).tolist()
statewise_confirmed_statename = pd.Series( statewise_confirmed_grouped['State'] ).tolist()


