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
import zipfile

# development
file_loc = ''  # deploy
from services.fetch import get  # deploy
# from news_api import API_KEY
'''
# build
file_loc = '.' # production
from fetch import get # production
# from news_api import API_KEY # production
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

def raw_data_update():
    print('Fetching and updating raw data')
    #global raw_data
    raw_data = getData( Data.raw_data )
    raw_data[0].rename( columns={'Num cases': 'Num Cases'}, inplace=True )
    raw_data[1].rename( columns={'Num cases': 'Num Cases'}, inplace=True )

    df = pd.DataFrame()


    for data in raw_data:
        df = df.append(data, ignore_index=True)


    df = df[df['Age Bracket'] != '28-35']
    df = df[df['Age Bracket'] != '8 Months']
    df = df[df['Age Bracket'] != '6 Months']
    df = df[df['Age Bracket'] != '5 months']
    # print(type(df))
    df.to_csv( file_loc + './data/raw_data.csv', index=False, date_format="%Y-%m-%d %H:%M:%S")

def death_and_recovery_update():
    death_and_recovered = getData( Data.death_and_recovered )


def district_wise():
    print('Updating district wise')
    state_district_wise = get( 'https://api.covid19india.org/v2/state_district_wise.json' )

    df = pd.DataFrame( columns=['district', 'notes', 'active', 'confirmed', 'deceased', 'recovered', 'delta.confirmed',
                                'delta.deceased', 'delta.recovered'] )
    state_district_wise = state_district_wise.json()

    for row in state_district_wise:
        state_district_wise = row
        data = json_normalize( state_district_wise )
        state = json_normalize( data['districtData'][0] )
        df = df.append( state )

    df = df[["district", "active", "confirmed", "deceased", "recovered"]]
    df = df[df.district != "Unknown"]

    # latest_grouped = df.groupby( 'district' )['confirmed'].sum().reset_index()

    df.to_csv( file_loc + './data/district_wise.csv', index=False, date_format="%Y-%m-%d %H:%M:%S" )



def testing_data():
    print('Updating testing data')
    testing_data = get( 'https://api.covid19india.org/state_test_data.json' )
    testing_data = testing_data.json()
    testing_data = json_normalize(testing_data)
    testing_data = pd.DataFrame.from_dict( testing_data['states_tested_data'][0] )
    testing_data = testing_data[testing_data['updatedon'] != '']

    testing_data['updatedon'] = pd.to_datetime( testing_data['updatedon'], format='%d/%m/%Y' )
    testing_data = testing_data[testing_data['totaltested'] != '14/04/2020']
    testing_data.replace( to_replace="", value="0", inplace=True )  ######VERY CRUCIAL, WITHOUT THIS CODE BREAKS, IDK WHY THOUGH {TOOK 30 MIN TO FIND}
    testing_data.replace( to_replace=" ", value="0", inplace=True )  ## NEW Type of issue addressed here! (More efficient code will be written in a later version so that such probelms do not arise, for now hard-coding till V1.0)

    testing_data['totaltested'] = testing_data['totaltested'].str.replace( ',', '' ).astype( float )
    testing_data['positive'] = testing_data['positive'].str.replace( ',', '' ).astype( float )
    testing_data['negative'] = testing_data['negative'].str.replace( ',', '' ).astype( float )
    testing_data['unconfirmed'] = testing_data['unconfirmed'].str.replace( ',', '' ).astype( float )

    grouped_testing_data = testing_data
    grouped_testing_data = grouped_testing_data.sort_values( ['totaltested'], ascending=False )
    grouped_testing_data = grouped_testing_data.groupby( 'updatedon' )['totaltested', 'positive', 'negative', 'unconfirmed'].sum().reset_index()
    grouped_testing_data.to_csv( file_loc + './data/testing_data.csv', index=False, date_format="%Y-%m-%d %H:%M:%S" )

# testing_data()

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
    try :
        print("File Download Kaggle")
        os.system( 'kaggle datasets download sudalairajkumar/covid19-in-india ' )

    except:
        print("Can't connect to kaggle")

    zip = zipfile.ZipFile( 'covid19-in-india.zip' )
    zip.extract( 'covid_19_india.csv' )
    del zip
    os.remove( 'covid19-in-india.zip' )

    source = 'covid_19_india.csv'
    destination = file_loc + './data/covid_19_india.csv'
    shutil.move( source, destination )

    # print('Kaggle')


def manipulate_raw_data():
    df = pd.read_csv(file_loc + '../data/raw_data.csv')
    df = df[df['Age Bracket'] != '8 Months']
    df = df[df['Age Bracket'] != '28-35']
    df = df[df['Age Bracket'] != '6 Months']
    df = df[df['Age Bracket'] != '5 Months']
    df = df[df['Age Bracket'] != '5 months']
    df = df[df['Age Bracket'] != '9 Months']
    df = df[df['Age Bracket'] != '8 month']
    df = df[df['Age Bracket'] != '1 DAY']
    df = df[df['Age Bracket'] != '9 Month']
    df = df[df['Age Bracket'] != '18-28']


    # df.to_csv( file_loc + './data/raw_data.csv', index=False, date_format="%Y-%m-%d %H:%M:%S")
    df.to_csv('../data/raw_data.csv', index=False, date_format="%Y-%m-%d %H:%M:%S" )

#get_news()

'''
get_govt_data_from_kaggle()
raw_data_update()
district_wise()
testing_data()
'''
# manipulate_raw_data()