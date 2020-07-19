import math
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
num = []
for i in range(0,111):
  i = str(i)
  num.append(i)
  clean = []

for age in clean_age['Age']:
  if age in num:
    clean.append(age)

cl = {'Age' : clean}
cl = pd.DataFrame(cl)
cl['Age'] = cl['Age'].astype(float)
cl['Age'].dropna(inplace=True)
cl['Age'] = cl['Age'].apply(lambda x: math.floor(x))


age = pd.Series(cl['Age']).to_list()
# print(age)