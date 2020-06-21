# from services.processes import raw_data
import pandas as pd
file_loc = ''  # development
# file_loc = '../.' # build

'''
# build
from services.processes import getData, Data
raw_data = getData(Data.raw_data)
# print(raw_data)
# -------------
'''
raw_data = pd.read_csv(file_loc + './data/raw_data.csv', dtype=object)
clean_age = {'Age' : raw_data['Age Bracket']}
clean_age = pd.DataFrame(clean_age)

clean_age = pd.DataFrame(clean_age)
'''
clean_age = clean_age[clean_age['Age'] != '28-35' ]
clean_age = clean_age[clean_age['Age'] != '8 Months']
clean_age = clean_age[clean_age['Age'] != '6 Months']
'''
clean_age['Age'] = clean_age['Age'].astype(float)
clean_age['Age'].dropna(inplace=True)


age = pd.Series(clean_age['Age']).to_list()
# print(age)