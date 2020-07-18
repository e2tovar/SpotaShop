from datetime import datetime
import random
import pandas as pd
import os

def get_current_population(id, date = datetime.now(), df=None):
    '''
        This function function return tne current population of a given place


        Params:
            id([string]) [this is the place id]
            date([timespamp]) [optional, defoult = now()]
            df([DataFrame]) [optional, database]
    '''    
    #read places df, it must have id and 
    if not df:
        #print(os.getcwd())
        places = pd.read_json('data/Final.json')
    else:
        places = df
        
    place = places[places.place_id == id]
    if place.shape[0] == 0:
        ans = "This id is not in database"
        return ans
    
    #get day and hour
    day = date.strftime("%A").lower()
    hour = date.hour

    #get current pop
    current_pop = int(place[day].iloc[0][1:-1].split(',')[hour])
    
    #randomize a 20%
    seed = round(datetime.now().minute)
    random.seed(seed)
    perc = random.randrange(-20,20)/100

    ans = current_pop + (current_pop * perc)

    if ans > 100:
        ans = 100.0
    elif ans < 0:
        ans = 0.0

    return ans