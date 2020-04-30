import pandas as pd

file_loc = ''  # deploy
#file_loc = '../.'  # production

df = pd.read_csv( file_loc + './data/district_wise.csv' )
# all graphs with 'h' orientation

# Most affected district confirmed
latest_grouped = df.groupby( 'district' )['confirmed'].sum().reset_index()
confirmed = latest_grouped.sort_values( 'confirmed', ascending=False )[:20][::-1]
district_confirmed = pd.Series( confirmed['confirmed'] ).tolist()
district_confirmed_names = pd.Series( confirmed['district'] ).tolist()

# District with most active cases
latest_grouped = df.groupby('district')['active'].sum().reset_index()
active = latest_grouped.sort_values( 'active', ascending=False )[:20][::-1]
district_active = pd.Series( active['active'] ).tolist()
district_active_names = pd.Series( active['district'] ).tolist()

# District with most deaths
latest_grouped = df.groupby('district')['deceased'].sum().reset_index()
deaths = latest_grouped.sort_values( 'deceased', ascending=False )[:20][::-1]
district_deaths = pd.Series( deaths['deceased'] ).tolist()
district_deaths_names = pd.Series( deaths['district'] ).tolist()

# District recovery
latest_grouped = df.groupby('district')['recovered'].sum().reset_index()
recovery = latest_grouped.sort_values('recovered', ascending=False)[:20][::-1]
district_recovered = pd.Series( recovery['recovered'] ).tolist()
district_recovered_names = pd.Series( recovery['district'] ).tolist()
