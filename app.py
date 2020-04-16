from datetime import date, datetime, timedelta
import warnings
import pandas as pd
import json
from flask import Flask
from dateutil.parser import parse
import requests
from flask_cors import CORS, cross_origin
import services.processes
from services.country_wise import grouped
from services.travel_history import pie_data
from services.statewise.statewise_confirmed import statewise_confirmed_grouped
import threading
import time
app = Flask( __name__ )
cors = CORS( app )
app.config['CORS_HEADERS'] = 'Content-Type'
warnings.simplefilter('ignore')
# diagnosed date string format mein aa rha hai

# def __init__():
#    raw_data = [1, 2, 3]
def update():
    while 1:
        services.processes.update_database()
        services.processes.update_database2()
        time.sleep(3600) # 10 mins
        #time.sleep(10) #testing

t = threading.Thread(target=update)
t.start()


def myconverter(o):  # datetime to JSON converter
    if isinstance( o, datetime ):
        #date_time = datetime.fromtimestamp(o.timestamp())  # can change to string o.__str
        #time = date_time.strftime("%d %B %Y")
        #return time
        return o.timestamp()


@app.route( '/' )
def index():
    return 'Hello World!'

@app.route( '/api/day_wise_confirmed', methods=['GET'] )
def day_wise_confirmed():

    diagnosed = pd.Series( grouped['Diagnosed date'] ).tolist()
    diagnosed_date = [datetime.strptime(x, "%Y-%m-%d %H:%M:%S") for x in diagnosed]
    total_confirmed = pd.Series( grouped['tot_confirmed'] ).tolist()

    graph_data = {
        'x': diagnosed_date,
        'y': total_confirmed,
        'type': 'line',
    }
    #update_database()
    return json.dumps(graph_data, default=myconverter)

@app.route('/api/day_wise_encountered', methods=['GET'])
def day_wise_encountered():
    diagnosed = pd.Series( grouped['Diagnosed date'] ).tolist()
    diagnosed_date = [datetime.strptime( x, "%Y-%m-%d %H:%M:%S" ) for x in diagnosed]
    confirmed = pd.Series( grouped['confirmed']).tolist()

    graph_data = {
        'x': diagnosed_date,
        'y': confirmed,
        'type': 'line',
    }

    return json.dumps(graph_data, default=myconverter)


@app.route('/api/travel_history_analysis')
def travel_history_analysis():
    graph_data = [{
        'values' : pd.Series( pie_data['per'] ).tolist(),
        'labels' : pd.Series( pie_data['travel'] ).tolist(),
        'type' : 'pie'
    }]

    return json.dumps(graph_data)

@app.route('/api/state_wise_confirmed')
def state_wise_confirmed():
    # horizontal bar-graph
    graph_data = [{
        'x': pd.Series(statewise_confirmed_grouped['Confirmed'] ).tolist(),
        'y': pd.Series(statewise_confirmed_grouped['State']).tolist(),
        'orientation': 'h',
        'type': 'bar'
    }]
    return json.dumps(graph_data)

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

