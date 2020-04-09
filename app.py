from datetime import datetime
import warnings
import pandas as pd
import json
from flask import Flask
import requests
from flask_cors import CORS, cross_origin
from services.processes import apiResponse
from services.country_wise import grouped

app = Flask( __name__ )
cors = CORS( app )
app.config['CORS_HEADERS'] = 'Content-Type'
warnings.simplefilter( 'ignore' )


# def __init__():
#    raw_data = [1, 2, 3]

def myconverter(o):  # datetime to JSON converter
    if isinstance( o, datetime ):
        return o.timestamp()  # can change to string o.__str


@app.route( '/' )
def index():
    return 'Hello World!'


@app.route('/api/fetch', methods=['GET'])
def fetch_from_api():
    return json.dumps({"status": apiResponse.status_code, "reason": apiResponse.reason})


@app.route( '/api/day_wise_confirmed', methods=['GET'] )
def day_wise_confirmed():

    diagnosed_date = pd.Series( grouped['Diagnosed date'] ).tolist()
    total_confirmed = pd.Series( grouped['tot_confirmed'] ).tolist()
    graph_data = {
        'type': 'line-graph',
        'graphTitle': "Day Wise Confirmed Cases in India",
        'xLabel': "Diagnosed date",
        'yLabel': "total confirmed",
        'xPoints': diagnosed_date,
        'yPoints': total_confirmed,
        'timestamp': datetime.timestamp(datetime.utcnow()),
        'message': "graph sent",
        'status': "200"
    }
    return json.dumps( graph_data, default=myconverter )


@app.route('/api/day_wise_encountered', methods=['GET'])
def day_wise_encountered():
    diagnosed_date = pd.Series( grouped['Diagnosed date'] ).tolist()
    confirmed = pd.Series( grouped['confirmed'] ).tolist()
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
    return json.dumps(graph_data, default=myconverter)


if __name__ == "__main__":
    app.run(debug=True)
