import atexit
# refreshing all imports to get the latest analysis
import importlib
import json
import warnings
from datetime import datetime

# noinspection PyUnresolvedReferences
import services.country_wise
# local module exporting
# noinspection PyUnresolvedReferences
import services.processes
# noinspection PyUnresolvedReferences
import services.statewise.statewise_confirmed
# noinspection PyUnresolvedReferences
import services.travel_history
# noinspection PyUnresolvedReferences
import services.recovered

from apscheduler.schedulers.background import BackgroundScheduler
from flask import Flask
from flask_cors import CORS

app = Flask( __name__ )
cors = CORS( app )
app.config['CORS_HEADERS'] = 'Content-Type'
warnings.simplefilter( 'ignore' )


# diagnosed date string format mein aa rha hai

def update():
    # updating database
    services.processes.update_database()
    services.processes.update_database2()
    # updating imports
    importlib.reload( services.statewise.statewise_confirmed )
    importlib.reload( services.country_wise )
    importlib.reload( services.travel_history )


scheduler = BackgroundScheduler()
scheduler.add_job( func=update, trigger='interval', seconds=3600 )  # updating in every 1 hour
scheduler.start()
atexit.register( lambda: scheduler.shutdown() )


# t = threading.Thread(target=update)
# t.start()


def myconverter(o):  # datetime to JSON converter
    if isinstance( o, datetime ):
        # date_time = datetime.fromtimestamp(o.timestamp())  # can change to string o.__str
        # time = date_time.strftime("%d %B %Y")
        # return time
        return o.timestamp()


@app.route( '/' )
def index():
    return 'Hello World!'


@app.route( '/api/day_wise_confirmed', methods=['GET'] )
def day_wise_confirmed():
    graph_data = {
        'x': services.country_wise.diagnosed_date,
        'y': services.country_wise.day_wise_confirmed,
        'type': 'line',
        'title': 'Day wise confirmed cases in India',
        'x_label': 'Diagnosed Date',
        'y_label': 'Total cases confirmed'
    }

    return json.dumps( graph_data, default=myconverter )


@app.route( '/api/day_wise_encountered', methods=['GET'] )
def day_wise_encountered():
    graph_data = {
        'x': services.country_wise.diagnosed_date,
        'y': services.country_wise.day_wise_encountered,
        'type': 'line',
        'title': 'Day wise confirmed cases in India',
        'x_label': 'Diagnosed Date',
        'y_label': 'Total cases confirmed'
    }

    return json.dumps( graph_data, default=myconverter )


@app.route('/api/day_wise_recovered', methods=['GET'])
def day_wise_recovered():
    graph_data = {
        'x': services.recovered.recovery_dates,
        'y': services.recovered.recovery_daywise,
        'title':'Recoveries Day wise in india',
        'x_label' : 'Date',
        'y_label': 'recovered',
        'type': 'line'
    }
    return json.dumps( graph_data, default=myconverter )


@app.route( '/api/day_wise_recovered_cumulative', methods=['GET'] )
def day_wise_recovered_cumulative():
    graph_data = {
        'x': services.recovered.recovery_dates,
        'y': services.recovered.recovery_cumulative,
        'title': 'Recovered cases in India(Cumulative)',
        'x_label': 'Date',
        'y_label': 'Total recovered',
        'type': 'line'
    }
    return json.dumps( graph_data, default=myconverter )


@app.route( '/api/travel_history_analysis', methods=['GET'] )
def travel_history_analysis():
    graph_data = [{
        'values': services.travel_history.pie_data_percentage,
        'labels': services.travel_history.pie_data_travel,
        'type': 'pie',
        'title': 'Travel history analysis'
    }]

    return json.dumps( graph_data )


@app.route( '/api/state_wise_confirmed' )
def state_wise_confirmed():
    # horizontal bar-graph
    graph_data = [{
        'x': services.statewise.statewise_confirmed.statewise_confirmed,
        'y': services.statewise.statewise_confirmed.statewise_confirmed_statename,
        'orientation': 'h',
        'type': 'bar',
        'title': 'Total Number of Confirmed cases in Various States till Date'
    }]

    return json.dumps( graph_data )


@app.route( '/api/get_all' )
def get_all_graphs():
    graphs_data = {
        'country_wise': {
            'day_wise_confirmed': {
                'x': services.country_wise.diagnosed_date,
                'y': services.country_wise.day_wise_confirmed,
                'type': 'line',
                'title': 'Day wise Total confirmed cases in India(cumulative)',
                'x_label': 'Diagnosed Date',
                'y_label': 'Total cases confirmed'
            },

            'day_wise_encountered': {
                'x': services.country_wise.diagnosed_date,
                'y': services.country_wise.day_wise_encountered,
                'type': 'line',
                'title': 'Day wise confirmed cases in India',
                'x_label': 'Diagnosed Date',
                'y_label': 'Total cases confirmed'
            },
            'day_wise_recovered_cumulative' : {
                'x': services.recovered.recovery_dates,
                'y': services.recovered.recovery_cumulative,
                'title': 'Recovered cases in India(Cumulative)',
                'x_label': 'Date',
                'y_label': 'Total recovered',
                'type': 'line'
            },
            'day_wise_recovered' : {
                'x': services.recovered.recovery_dates,
                'y': services.recovered.recovery_daywise,
                'title': 'Recoveries Day wise in india',
                'x_label': 'Date',
                'y_label': 'recovered',
                'type': 'line'
            }

        },
        'state_wise': {
            'state_wise_confirmed': [{
                'x': services.statewise.statewise_confirmed.statewise_confirmed,
                'y': services.statewise.statewise_confirmed.statewise_confirmed_statename,
                'orientation': 'h',
                'type': 'bar',
                'title': 'Total Number of Confirmed cases in Various States till Date'
            }]
        },
        'travel_history_analysis': [{
            'values': services.travel_history.pie_data_percentage,
            'labels': services.travel_history.pie_data_travel,
            'type': 'pie',
            'title': 'Travel history analysis'
        }]
    }

    return json.dumps( graphs_data, default=myconverter )


if __name__ == "__main__":
    app.run( debug=True )  # for deployment turn it off(False)
