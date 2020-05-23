# refreshing all imports to get the latest analysis
# for deployment turn it off(False)
# TODO: REMOVE DEBUG CONSTANT BEFORE DEPLOYMENT
import atexit
import importlib
import json
import warnings
from builtins import isinstance
from datetime import datetime


# local module exporting
# add the below modules to auto reloading function
# noinspection PyUnresolvedReferences
import services.processes
# noinspection PyUnresolvedReferences
#import services.country_wise_confirmed
# noinspection PyUnresolvedReferences
import services.statewise.statewise_confirmed_recovered_deaths
# noinspection PyUnresolvedReferences
import services.travel_history
# noinspection PyUnresolvedReferences
import services.country_wise_confirmed_recovered_and_deaths
# noinspection PyUnresolvedReferences
import services.district_wise.district_all

from apscheduler.schedulers.background import BackgroundScheduler
from flask import Flask
from flask_cors import CORS
from flask_restplus import Resource, Api, fields
from werkzeug.utils import cached_property
from werkzeug.contrib.fixers import ProxyFix
from flask_swagger_ui import get_swaggerui_blueprint

app = Flask( __name__ )
### swagger specific ###
SWAGGER_URL = '/swagger'
API_URL = '/static/swagger.json'
SWAGGERUI_BLUEPRINT = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "covid19analytics"
    }
)
app.register_blueprint(SWAGGERUI_BLUEPRINT, url_prefix=SWAGGER_URL)
### end swagger specific ###

app.wsgi_app = ProxyFix(app.wsgi_app)
api = Api(app,
          version='0.1',
          title='Our sample API',
          description='This is our sample API'
)

cors = CORS( app )
app.config['CORS_HEADERS'] = 'Content-Type'
warnings.simplefilter( 'ignore' )


# diagnosed date string format mein aa rha hai
'''
def update():

    # updating database
    services.processes.update_database()
    services.processes.update_database2()
    services.processes. get_govt_data_from_kaggle()

    # updating imports
    importlib.reload(services.statewise.statewise_confirmed_recovered_deaths )
    importlib.reload(services.country_wise_confirmed )
    importlib.reload(services.travel_history )
    importlib.reload(services.country_wise_recovered_and_deaths )
    importlib.reload(services.district_wise.district_all)


scheduler = BackgroundScheduler()
scheduler.add_job( func=update, trigger='interval', seconds=3600 )  # updating in every 1 hour
scheduler.start()
atexit.register( lambda: scheduler.shutdown() )

'''
# t = threading.Thread(target=update)
# t.start()


def myconverter(o):  # datetime to JSON converter
    if isinstance( o, datetime ):
        date_time = datetime.fromtimestamp(o.timestamp())  # can change to string o.__str
        time = date_time.strftime("%d %B %Y")
        return time
        #return o.timestamp()


@app.route( '/' )
def index():
    return 'Hello World!'


@app.route('/api/update')
def update():
    print("Updating DB")
    # updating database
    #services.processes.update_database()
    #services.processes.update_database2()
    services.processes. get_govt_data_from_kaggle()

    # updating imports
    importlib.reload(services.statewise.statewise_confirmed_recovered_deaths )
    importlib.reload(services.country_wise_confirmed_recovered_and_deaths )
    importlib.reload(services.travel_history )
    #importlib.reload( services.country_wise_confirmed_recovered_and_deaths )
    importlib.reload(services.district_wise.district_all)

    return 'Data updated'



@app.route( '/api/day_wise_confirmed', methods=['GET'] )
def day_wise_confirmed():
    graph_data = {
        'x': services.country_wise_confirmed_recovered_and_deaths.dates,
        'y': services.country_wise_confirmed_recovered_and_deaths.day_wise_confirmed_overall,
        'type': 'line',
        'title': 'Day wise confirmed cases in India(Cumulative)',
        'x_label': 'Diagnosed Date',
        'y_label': 'Total cases confirmed'
    }

    return json.dumps( graph_data, default=myconverter )


