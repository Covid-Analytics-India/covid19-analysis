# from flask import Flask, request, make_response
# # from flask_sqlalchemy import SQLAlchemy
# from datetime import datetime

# app = Flask(__name__)

# # # Settting up the DB
# # app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
# # db = SQLAlchemy(app)

# # # DB Model
# # class Todo(db.Model):
# #     id = db.Column(db.Integer, primary_key=True)
# #     content = db.Column(db.String(200), nullable=False)
# #     date_created = db.Column(db.DateTime, default=datetime.utcnow)

# #     def __repr__(self):
# #         return '<Task %r>' % self.id

# @app.route('/', methods=['GET', 'POST'])
# def index():
#     if request.method == 'POST':
#         return {"hello": "World", "method": "POST"}
#     else:
#         return {"hello": "World", "method": "GET"}

# @app.route('/api', methods=['GET', 'POST'])
# def getAPI():
#     if request.method == 'GET':
#         return make_response({"hello": "API", "method": "GET"}, 201)
#     else:
#         return {"hello": "API", "method": "POST"}

# @app.route('/api/time', methods=['GET', 'POST'])
# def getTime():
#     if request.method == 'GET':
#         return {"time": datetime.utcnow}
#     else:
#         return {"hello": "API", "method": "POST"}

# if __name__ == "__main__" :
#     app.run(debug=True)

import warnings
# import numpy as np
import pandas as pd
# from datetime import datetime
# import os
# import glob
from bs4 import BeautifulSoup
import json
from flask import Flask
import requests
app = Flask(__name__)
warnings.simplefilter( 'ignore' )

def get(url):
    try:
        response = requests.get( url )
        print( f"Request returned {response.status_code} : '{response.reason}'" )
        return response.json()
    except requests.HTTPError:
        print( response.status_code, response.reason )
        raise


# Fetching and Parsing the data
raw_data = get( 'https://api.covid19india.org/raw_data.json' )
raw_data = raw_data['raw_data']

"""## Fetching State wise Data"""

from datetime import datetime
# import os
# import glob
# from bs4 import BeautifulSoup

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
'''
# Import gdrive
from google.colab import drive
drive.mount('/content/gdrive')
'''
# Adding new data to old
# file_loc = 'gdrive/My Drive/Covid19/day_by_day_data/'
file_loc = ''
prev_data = pd.read_csv( 'complete_statewise.csv' )

prev_data = prev_data.rename( columns={'Cured': 'Cured/Discharged'} )
prev_data = prev_data.rename( columns={'Cured/Discharged': 'Cured/Discharged/Migrated'} )

prev_data['Date'] = pd.to_datetime( prev_data['Date'] )
prev_data = pd.concat( [statewise_data_today, prev_data], ignore_index=True ).sort_values( ['Date'],
                                                                                           ascending=True ).reset_index(
    drop=True )
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
complete_statewise.to_csv( 'complete_statewise.csv', index=False )
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
# print(data.head())
# print(data['Diagnosed date'].max())
# print(data['Status change date'].max())

"""# Understanding the Data"""

# data['Diagnosed date'].sample(5)

# print( "External Data" )
# print( f"First recorded Case: {data['Diagnosed date'].min()}" )
# print( f"Last recorded Case: {data['Diagnosed date'].max()}" )
# print( f"Total Days recorded: {data['Diagnosed date'].max() - data['Diagnosed date'].min()}" )

"""# Data Analysis (COVID - 19)

## Data Wrangling
"""

# data['Age'].describe()

# replacing all the missing values with unknown
data.replace( to_replace="",value="unknown", inplace=True )
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

grouped = data.groupby('Diagnosed date' )['Diagnosed date', 'confirmed'].sum().reset_index()
s = 0
grouped['tot_confirmed'] = grouped['confirmed']
for row in grouped.index:
    grouped['tot_confirmed'][row] += s
    s = grouped['tot_confirmed'][row]

@app.route('/')
def index():
    return 'Hello World!'

