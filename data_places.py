import pandas as pd
import populartimes
import json
import urllib.request as url_req
import time
import geopandas as gpd
import geopy
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter
from tqdm import tqdm
from datetime import datetime
import random

class PlacesMoments():
    """This class uses Places API in order to get some places data
    """    
    def __init__(self, API_KEY):
        """Init method of the class

        Arguments:
            API_KEY {string} -- [your API key]
        """
        self.api = API_KEY
    
    
    
    def read_places(self, center_lat, center_lng, radius, places_types):
        """this function search for places in an expesific area

        Args:
            center_lat ([float]): [latitud]
            center_lng ([float]): [longitud]
            radius ([int]): [the radius of the area]
            places_types ([list of tuples]): [list of places types and pages to be scanned.For admited places refer to https://developers.google.com/places/supported_types]. ex ('store', 2)

        Returns:
            [DataFrame]: [Data Frame with places Data]
        """        
    
        CENTER = (center_lat, center_lng)
        RADIUS = radius
        API_NEARBY_SEARCH_URL = 'https://maps.googleapis.com/maps/api/place/nearbysearch/json'   
        PLACES_TYPES = places_types

        def request_api(url):
            response = url_req.urlopen(url)
            json_raw = response.read()
            json_data = json.loads(json_raw)
            return json_data

        def get_places(types, pages):
            location = str(CENTER[0]) + "," + str(CENTER[1])
            mounted_url = ('%s'
                '?location=%s'
                '&radius=%s'
                '&type=%s'
                '&key=%s') % (API_NEARBY_SEARCH_URL, location, RADIUS, types, self.api)
            
            results = []
            next_page_token = None

            if pages == None: pages = 1

            for num_page in range(pages):
                if num_page == 0:
                    api_response = request_api(mounted_url)
                    results = results + api_response['results']
                else:
                    page_url = ('%s'
                        '?key=%s'
                        '&pagetoken=%s') % (API_NEARBY_SEARCH_URL, self.api, next_page_token)
                    api_response = request_api(str(page_url))
                    results += api_response['results']

                if 'next_page_token' in api_response:
                    next_page_token = api_response['next_page_token']
                else: break
                
                time.sleep(1)
            return results

        def parse_place_to_list(place, type_name):
            # Using name, place_id, lat, lng, rating, type_name
            return [
                place['name'],
                place['place_id'],
                place['geometry']['location']['lat'],
                place['geometry']['location']['lng'],
                type_name       
            ]

        def mount_dataset():
            data = []

            for place_type in PLACES_TYPES:
                type_name = place_type[0]
                type_pages = place_type[1]

                print("Getting into " + type_name)

                result = get_places(type_name, type_pages)
                result_parsed = list(map(lambda x: parse_place_to_list(x, type_name), result))
                data += result_parsed

            dataframe = pd.DataFrame(data, columns=['place_name', 'place_id', 'lat', 'lng', 'type'])
            dataframe.to_csv('data/places.csv')
            return dataframe

        return mount_dataset()

    
    
    def get_places_popular_moments(self, df):
        
        """This function get popular moments from places id.

        Args:
            df ([DataFrame]): DataFrame. One column must be 'places_id'
        """    

        places = df
        places['monday'] = None
        places['tuesday'] = None
        places['wednesday'] = None
        places['thursday'] = None
        places['friday'] = None
        places['saturday'] = None
        places['sunday'] = None

        def get_place_popular_moments(place_id):
            popular_moments = populartimes.get_id(self.api, place_id)
            if 'populartimes' in popular_moments:
                return popular_moments['populartimes']
            else:
                return None

        for (index, row) in places.iterrows():
            print("Populating " + str(index))
            try:
                moments = get_place_popular_moments(row.place_id)
                if moments != None:
                    places.at[index, 'monday'] = moments[0]['data']
                    places.at[index, 'tuesday'] = moments[1]['data']
                    places.at[index, 'wednesday'] = moments[2]['data']
                    places.at[index, 'thursday'] = moments[3]['data']
                    places.at[index, 'friday'] = moments[4]['data']
                    places.at[index, 'saturday'] = moments[5]['data']
                    places.at[index, 'sunday'] = moments[6]['data']
            except:
                continue
        
        places.to_csv('data/places_with_moments.csv')
        return places


    def get_address(self, df):
        '''This function search for places addres given their coordenates

        Args:
            df ([DataFrame]): DataFrame. One column must be 'lat' and other 'lng'
        return:
            ([DataFrame]): The same as input with address added
        '''
        #formating geometry
        places = df
        places["geom"] = places["lat"].map(str) + "," + places["lng"].map(str)

        #Reverse Geocoding
        locator = Nominatim(user_agent="Openstreetmap", timeout=10)
        rgeocode = RateLimiter(locator.reverse, min_delay_seconds=0.001)

        tqdm.pandas()
        places["address"] = places["geom"].progress_apply(rgeocode)
        places.to_csv('data/places_with_all.csv')
        return places