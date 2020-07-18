import googlemaps

def get_photo(place_id, key, height=400, width=400, sensor = 'false'):
    """This function retun a picture from a given id

    Args:
        place_id ([string]): [The place ID]
        key ([string]): [API_KEY]
        height (int, optional): [max Height]. Defaults to 400.
        width (int, optional): [min Height]. Defaults to 400.
        sensor (str, optional): [description]. Defaults to 'false'..TODO

    Returns:
        [string]: [picture URL]
    """    

    ID = place_id
    API_KEY = key
    HIGHT = height
    WIDTH =  width
    SENSOR = sensor

    #get reference number from id
    #enter api
    gmaps = googlemaps.Client(key = API_KEY)
    #get photos details
    places_details  = gmaps.place(place_id= ID, fields=['photo'])
    #retrieve reference
    REFERENCE = places_details['result']['photos'][0]['photo_reference']

    URL = 'https://maps.googleapis.com/maps/api/place/photo?photoreference={}&sensor={}&maxheight={}&maxwidth={}&key={}'
    
    url_final = URL.format(
        REFERENCE,
        SENSOR,
        HIGHT,
        WIDTH,     
        API_KEY
    )
    return url_final