@app.route('/day_wise_confirmed')
def day_wise_confirmed():
    diagnosed_date = grouped['Diagnosed date']
    #print(type(diagnosed_date))
    total_confirmed = grouped['tot_confirmed']
    diagnosed_date = diagnosed_date.to_json()
    #diagnosed = json.dumps(diagnosed_date)
    total_confirmed = total_confirmed.to_json()
    #print(type(diagnosed))
    diagnosed = json.loads(diagnosed_date)
    total = json.loads(total_confirmed)
    #print(diagnosed)
    #print(total_confirmed)

    graph_data = {}
    xplots = {}
    yplots = {}
    graph_data['type'] = 'line-graph'
    graph_data['graphTitle'] = "Day Wise Confirmed Cases in India"
    graph_data['xLabel'] = "Diagnosed date"
    graph_data['yLabel'] = "total confirmed"
    xplots = diagnosed
    yplots = total
    graph_data['xpoints'] = xplots
    graph_data['ypoints'] = yplots
    now = datetime.now()
    timestamp = datetime.timestamp(now)
    graph_data['timestamp'] = timestamp
    graph_data['message'] = "graph sent"
    graph_data['status'] = "200"
    print(datetime.now())
    #print("Graph data")
    #graph_data = graph_data.to_json()
    #graph_data = json.loads(graph_data)
    #print(graph_data)
    #print(type(graph_data))
    return (json.dumps(graph_data))

'''
fig2 = px.line( grouped, x="Diagnosed date", y="tot_confirmed",
                title="Day Wise Confirmed Cases in India(Logarithmic Scale)", log_y=True, width=900, height=650 )

# fig.show()
graph1 = dcc.Graph(
    id='graph1',
    figure=fig1,
)
graph2 = dcc.Graph(
    id='graph2',
    figure=fig2,
)

fig3 = px.line( grouped, x="Diagnosed date", y="confirmed", title="Day Wise Encountered Cases in India", width=900,
                height=650 )

# fig.show()

fig4 = px.line( grouped, x="Diagnosed date", y="confirmed",
                title="Day Wise Encountred Cases in India(Logarithmic Scale)", log_y=True, width=900, height=650 )

# fig.show()
graph3 = dcc.Graph(
    id='graph3',
    figure=fig3,
)
graph4 = dcc.Graph(
    id='graph4',
    figure=fig4,
)
complete_statewise['Total Confirmed cases (Including 66 foreign Nationals) '] = complete_statewise['Total Confirmed cases (Including 66 foreign Nationals) '].astype(float)
#cases state wise
state_grouped = complete_statewise.groupby(['Name of State / UT'])['Total Confirmed cases (Including 66 foreign Nationals) '].sum().reset_index()

fig5 = px.bar(state_grouped.sort_values('Total Confirmed cases (Including 66 foreign Nationals) ', ascending=False)[:33][::-1],
             x='Total Confirmed cases (Including 66 foreign Nationals) ', y='Name of State / UT',
             title='Confirmed Cases in Various States in India', text='Total Confirmed cases (Including 66 foreign Nationals) ', height=800,width = 1050, orientation='h')
#fig.show()
graph5 = dcc.Graph(
    id='graph5',
    figure=fig5,
)
# gender pie chart
# Remove all the unknown Genders
df_gender_cleaned = data[data['Gender']!="unknown"]
# Pie Chart
fig6 = px.pie(df_gender_cleaned,values='confirmed', names='Gender')
graph6 = dcc.Graph(
    id='graph6',
    figure=fig6,
)

# Observation, Front-end part
ratio = df_gender_cleaned['Gender'].value_counts()[0] / df_gender_cleaned['Gender'].value_counts()[1]
print("\nAlthough more than 50% of the genders of people affected with covid19 is unknown but from the ones that are known we can see that almost\n{} times the number of Males are getting affected by COVID-19 in India. ".format(0.5*round(ratio/0.5)))


# HTML PART
header = html.H2(children="Testing Covid Analysis" )
row1 = html.Div(children=[graph1])
row2 = html.Div(children=[graph2])
row3 = html.Div(children=[graph3])
row4 = html.Div(children=[graph4])
row5 = html.Div(children=[graph5])
row6 = html.Div(children=[graph6])

layout = html.Div(children=[header, row1, row2, row3, row4, row5, row6], style={"text-align": "center"} )

app.layout = layout
'''
if __name__ == "__main__":
    app.run( debug=True )