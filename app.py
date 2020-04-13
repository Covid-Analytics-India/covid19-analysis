from datetime import datetime
import warnings
import pandas as pd
import json
from flask import Flask
import requests
from flask_cors import CORS, cross_origin
from services.processes import apiResponse
from services.country_wise import grouped
from services.travel_history import notes_cleaned

app = Flask( __name__ )
cors = CORS( app )
app.config['CORS_HEADERS'] = 'Content-Type'
warnings.simplefilter('ignore')


# def __init__():
#    raw_data = [1, 2, 3]

def myconverter(o):  # datetime to JSON converter
    if isinstance( o, datetime ):
        date_time = datetime.fromtimestamp(o.timestamp())  # can change to string o.__str
        time = date_time.strftime("%d %B %Y")
        return time
        #return o.timestamp()


@app.route( '/' )
def index():
    return 'Hello World!'


@app.route('/api/fetch_api_status', methods=['GET'])
def fetch_from_api():
    if(apiResponse.status_code == 200):
        return {"status": True}
    else:
        return {"status": False}

@app.route( '/api/day_wise_confirmed', methods=['GET'] )
def day_wise_confirmed():

    #diagnosed_date = pd.Series( grouped['Diagnosed date'] ).tolist()
    #print(diagnosed_date)
    #total_confirmed = pd.Series( grouped['tot_confirmed'] ).tolist()

    graph_data = grouped[['Diagnosed date', 'tot_confirmed']].to_dict('records')
    return json.dumps(graph_data, default=myconverter)

@app.route('/api/day_wise_encountered', methods=['GET'])
def day_wise_encountered():
    diagnosed_date = pd.Series( grouped['Diagnosed date'] ).tolist()
    confirmed = pd.Series( grouped['confirmed']).tolist()
    '''
    graph_data = {
        'type': 'line-graph',
        'graphTitle': "Day Wise Encountered Cases in India",
        'xLabel': "Diagnosed date",
        'yLabel': "confirmed",
        'xPoints': diagnosed_date,
        'yPoints': confirmed,
        'timestamp': datetime.timestamp(datetime.utcnow()),
        'message': "graph sent",
        'status': "200"
    }
    '''
    graph_data = grouped[['Diagnosed date', 'confirmed']].to_dict( 'records' )
    return json.dumps(graph_data, default=myconverter)


@app.route('/api/travel_history_analysis')
def travel_history_analysis():
    print(notes_cleaned)
    labels = notes_cleaned['Available Information']
    values = notes_cleaned['confirmed']
    #print(labels)
    print()
    return 'Travel history endpoint'
    #return json.dumps(notes_cleaned)

@app.route('/api/getAll')
def get_all_graphs():
    graphs_data = {
        'countryWise' : {
            'dayWiseConfirmed': grouped[['Diagnosed date', 'tot_confirmed']].to_dict('records'),
            'dayWiseEncountered': grouped[['Diagnosed date', 'confirmed']].to_dict('records'),
        }
    }

    return json.dumps( graphs_data, default=myconverter )

if __name__ == "__main__":
    app.run(debug=True)
