from flask import Flask, jsonify
import occupation_request
from datetime import datetime
import pandas as pd
import json
import os
from flask_cors import CORS, cross_origin

myapi = Flask(__name__)

@myapi.route('/', methods=['GET'])
@cross_origin()
def hello_world():
    message = '''
    Mi first API. Thanks Miguel-Angel <br/> 
    Directions: <br/> 
    <br/> 
    <b>Get all ids/</b> --> /get_ids <br/>
    <br/>
    <b>Get Current Occupation</b> --> /occupation/id/[id]/time/[time] <br/> 
    &nbsp &nbsp To get now ([time] == now) <br/>
    <br/>
    <b>Get Place details</b> --> /get_place/id/[id] <br/>
    &nbsp &nbsp TODO. Rating. --> I'm working on that... <br/>
    <br/>
    <br/>
    id example --> ChIJk9s5DAQpQg0RGqVnRT1jGMcs
    <br/>
    <br/>
    Enjoy it &#128540
    <br/>
    What about my just learnend HTML?? &#128513
    '''
    return message

@myapi.route('/occupation/id/<id>/time/<time>', methods=['GET'])
@cross_origin()
def getOcc(id, time):
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

@myapi.route('/get_ids', methods=['GET'])
@cross_origin()
def getIds():
    df = pd.read_json('data/Final.json')
    return df.place_id.to_dict()

@myapi.route('/get_place/id/<id>', methods=['GET'])
@cross_origin()
def getPlace(id):
    df = pd.read_json('data/Final.json')
    df_dict = df.drop(columns=['lat', 'lng']).loc[df.place_id==id].to_dict('records')
    return json.dumps(df_dict, indent=4, sort_keys=False)

if __name__ == '__main__':
    myapi.run()