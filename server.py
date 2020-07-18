from flask import Flask, jsonify
import occupation_request
from datetime import datetime
import pandas as pd
import json
import os

myapi = Flask(__name__)

@myapi.route('/', methods=['GET'])
def hello_world():
    message = 'Mi first API. Thanks Miguel Angel\nTest'
    return message

@myapi.route('/occupation/id/<id>/time/<time>', methods=['GET'])
def getImage(id, time):
    """This function return the current capacity of a place

    Args:
        id (string): [place id]
        time (string, optional): [specific time, now eill return current]

    Returns:
        string: current occupation percent
    """    
    if time == 'now':        
        req = occupation_request.get_current_population(id)
    else:
        try:
            date = datetime.strptime((time), '%H:%M')
            req = occupation_request.get_current_population(id, date)
        except:
            req('Please, check time format. Must be H:M')

    return str(req)

@myapi.route('/place/get_ids', methods=['GET'])
def getIds():
    df = pd.read_csv('data/places_with_all.csv', index_col=0)
    return df.place_id.to_dict()

@myapi.route('/place/get_place/id/<id>', methods=['GET'])
def getPlaces(id):
    df = pd.read_csv('data/places_with_all.csv', index_col=0)
    df_dict = df.drop(columns=['lat', 'lng']).loc[df.place_id==id].to_dict('records')
    return json.dumps(df_dict, indent=4, sort_keys=False)
    