@app.route( '/api/day_wise_encountered', methods=['GET'] )
def day_wise_encountered():
    graph_data = {
        'x': services.country_wise_confirmed_recovered_and_deaths.dates,
        'y': services.country_wise_confirmed_recovered_and_deaths.day_wise_encountered,
        'type': 'line',
        'title': 'Day wise confirmed cases in India',
        'x_label': 'Diagnosed Date',
        'y_label': 'Total cases confirmed'
    }

    return json.dumps( graph_data, default=myconverter )


@app.route('/api/day_wise_recovered', methods=['GET'])
def day_wise_recovered():
    graph_data = {
        'x': services.country_wise_confirmed_recovered_and_deaths.dates,
        'y': services.country_wise_confirmed_recovered_and_deaths.recovery_daywise,
        'title':'Recoveries Day wise in india',
        'x_label' : 'Date',
        'y_label': 'recovered',
        'type': 'line'
    }
    return json.dumps( graph_data, default=myconverter )


@app.route( '/api/day_wise_recovered_cumulative', methods=['GET'] )
def day_wise_recovered_cumulative():
    graph_data = {
        'x': services.country_wise_confirmed_recovered_and_deaths.dates,
        'y': services.country_wise_confirmed_recovered_and_deaths.recovery_cumulative,
        'title': 'Recovered cases in India(Cumulative)',
        'x_label': 'Date',
        'y_label': 'Total recovered',
        'type': 'line'
    }
    return json.dumps( graph_data, default=myconverter )

@app.route( '/api/day_wise_deaths', methods=['GET'] )
def day_wise_deaths():
    graph_data = {
        'x': services.country_wise_confirmed_recovered_and_deaths.dates,
        'y': services.country_wise_confirmed_recovered_and_deaths.death_day_wise,
        'title': 'Deaths Day wise in India',
        'x_label': 'Date',
        'y_label': 'Total Deaths',
        'type': 'line'
    }
    return json.dumps( graph_data, default=myconverter )

@app.route( '/api/day_wise_deaths_cumulative', methods=['GET'] )
def day_wise_deaths_cumulative():
    graph_data = {
        'x': services.country_wise_confirmed_recovered_and_deaths.dates,
        'y': services.country_wise_confirmed_recovered_and_deaths.death_cumulative,
        'title': 'Deaths(Cumulative) wise in India',
        'x_label': 'Date',
        'y_label': 'Total Deaths',
        'type': 'line'
    }
    return json.dumps( graph_data, default=myconverter )


@app.route( '/api/travel_history_analysis', methods=['GET'] )
def travel_history_analysis():
    graph_data = {
        'values': services.travel_history.pie_data_percentage,
        'labels': services.travel_history.pie_data_travel,
        'type': 'pie',
        'title': 'Travel history analysis'
    }

    return json.dumps( graph_data )


@app.route( '/api/state_wise_confirmed' )
def state_wise_confirmed():
    # horizontal bar-graph
    graph_data = {
        'x': services.statewise.statewise_confirmed_recovered_deaths.statewise_confirmed,
        'y': services.statewise.statewise_confirmed_recovered_deaths.statewise_confirmed_names,
        'orientation': 'h',
        'type': 'bar',
        'title': 'Total Number of Confirmed cases in Various States till Date',
        'x_label' : 'Total confirmed cases',
        'y_label' : 'States'
    }

    return json.dumps( graph_data )


@app.route('/api/state_wise_recovered')
def state_wise_recovered():
    graph_data = {
        'x' : services.statewise.statewise_confirmed_recovered_deaths.statewise_recovered_cases,
        'y' : services.statewise.statewise_confirmed_recovered_deaths.statewise_recovered_names,
        'orientation': 'h',
        'type': 'bar',
        'title': 'Total Number of Recovered cases in Various States till Date',
        'x_label': 'Total recovered cases',
        'y_label': 'States'
    }

    return json.dumps(graph_data)


