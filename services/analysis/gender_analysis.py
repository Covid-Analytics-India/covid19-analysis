# from services.processes import raw_data
file_loc = ''  # development
# file_loc = '../.' # production


import pandas as pd
import math
'''
# Development
from services.processes import getData, Data
raw_data = getData(Data.raw_data)
# print(raw_data)
# -------------
'''
raw_data = pd.read_csv(file_loc + './data/raw_data.csv', dtype=object)
#clean_Gender = {'Gender': raw_data[0]['Gender']}
clean_Gender = raw_data['Gender']
'''
for i in range( 1, len( raw_data ) ):
    clean_Gender['Gender'] = clean_Gender['Gender'].append( raw_data[i]['Gender'], ignore_index=True )

clean_Gender = pd.DataFrame(clean_Gender)

# print(clean_Gender)
'''
clean_Gender = clean_Gender.dropna()
clean_Gender = clean_Gender.replace('M ', 'M')
m = 0
f = 0
nb = 0
for gender in clean_Gender:
    if(gender == 'M'):
        m += 1
    elif(gender == 'F'):
        f += 1
    elif (gender == 'Non-Binary') :
        nb += 1

total = clean_Gender.size
male = (m / total ) * 100
female = (f / total ) * 100
non_binary = (nb / total ) * 100
percentage = [male, female, non_binary]
labels = ['Male', 'Female', 'Non-binary']
# print(male, female, non_binary)


# ----------- GENDER AGE CORRELATION-------
'''
clean = {'Gender' : raw_data[0]['Gender'],'Age' : raw_data[0]['Age Bracket']}
for i in range (1, len(raw_data)):
  clean['Gender'] = clean['Gender'].append(raw_data[i]['Gender'],ignore_index=True)
  clean['Age'] = clean['Age'].append(raw_data[i]['Age Bracket'],ignore_index=True)

clean = pd.DataFrame(clean)
'''
df = raw_data
clean_g = {'Gender' : df['Gender'],'Age' : df['Age Bracket']}
# df.set_index('Name', inplace=True)
# print(clean)
clean_g = pd.DataFrame(clean_g)
clean_g.dropna(inplace=True)
clean = {'Age':[], 'Gen':[] }

num = []
for i in range(0,111):
  i = str(i)
  num.append(i)

for row in clean_g.index:
  #print(clean_g['Age'][row])
  if clean_g['Age'][row] in num:
    clean['Age'].append( clean_g['Age'][row])
    clean['Gen'].append( clean_g['Gender'][row])

clean = pd.DataFrame(clean)
clean['Gen'] = clean['Gen'].str.strip()
clean['Age'] = clean['Age'].astype(float)
clean['Age'] = clean['Age'].apply(lambda x: math.floor(x));
# clean['Gender'] = clean['Gender'].str.replace('M ','M')
M = []
F = []
NB = []
for row in clean.index:
    if clean['Gen'][row] == 'M':
        M.append(clean['Age'][row])
    if clean['Gen'][row] == 'F':
        F.append(clean['Age'][row])
    if clean['Gen'][row] == 'Non-Binary':
        NB.append(clean['Age'][row])
# print(M)
# print(F)
# print(NB)
