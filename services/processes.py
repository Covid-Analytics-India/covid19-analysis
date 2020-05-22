import warnings
from builtins import len
import shutil
import os
import pandas as pd
from pandas.io.json import json_normalize
#import requests

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
def update_database_merge():
    print('Fetching and updating 1')

    apiResponse1 = get( 'https://api.covid19india.org/raw_data1.json' )
    apiResponse2 = get( 'https://api.covid19india.org/raw_data2.json' )
    apiResponse3 = get( 'https://api.covid19india.org/raw_data3.json' )
    # print("Processes", apiResponse.status_code)

    #print(apiResponse)
    if (apiResponse1.status_code == 200):
        raw_data1 = apiResponse1.json()
        raw_data2 = apiResponse2.json()
        raw_data3 = apiResponse3.json()
        raw_data = raw_data1['raw_data'] + raw_data2['raw_data'] + raw_data3['raw_data']
        # JSON to dataframe
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

        # converting the string values to datetime object
        data['Diagnosed date'] = pd.to_datetime( data['Diagnosed date'], dayfirst=True )
        data['Status change date'] = pd.to_datetime( data['Status change date'], dayfirst=True )

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


        data.to_csv( file_loc + './data/data-copy.csv', index=False, date_format="%Y-%m-%d %H:%M:%S")
        #print( 'raw data complete' )

    else:
        print( "Connection error" )

def update_database():
    print('Fetching and updating 1')
    apiResponse = get( 'https://api.covid19india.org/raw_data.json' )
    # print("Processes", apiResponse.status_code)

    #print(apiResponse)
    if (apiResponse.status_code == 200):
        raw_data = apiResponse.json()
        raw_data = raw_data['raw_data']
        # JSON to dataframe
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

        # converting the string values to datetime object
        data['Diagnosed date'] = pd.to_datetime( data['Diagnosed date'], dayfirst=True )
        data['Status change date'] = pd.to_datetime( data['Status change date'], dayfirst=True )

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


        data.to_csv( file_loc + './data/data.csv', index=False, date_format="%Y-%m-%d %H:%M:%S")
        #print( 'raw data complete' )

    else:
        print( "Connection error" )

def update_database2():
    state_district_wise = get( 'https://api.covid19india.org/v2/state_district_wise.json' )

    df = pd.DataFrame( columns=['district', 'notes', 'active', 'confirmed', 'deceased', 'recovered', 'delta.confirmed',
                                'delta.deceased', 'delta.recovered'] )

    state_district_wise = state_district_wise.json()
    #print(state_district_wise)
    #print(json_normalize(state_district_wise.to_dict()))
    for row in state_district_wise:
        state_district_wise = row
        data = json_normalize( state_district_wise)
        state = json_normalize( data['districtData'][0] )
        df = df.append( state )
    df = df[["district", "active", "confirmed", "deceased", "recovered"]]
    df = df[df.district != "Unknown"]
    df.to_csv( file_loc + './data/district_wise.csv', index=False, date_format="%Y-%m-%d %H:%M:%S" )


def Insert_row_(row_number, df, row_value):
    # Slice the upper half of the dataframe
    df1 = df[0:row_number]

    # Store the result of lower half of the dataframe
    df2 = df[row_number:]

    # Inser the row in the upper half dataframe
    df1.loc[row_number] = row_value

    # Concat the two dataframes
    df_result = pd.concat( [df1, df2] )

    # Reassign the index labels
    df_result.index = [*range( df_result.shape[0] )]

    # Return the updated dataframe
    return df_result


def get_govt_data_from_kaggle():
    #os.system('kaggle competitions list')
    try :
        os.system( 'kaggle datasets download -f complete.csv imdevskp/covid19-corona-virus-india-dataset')
    except:
        print("Can't connect to kaggle")

    # Let's create a row which we want to insert
    row_number = 930
    row_value = ['2020-04-13', 'Meghalaya', 0, 0, 0, 25.4670, 91.3662, 0, 1]
    try:
        govt_data = pd.read_csv('complete.csv')
        govt_data = Insert_row_( row_number, govt_data, row_value )
    except FileNotFoundError:
        govt_data = pd.read_csv(file_loc + './data/complete.csv')

    govt_data.to_csv('complete.csv') #date_format="%Y-%m-%d %H:%M:%S"
    source = './complete.csv'
    destination = file_loc + './data/complete.csv'
    shutil.move( source, destination)
#update_database()
#update_database2()
#get_govt_data_from_kaggle()
#update_database_merge()