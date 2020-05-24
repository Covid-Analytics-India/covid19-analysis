
file_loc = ''  # deploy
#file_loc = '../.' # production
import pandas as pd

gov_data = pd.read_csv(file_loc + './data/complete.csv')

c = 0
for row in gov_data.index:
  if gov_data['Date'][row] == '2020-04-13':
    c += 1
    if c == 2:
      gov_data['Date'][row] = "2020-04-14"
      c=0
gov_data['Date'] = pd.to_datetime(gov_data['Date'],dayfirst=True)
#print(gov_data)
#print(gov_data)
gov_data = gov_data.replace(['Telengana', 'Dadar Nagar Haveli'] ,['Telangana', 'Dadra and Nagar Haveli'])
#gov_data = gov_data.replace('Dadar Nagar Haveli','Dadra and Nagar Haveli')
#print(gov_data['Name of State / UT'])
confirmed = gov_data[-gov_data[gov_data['Date'] == gov_data['Date'].max()].shape[0]:].sort_values('Total Confirmed cases', ascending=False)[:33][::-1]
statewise_confirmed = pd.Series( confirmed['Total Confirmed cases']).tolist()
statewise_confirmed_names = pd.Series( confirmed['Name of State / UT'] ).tolist()

recovered = gov_data[-gov_data[gov_data['Date'] == gov_data['Date'].max()].shape[0]:].sort_values('Cured/Discharged/Migrated', ascending=False)[:33][::-1]
statewise_recovered_cases = pd.Series(recovered['Cured/Discharged/Migrated']).tolist()
statewise_recovered_names = pd.Series( recovered['Name of State / UT'] ).tolist()

deaths = gov_data[-gov_data[gov_data['Date'] == gov_data['Date'].max()].shape[0]:].sort_values('Death', ascending=False)[:33][::-1]
statewise_deaths = pd.Series(deaths['Death']).tolist()
statewise_deaths_names = pd.Series( deaths['Name of State / UT'] ).tolist()

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
    'Andaman and Nicobar Islands':'AN',
}
state_code_list = []
for state in statewise_confirmed_names:
    state_code_list.append(state_codes[state])