@app.route('/api/state_wise_deaths')
def state_wise_deaths():
    graph_data = {
        'x' : services.statewise.statewise_confirmed_recovered_deaths.statewise_deaths,
        'y' : services.statewise.statewise_confirmed_recovered_deaths.statewise_deaths_names,
        'orientation': 'h',
        'type': 'bar',
        'title': 'Total Number of Deaths in Various States till Date',
        'x_label': 'Total deaths',
        'y_label': 'States'
    }

    return json.dumps(graph_data)


@app.route('/api/district_wise_confirmed', methods=['GET'])
def district_wise_confirmed():
    graph_data = {
        'x': services.district_wise.district_all.district_confirmed,
        'y': services.district_wise.district_all.district_confirmed_names,
        'orientation': 'h',
        'type': 'bar',
        'title': 'Most affected Districts',
        'x_label': 'Confirmed cases',
        'y_label': 'District'
    }
    return json.dumps(graph_data)


@app.route('/api/district_wise_active', methods=['GET'])
def district_wise_active():
    graph_data = {
        'x': services.district_wise.district_all.district_active,
        'y': services.district_wise.district_all.district_active_names,
        'orientation': 'h',
        'type': 'bar',
        'title': 'Total Number of Active cases in Various Districts',
        'x_label': 'Active cases',
        'y_label': 'District'
    }

    return json.dumps(graph_data)


@app.route('/api/district_wise_recovery', methods=['GET'])
def district_wise_recovery():
    graph_data = {
        'x': services.district_wise.district_all.district_recovered,
        'y': services.district_wise.district_all.district_recovered_names,
        'orientation': 'h',
        'type': 'bar',
        'title': 'Total Number of Recovered cases in Various Districts',
        'x_label': 'Recovered cases',
        'y_label': 'District'
    }
    return json.dumps(graph_data)

@app.route('/api/district_wise_deaths', methods=['GET'])
def district_wise_deaths():
    graph_data = {
        'x': services.district_wise.district_all.district_deaths,
        'y': services.district_wise.district_all.district_deaths_names,
        'orientation': 'h',
        'type': 'bar',
        'title': 'Total Number of Deaths in Various District',
        'x_label': 'Deaths',
        'y_label': 'District'
    }
    return json.dumps(graph_data)


