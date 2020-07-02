import pandas as pd
import warnings
file_loc = ''  # development
# file_loc = '../.' # build
warnings.simplefilter( 'ignore' )

gov_data = pd.read_csv(file_loc + './data/covid_19_india.csv', dtype=object)

gov_data['Date'] = pd.to_datetime(gov_data['Date'],dayfirst=True)
gov_data = gov_data.rename(columns={"Confirmed": "Total Confirmed cases", 'Cured': "Cured/Discharged/Migrated", "State/UnionTerritory" : "Name of State / UT", "Deaths":"Death"})

# --- --- --- MORTALITY RATE --- --- ---
statewise_data = gov_data[-gov_data[gov_data['Date'] == gov_data['Date'].max()].shape[0]:]
statewise_data['Death'] = pd.to_numeric(statewise_data['Death'])
statewise_data['Total Confirmed cases'] = pd.to_numeric(statewise_data['Total Confirmed cases'])

statewise_data['mortalityRate'] = round((statewise_data['Death'] / statewise_data['Total Confirmed cases'])*100, 2)
temp = statewise_data[statewise_data['Total Confirmed cases']>10]
temp = temp.sort_values('mortalityRate', ascending=False)
temp = temp.sort_values(by="mortalityRate", ascending=False)[:22][::-1]

mortality_rate = pd.Series(temp['mortalityRate']).to_list()
name_of_state_mr = pd.Series(temp['Name of State / UT']).to_list()

# print(mortality_rate)
# print(name_of_state_mr)

# --- --- --- RECOVERY RATE --- --- --- 
statewise_data['Cured/Discharged/Migrated'] = pd.to_numeric(statewise_data['Cured/Discharged/Migrated'])
statewise_data['recoveryRate'] = round((statewise_data['Cured/Discharged/Migrated']/statewise_data['Total Confirmed cases'])*100, 2)
temp = statewise_data[statewise_data['Total Confirmed cases']>10]
temp = temp.sort_values('recoveryRate', ascending=False)
temp = temp.sort_values(by="recoveryRate", ascending=False)[:25][::-1]

recovery_rate = pd.Series(temp['recoveryRate']).to_list()
name_of_state_rr = pd.Series(temp['Name of State / UT']).to_list()

# print(recovery_rate)
# print(name_of_state_rr)
