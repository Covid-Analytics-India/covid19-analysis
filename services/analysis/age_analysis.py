from services.processes import raw_data
import pandas as pd
# import boto3
# import requests
# from urllib.request import Request, urlopen
file_loc = ''  # deploy
#file_loc = '../.' # production

'''
# Development
from services.processes import getData, Data
raw_data = getData(Data.raw_data)
# print(raw_data)
# -------------
'''
raw_data = pd.read_csv(file_loc + './data/raw_data.csv', dtype=object)

#raw_data = pd.read_csv('https://covid19analytics-india.s3.amazonaws.com/df.csv', dtype=object)
#raw_data = requests.get('https://covid19analytics-india.s3.amazonaws.com/df.csv')
#raw_data = Request('https://covid19analytics-india.s3.amazonaws.com/df.csv')
# raw_data = urlopen(raw_data).read()
#print(raw_data)
#data = pd.read_csv('https://s3-ap-southeast-2.amazonaws.com/example_bucket/data_1.csv')
#print(data)
clean_age = {'Age' : raw_data['Age Bracket']}
clean_age = pd.DataFrame(clean_age)

clean_age = pd.DataFrame(clean_age)
clean_age = clean_age[clean_age['Age'] != '28-35']
clean_age['Age'] = clean_age['Age'].astype(float)
clean_age['Age'].dropna(inplace=True)


age = pd.Series(clean_age['Age']).to_list()
# print(age)