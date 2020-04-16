#file_loc = './.' # production
file_loc = ''  # deploy
import pandas as pd
statewise_data = pd.read_csv(file_loc + './data/statewise_data.csv')
statewise_data['Confirmed'] = statewise_data['Confirmed'].astype(float)
state_grouped = statewise_data.groupby(['State'])['Confirmed'].sum().reset_index()
statewise_confirmed_grouped = state_grouped[state_grouped['State']!='Total'].sort_values('Confirmed', ascending=True)[:40][::-1]
