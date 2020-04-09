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
from datetime import datetime
import warnings
# import numpy as np
import pandas as pd
# from datetime import datetime
# import os
# import glob
#from bs4 import BeautifulSoup
import json
from flask import Flask
import requests
from flask_cors import CORS, cross_origin
from services.processes import grouped, apiResponse
app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
warnings.simplefilter('ignore')

#def __init__():
#    raw_data = [1, 2, 3]

def myconverter(o):  # datetime to JSON converter
    if isinstance( o, datetime ):
        return o.timestamp()  # can change to string o.__str


@app.route('/')
def index():
    return 'Hello World!'

@app.route('/fetch', methods=['GET'])
def fetch_from_api():
    #print("App.py", apiResponse)
    return json.dumps({"status":apiResponse.status_code, "reason":apiResponse.reason})

@app.route( '/api/day_wise_confirmed', methods=['GET'])
def day_wise_confirmed():

    # diagnosed_date = grouped['Diagnosed date']
    # print(type(diagnosed_date))
    diagnosed_date = pd.Series( grouped['Diagnosed date'] ).tolist()
    # print(ser)
    # print(ser[1])
    total_confirmed = pd.Series( grouped['tot_confirmed'] ).tolist()
    # diagnosed_date = diagnosed_date.to_json()
    # diagnosed = json.dumps(diagnosed_date)
    # total_confirmed = total_confirmed.to_json()
    # print(type(diagnosed))
    # diagnosed = json.loads(diagnosed_date)
    # total = json.loads(total_confirmed)
    # print( diagnosed_date )
    # print( total_confirmed )

    graph_data = {}
    graph_data['type'] = 'line-graph'
    graph_data['graphTitle'] = "Day Wise Confirmed Cases in India"
    graph_data['xLabel'] = "Diagnosed date"
    graph_data['yLabel'] = "total confirmed"
    graph_data['xPoints'] = diagnosed_date
    graph_data['yPoints'] = total_confirmed
    graph_data['timestamp'] = datetime.timestamp(datetime.utcnow())
    graph_data['message'] = "graph sent"
    graph_data['status'] = "200"
    # print(datetime.now())
    # print("Graph data")
    # graph_data = graph_data.to_json()
    # graph_data = json.loads(graph_data)
    # print(graph_data)
    # print(type(graph_data))
    return (json.dumps( graph_data, default=myconverter ))



if __name__ == "__main__":
    app.run( debug=True )
