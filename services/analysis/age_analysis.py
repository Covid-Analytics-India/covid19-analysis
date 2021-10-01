from services.processes import raw_data
import pandas as pd
file_loc = '' 

raw_data = pd.read_csv(file_loc + './data/raw_data.csv', dtype=object)
clean_age = {'Age' : raw_data['Age Bracket']}
clean_age = pd.DataFrame(clean_age)

clean_age = pd.DataFrame(clean_age)
clean_age = clean_age[clean_age['Age'] != '28-35']
clean_age['Age'] = clean_age['Age'].astype(float)
clean_age['Age'].dropna(inplace=True)

clean_age = pd.DataFrame(clean_age)
clean_age = clean_age[clean_age['Age'] != '28-35']
clean_age['Age'] = clean_age['Age'].astype(float)
clean_age['Age'].dropna(inplace=True)


age = pd.Series(clean_age['Age']).to_list()
# print(age)