@app.route( '/api/get_all' )
def get_all_graphs():
    graphs_data = {
        'country_wise': {
            'day_wise_confirmed': {
                'x': services.country_wise_confirmed_recovered_and_deaths.dates,
                'y': services.country_wise_confirmed_recovered_and_deaths.day_wise_confirmed_overall,
                'type': 'line',
                'title': 'Day wise Total confirmed cases in India(cumulative)',
                'x_label': 'Diagnosed Date',
                'y_label': 'Total cases confirmed'
            },
            'day_wise_encountered': {
                'x': services.country_wise_confirmed_recovered_and_deaths.dates,
                'y': services.country_wise_confirmed_recovered_and_deaths.day_wise_encountered,
                'type': 'line',
                'title': 'Day wise confirmed cases in India',
                'x_label': 'Diagnosed Date',
                'y_label': 'Total cases confirmed'
            },
            'recovered_cumulative' : {
                'x': services.country_wise_confirmed_recovered_and_deaths.dates,
                'y': services.country_wise_confirmed_recovered_and_deaths.recovery_cumulative,
                'title': 'Recovered cases in India(Cumulative)',
                'x_label': 'Date',
                'y_label': 'Total recovered',
                'type': 'line'
            },
            'day_wise_recovered' : {
                'x': services.country_wise_confirmed_recovered_and_deaths.dates,
                'y': services.country_wise_confirmed_recovered_and_deaths.recovery_daywise,
                'title': 'Recoveries Day wise in india',
                'x_label': 'Date',
                'y_label': 'recovered',
                'type': 'line'
            },
            'deaths_cumulative' : {
                'x': services.country_wise_confirmed_recovered_and_deaths.dates,
                'y': services.country_wise_confirmed_recovered_and_deaths.death_cumulative,
                'title': 'Deaths(Cumulative) wise in India',
                'x_label': 'Date',
                'y_label': 'Total Deaths',
                'type': 'line'
            },
            'day_wise_deaths': {
                'x': services.country_wise_confirmed_recovered_and_deaths.dates,
                'y': services.country_wise_confirmed_recovered_and_deaths.death_day_wise,
                'title': 'Deaths(Cumulative) wise in India',
                'x_label': 'Date',
                'y_label': 'Total Deaths',
                'type': 'line'
            }

        },
        'state_wise': {
            'state_wise_confirmed': {
                'x': services.statewise.statewise_confirmed_recovered_deaths.statewise_confirmed,
                'y': services.statewise.statewise_confirmed_recovered_deaths.statewise_confirmed_names,
                'orientation': 'h',
                'type': 'bar',
                'title': 'Total Number of Confirmed cases in Various States till Date',
                'x_label' : 'Total confirmed cases',
                'y_label' : 'States'
            },
            'state_wise_recovered':{
                'x' : services.statewise.statewise_confirmed_recovered_deaths.statewise_recovered_cases,
                'y' : services.statewise.statewise_confirmed_recovered_deaths.statewise_recovered_names,
                'orientation': 'h',
                'type': 'bar',
                'title': 'Total Number of Recovered cases in Various States till Date',
                'x_label': 'Total recovered cases',
                'y_label': 'States'
            },
            'state_wise_deaths': {
                'x': services.statewise.statewise_confirmed_recovered_deaths.statewise_deaths,
                'y': services.statewise.statewise_confirmed_recovered_deaths.statewise_deaths_names,
                'orientation': 'h',
                'type': 'bar',
                'title': 'Total Number of Deaths in Various States till Date',
                'x_label': 'Total Deaths cases',
                'y_label': 'States'
            },
            'state_codes': services.statewise.statewise_confirmed_recovered_deaths.state_code_list
        },
        'district_wise':{
            'district_wise_confirmed' : {
                'x': services.district_wise.district_all.district_confirmed,
                'y': services.district_wise.district_all.district_confirmed_names,
                'orientation': 'h',
                'type': 'bar',
                'title': 'Most affected Districts',
                'x_label': 'Confirmed cases',
                'y_label': 'District'
            },
            'district_wise_active': {
                'x': services.district_wise.district_all.district_active,
                'y': services.district_wise.district_all.district_active_names,
                'orientation': 'h',
                'type': 'bar',
                'title': 'Total number of Active cases in Various Districts',
                'x_label': 'Active cases',
                'y_label': 'District'
            },
            'district_wise_recovered': {
                'x': services.district_wise.district_all.district_recovered,
                'y': services.district_wise.district_all.district_recovered_names,
                'orientation': 'h',
                'type': 'bar',
                'title': 'Total number of Recovered cases in Various Districts',
                'x_label': 'Recovered cases',
                'y_label': 'District'
            },
            'district_wise_deaths': {
                'x': services.district_wise.district_all.district_deaths,
                'y': services.district_wise.district_all.district_deaths_names,
                'orientation': 'h',
                'type': 'bar',
                'title': 'Total number of Deaths in Various Districts',
                'x_label': 'Deaths',
                'y_label': 'District'
            }

        },
        'travel_history_analysis': {
            'values': services.travel_history.pie_data_percentage,
            'labels': services.travel_history.pie_data_travel,
            'type': 'pie',
            'title': 'Travel history analysis'
        }
    }

    return json.dumps( graphs_data, default=myconverter )


if __name__ == "__main__":
    app.run( debug=True )  # for deployment turn it off(False)
