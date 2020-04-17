#file_loc = '../.' # production
file_loc = ''  # deploy
import pandas as pd

death_and_recovered = pd.read_csv( file_loc + './data/death_and_recovered.csv' )
statewise_data = pd.read_csv( file_loc + './data/statewise_data.csv' )

latest_grouped = death_and_recovered[death_and_recovered['District']!=''].groupby('District')['recovered'].sum().reset_index()
recovered_cases_district_wise = latest_grouped.sort_values('recovered', ascending=False)[:7][::-1]
recovered_cases_district_wise = recovered_cases_district_wise.sort_values('recovered', ascending=False)

recovered_cases_district_wise_district = pd.Series(recovered_cases_district_wise['District']).tolist()
recovered_cases_district_wise_recovered = pd.Series(recovered_cases_district_wise['recovered']).tolist()

# State Wise Recovery
statewise_data = statewise_data[statewise_data['State']!='Total'].sort_values('Recovered', ascending=False)[:7][::-1]
statewise_data = statewise_data.sort_values('Recovered', ascending=False)
statewise_recovered_cases = pd.Series(statewise_data['Recovered']).tolist()
statewise_recovered_states = pd.Series(statewise_data['State']).tolist()