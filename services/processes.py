import warnings
from builtins import len
import shutil
import os
import pandas as pd
from pandas.io.json import json_normalize
import flask
import json
#import requests
import enum

# deploy
file_loc = ''  # deploy
from services.fetch import get  # deploy
# from news_api import API_KEY
'''
# production
file_loc = '.' # production
from fetch import get # production
from news_api import API_KEY # production
'''

'''
from io import StringIO
# import boto3
'''
warnings.simplefilter( 'ignore' )
soup=[]
news = {}
raw_data = {}
class Data(enum.Enum):
  raw_data = 'https://api.covid19india.org/csv/latest/raw_data{}.csv'
  death_and_recovered = 'https://api.covid19india.org/csv/latest/death_and_recovered{}.csv'
  state_wise = 'https://api.covid19india.org/csv/latest/state_wise.csv'
  case_time_series = 'https://api.covid19india.org/csv/latest/case_time_series.csv'
  district_wise = 'https://api.covid19india.org/csv/latest/district_wise.csv'
  state_wise_daily = 'https://api.covid19india.org/csv/latest/state_wise_daily.csv'
  statewise_tested_numbers_data = 'https://api.covid19india.org/csv/latest/statewise_tested_numbers_data.csv'
  tested_numbers_icmr_data = 'https://api.covid19india.org/csv/latest/tested_numbers_icmr_data.csv'
  sources_list = 'https://api.covid19india.org/csv/latest/sources_list.csv'


def getDataFromCsv(link_template, number):
  try:
    df = pd.read_csv(link_template.format(number))
    if not df.empty:
      return {'data': df, 'status': 'ok'}
  except:
    return {'data': None, 'status': 'error'}

def getData(data):
  data_array = []
  i = 1
  while True:
    result = getDataFromCsv(link_template=data.value, number=i)
    if result['status'] != 'error':
      data_array.append(result['data'])
      i += 1
    else:
      break
  return data_array

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


def raw_data_update():
    print('Fetching and updating 1')
    #global raw_data
    raw_data = getData( Data.raw_data )

    df = pd.DataFrame()


    for data in raw_data:
        df = df.append(data, ignore_index=True)

    # print(type(df))
    df.to_csv( file_loc + './data/raw_data.csv', index=False, date_format="%Y-%m-%d %H:%M:%S")
# raw_data_update()
def death_and_recovery_update():
    death_and_recovered = getData( Data.death_and_recovered )


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


def get_news():
    #print(os.environ)
    API_KEY = os.environ.get('NEWS_API_KEY')
    # print(API_KEY)
    # from news_api import API_KEY
    # print(FLASK_ENV)
    link1 = 'https://newsapi.org/v2/everything?language=en&q=india+corona+covid+covid+19+Covid-19+Coronavirus&sortBy=popularity&apiKey=' + API_KEY

    link2 = 'https://newsapi.org/v2/everything?language=en&q=india+corona+covid+covid+19+Covid-19+Coronavirus&sortBy=publishedAt&apiKey=' + API_KEY

    link3 = 'https://newsapi.org/v2/everything?language=hi&q=india+corona+covid+covid+19+Covid-19+Coronavirus&sortBy=popularity&apiKey=' + API_KEY
    link4 = 'https://newsapi.org/v2/everything?language=hi&q=india+corona+covid+covid+19+Covid-19+Coronavirus&sortBy=publishedAt&apiKey=' + API_KEY

    res1 = get(link1)
    en_popularity = res1.json()

    res2 = get( link2 )
    en_published = res2.json()

    res3 = get( link3 )
    hi_popularity = res3.json()

    res4 = get( link4 )
    hi_published = res4.json()

    global news
    news = {
        'en_popularity' : en_popularity,
        'en_published' : en_published,
        'hi_popularity' : hi_popularity,
        'hi_published' : hi_published
    }


    #print("INSIDE PROCESSES \n")
    #print(news)


def get_govt_data_from_kaggle():
    #os.system('kaggle competitions list')
    #data = os.popen( 'kaggle datasets download -f covid_19_india.csv sudalairajkumar/covid19-in-india --force' )
    #print(data.read())

    try :
        # os.system( 'kaggle datasets download -f complete.csv imdevskp/covid19-corona-virus-india-dataset')
        print("File Download")
        # file = 'datasets%2F557629%2F1210473%2Fcovid_19_india.csv'
        os.system( 'kaggle datasets download -f covid_19_india.csv sudalairajkumar/covid19-in-india --force' )
        #os.popen( 'kaggle datasets download -f covid_19_india.csv sudalairajkumar/covid19-in-india --force' )
        
    except:
        print("Can't connect to kaggle")

    # Let's create a row which we want to insert
    #row_number = 930
    # row_value = ['2020-04-13', 'Meghalaya', 0, 0, 0, 25.4670, 91.3662, 0, 1]

    # govt_data = pd.read_csv(file_loc + './data/covid_19_india.csv')
    os.rename('datasets%2F557629%2F1234650%2Fcovid_19_india.csv', 'covid_19_india.csv')
    # govt_data.to_csv('complete.csv') #date_format="%Y-%m-%d %H:%M:%S"
    source = './covid_19_india.csv'
    destination = file_loc + './data/covid_19_india.csv'
    shutil.move( source, destination)
    # print('Kaggle')


#update_database()
#update_database2()
#get_govt_data_from_kaggle()
#update_database_merge()
#get_news()
#raw_data_update()
