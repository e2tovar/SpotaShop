import googlemaps

def get_ratings(place_id, api_key):
    
    API_KEY = api_key

    gmaps = googlemaps.Client(key = API_KEY)
    
    my_fields = ['rating', 'user_ratings_total', 'opening_hours']
    
    place_details = gmaps.place(place_id = place_id, fields = my_fields)

    rating = place_details['result']['rating']
    total_rating = place_details['result']['user_ratings_total']

    return rating, total_rating

