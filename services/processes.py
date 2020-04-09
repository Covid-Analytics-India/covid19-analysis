import warnings
import numpy as np
import pandas as pd
import json
from datetime import datetime
import os
import glob
from bs4 import BeautifulSoup
import json
from datetime import datetime
import requests

warnings.simplefilter( 'ignore' )
apiResponse = {}
from services.fetch import get # deploy
#from fetch import get  # production
# Fetching and Parsing the data
apiResponse = get( 'https://api.covid19india.org/raw_data.json' )
raw_data = apiResponse.json()
raw_data = raw_data['raw_data']

"""## Fetching State wise Data"""

"""### Web Scraping"""

# web scrapping

link = 'https://www.mohfw.gov.in/'
req = requests.get( link )
soup = BeautifulSoup( req.content, "html.parser" )

thead = soup.find_all( 'thead' )[-1]
# print(thead)
head = thead.find_all( 'tr' )

tbody = soup.find_all( 'tbody' )[-1]
body = tbody.find_all( 'tr' )

# print(rows)

head_rows = []
body_rows = []

for tr in head:
    td = tr.find_all( ['th', 'td'] )
    row = [i.text for i in td]
    head_rows.append( row )

for tr in body:
    td = tr.find_all( ['th', 'td'] )
    row = [i.text for i in td]
    body_rows.append( row )

# print(head_rows)

df_bs = pd.DataFrame( body_rows[:len( body_rows ) - 2], columns=head_rows[0] )
df_bs.drop( 'S. No.', axis=1, inplace=True )
# ---------------------

now = datetime.now()
df_bs['Date'] = now.strftime( "%m/%d/%Y" )
df_bs['Date'] = pd.to_datetime( df_bs['Date'], format='%m/%d/%Y' )

# latitude and longitude information
# ----------------------------------

lat = {'Delhi': 28.7041, 'Haryana': 29.0588, 'Kerala': 10.8505, 'Rajasthan': 27.0238,
       'Telengana': 18.1124, 'Uttar Pradesh': 26.8467, 'Ladakh': 34.2996, 'Tamil Nadu': 11.1271,
       'Jammu and Kashmir': 33.7782, 'Punjab': 31.1471, 'Karnataka': 15.3173, 'Maharashtra': 19.7515,
       'Andhra Pradesh': 15.9129, 'Odisha': 20.9517, 'Uttarakhand': 30.0668, 'West Bengal': 22.9868,
       'Puducherry': 11.9416, 'Chandigarh': 30.7333, 'Chhattisgarh': 21.2787, 'Gujarat': 22.2587,
       'Himachal Pradesh': 31.1048, 'Madhya Pradesh': 22.9734, 'Bihar': 25.0961, 'Manipur': 24.6637,
       'Mizoram': 23.1645, 'Goa': 15.2993, 'Andaman and Nicobar Islands': 11.7401}

long = {'Delhi': 77.1025, 'Haryana': 76.0856, 'Kerala': 76.2711, 'Rajasthan': 74.2179,
        'Telengana': 79.0193, 'Uttar Pradesh': 80.9462, 'Ladakh': 78.2932, 'Tamil Nadu': 78.6569,
        'Jammu and Kashmir': 76.5762, 'Punjab': 75.3412, 'Karnataka': 75.7139, 'Maharashtra': 75.7139,
        'Andhra Pradesh': 79.7400, 'Odisha': 85.0985, 'Uttarakhand': 79.0193, 'West Bengal': 87.8550,
        'Puducherry': 79.8083, 'Chandigarh': 76.7794, 'Chhattisgarh': 81.8661, 'Gujarat': 71.1924,
        'Himachal Pradesh': 77.1734, 'Madhya Pradesh': 78.6569, 'Bihar': 85.3131, 'Manipur': 93.9063,
        'Mizoram': 92.9376, 'Goa': 74.1240, 'Andaman and Nicobar Islands': 92.6586}

