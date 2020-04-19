#file_loc = '../.' # production
file_loc = ''  # deploy
import pandas as pd

statewise_data = pd.read_csv( file_loc + './data/statewise_data.csv' )
statewise_data['Confirmed'] = statewise_data['Confirmed'].astype( float )
state_grouped = statewise_data.groupby( ['State'] )['Confirmed'].sum().reset_index()
statewise_confirmed_grouped = state_grouped[state_grouped['State'] != 'Total'].sort_values( 'Confirmed',ascending=False )[:40][::-1]
statewise_confirmed_grouped = statewise_confirmed_grouped.sort_values('Confirmed', ascending=False)

statewise_confirmed = pd.Series( statewise_confirmed_grouped['Confirmed'] ).tolist()
statewise_confirmed_statename = pd.Series( statewise_confirmed_grouped['State'] ).tolist()
state_codes = {
    'West Bengal': 'WB',
    'Odisha': 'OD',
    'Andhra Pradesh': 'AP',
    'Jammu and Kashmir':'JK',
    'Ladakh':'LD',
    'Uttarakhand':'UK',
    'Uttar Pradesh':'UP',
    'Tripura':'TR',
    'Telangana':'TG',
    'Tamil Nadu':'TN',
    'Sikkim':'SK',
    'Rajasthan':'RJ',
    'Punjab':'PB',
    'Puducherry':'PD',
    'Delhi':'DL',
    'Nagaland':'NL',
    'Mizoram':'MZ',
    'Meghalaya':'MG',
    'Manipur':'MN',
    'Maharashtra':'MH',
    'Madhya Pradesh':'MP',
    'Lakshadweep':'LD',
    'Kerala':'KL',
    'Karnataka':'KR',
    'Jharkhand':'JK',
    'Himachal Pradesh':'HP',
    'Haryana':'HR',
    'Gujarat':'GJ',
    'Goa':'GA',
    'Daman and Diu':'DD',
    'Dadra and Nagar Haveli':'DN',
    'Chhattisgarh':'CT',
    'Chandigarh':'CH',
    'Bihar':'BR',
    'Assam':'AS',
    'Arunachal Pradesh':'AR',
    'Andaman and Nicobar Islands':'AN'
}
state_code_list = []
for state in statewise_confirmed_statename:
    state_code_list.append(state_codes[state])
