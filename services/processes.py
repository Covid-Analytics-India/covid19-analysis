import warnings
import numpy as np
import pandas as pd
import json
from datetime import datetime
import os
import glob
from bs4 import BeautifulSoup
from datetime import datetime
import requests
#import threading
#import sys

# deploy
file_loc = ''  # deploy
from services.fetch import get  # deploy

'''
# production
file_loc = '.' # production
from fetch import get  # production
'''

warnings.simplefilter( 'ignore' )
soup=[]
def getDataFromSheet(id, index):
    table = soup.find( id=id ).div.table
    tbody = table.tbody
    body = tbody.find_all( 'tr' )

    body_rows = []

    for tr in body:
        td = tr.find_all( ['th', 'td'] )
        row = [i.text for i in td]
        body_rows.append( row )

    data = pd.DataFrame( body_rows[index:len( body_rows )], columns=body_rows[0] )

    data.drop( data.columns[0], axis='columns', inplace=True )
    return data

def update_database():
    print('Fetching and updating 1')
    apiResponse = get( 'https://api.covid19india.org/raw_data.json' )
    # print("Processes", apiResponse.status_code)

    #print(apiResponse)
    if (apiResponse.status_code == 200):
        raw_data = apiResponse.json()
        raw_data = raw_data['raw_data']
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

        # changing nationality Indian to India
        for ind in data.index:
            if (data['Nationality'][ind] == "Indian"):
                data['Nationality'][ind] = "India"


        data['Diagnosed date'] = pd.to_datetime( data['Diagnosed date'], dayfirst=True )
        data['Status change date'] = pd.to_datetime( data['Status change date'], dayfirst=True )

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


        data.to_csv( file_loc + './data/data.csv', index=False, date_format="%Y-%m-%d %H:%M:%S")
        #print( 'raw data complete' )

    else:
        print( "Connection error" )

def update_database2():
    print( 'Fetching and updating 2' )
    link = 'https://docs.google.com/spreadsheets/d/e/2PACX-1vSz8Qs1gE_IYpzlkFkCXGcL_BqR8hZieWVi-rphN1gfrO3H4lDtVZs4kd0C3P8Y9lhsT1rhoB-Q_cP4/pubhtml#'
    req = requests.get( link )
    print("Parsing")
    global soup
    soup = BeautifulSoup( req.content, "html.parser" )
    print('Parsing done')

    # The Statewise data
    statewise_data = getDataFromSheet( id='1896310216', index=1 )
    statewise_data.drop( statewise_data.index[1], axis='index', inplace=True )
    statewise_data.drop( '', axis=1, inplace=True )
    statewise_data['Confirmed'] = statewise_data['Confirmed'].astype( float )
    statewise_data['Recovered'] = statewise_data['Recovered'].astype( float )
    statewise_data['Deaths'] = statewise_data['Deaths'].astype( float )
    statewise_data['Active'] = statewise_data['Active'].astype( float )
    statewise_data['Delta_Recovered'] = statewise_data['Delta_Confirmed'].astype( float )
    statewise_data['Delta_Deaths'] = statewise_data['Delta_Deaths'].astype( float )
    statewise_data.to_csv(file_loc + './data/statewise_data.csv', date_format="%Y-%m-%d %H:%M:%S")

    # Fetching Death and Recovered Data
    death_and_recovered = getDataFromSheet( id='200733542', index=2 )
    # For death_and_recovered Dataset
    death_and_recovered.drop( [''], axis=1, inplace=True )
    death_and_recovered['Date'] = pd.to_datetime( death_and_recovered['Date'], dayfirst=True )
    death_and_recovered['recovered'] = 0
    death_and_recovered['death'] = 0
    for status in death_and_recovered.index:
        if (death_and_recovered['Patient_Status'][status] == "Recovered"):
            death_and_recovered['recovered'][status] = 1
        elif (death_and_recovered['Patient_Status'][status] == "Deceased"):
            death_and_recovered['death'][status] = 1
        elif (death_and_recovered['Patient_Status'][status] == "Deceased#"):
            death_and_recovered['death'][status] = 1

    death_and_recovered.to_csv(file_loc + './data/death_and_recovered.csv', date_format="%Y-%m-%d %H:%M:%S")

#update_database()
#update_database2()