df_bs['Latitude'] = df_bs['Name of State / UT'].map( lat )
df_bs['Longitude'] = df_bs['Name of State / UT'].map( long )

statewise_data_today = df_bs
file_loc = '' # deploy
#file_loc = '.' # production

prev_data = pd.read_csv(file_loc + './data/complete_statewise.csv' )

prev_data = prev_data.rename( columns={'Cured': 'Cured/Discharged'} )
prev_data = prev_data.rename( columns={'Cured/Discharged': 'Cured/Discharged/Migrated'} )

prev_data['Date'] = pd.to_datetime( prev_data['Date'] )
prev_data = pd.concat( [statewise_data_today, prev_data], ignore_index=True ).sort_values( ['Date'],ascending=True ).reset_index(drop=True )
prev_data = prev_data.sort_values( ['Date', 'Name of State / UT'] ).reset_index( drop=True )

cols = ['Total Confirmed cases (Indian National)', 'Total Confirmed cases ( Foreign National )',
        'Cured/Discharged/Migrated', 'Death']

prev_data[cols] = prev_data[cols].fillna( 0 ).astype( 'int' )

prev_data['Name of State / UT'].replace( 'Chattisgarh', 'Chhattisgarh', inplace=True )
prev_data['Name of State / UT'].replace( 'Pondicherry', 'Puducherry', inplace=True )

complete_statewise = prev_data.drop_duplicates( subset=['Date', 'Name of State / UT'], keep='first',
                                                inplace=False ).reset_index( drop=True )

# use this dataframe to do analysis
# complete_statewise
# save data
complete_statewise.to_csv( file_loc + './data/complete_statewise.csv', index=False )
# changing the column names
complete_statewise = complete_statewise.rename( columns={
    "Total Confirmed cases (Including 51 foreign Nationals) ": "Total Confirmed cases (Including 51 foreign Nationals)"} )

complete_statewise['Name of State / UT'].unique()

"""# Date Reading and Cleaning (From two different Sources)"""

# JSON to dataframe
from pandas.io.json import json_normalize

data = json_normalize( raw_data )

data = data.rename( columns={"patientnumber": "ID",
                             "statepatientnumber": "Government id",
                             "dateannounced": "Diagnosed date",
                             "agebracket": "Age",
                             "gender": "Gender",
                             "detectedcity": "Detected city",
                             "detecteddistrict": "Detected district",
                             "detectedstate": "Detected state",
                             "nationality": "Nationality",
                             "currentstatus": "Current status",
                             "statuschangedate": "Status change date",
                             "_d180g": "Notes",
                             "backupnotes": "Backup notes",
                             "contractedfromwhichpatientsuspected": "Contracted from which Patient (Suspected)",
                             "estimatedonsetdate": "Estimated on set date",
                             "source1": "Source 1",
                             "source2": "Source 2",
                             "source3": "Source 3"}
                    )

# converting the string values to datetime object
data['Diagnosed date'] = pd.to_datetime( data['Diagnosed date'], dayfirst=True )
data['Status change date'] = pd.to_datetime( data['Status change date'], dayfirst=True )

"""# Understanding the Data"""

"""# Data Analysis (COVID - 19)

## Data Wrangling
"""

# data['Age'].describe()

# replacing all the missing values with unknown
data.replace( to_replace="", value="unknown", inplace=True )
# creating new columns depicting the current status of patient
data['recovered'] = 0
data['active'] = 0
data['death'] = 0
data['unknown'] = 0
data['confirmed'] = 1

for status in data.index:
    if (data['Current status'][status] == "Hospitalized"):
        data['active'][status] = 1
    elif (data['Current status'][status] == "Recovered"):
        data['recovered'][status] = 1
    elif (data['Current status'][status] == "Deceased"):
        data['death'][status] = 1
    else:
        data['unknown'][status] = 1

# data[['Current status', 'recovered', 'active', 'death', 'unknown']].sample( 5 )

"""## 1. Confirmed Cases Over Time

## Total Confirmed Cases
"""


