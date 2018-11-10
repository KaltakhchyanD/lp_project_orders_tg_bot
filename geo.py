import pprint
import os

import googlemaps
from geopy.geocoders import Nominatim, Yandex, GoogleV3, ArcGIS

google_api=os.getenv('GOOGLE_API_KEY')
gmaps = googlemaps.Client(key=google_api)


def geocode_address(addr, service = 'ArcGIS'):
    if service=='Open':
        geolocator = Nominatim(user_agent="specify_your_app_name_here")
    elif service == 'Google':
        geolocator = GoogleV3(user_agent="specify_your_app_name_here")
    elif service == 'Yandex':
        geolocator = Yandex(user_agent="specify_your_app_name_here")
    elif service == 'ArcGIS':
        geolocator = ArcGIS(user_agent="specify_your_app_name_here")
    else:
        return False

    g2 = geolocator.geocode(addr)
    return g2.raw


def reverse_geocode(coords, service = 'ArcGIS'):
    if service=='Open':
        geolocator = Nominatim(user_agent="specify_your_app_name_here")
    elif service == 'Google':
        geolocator = GoogleV3(user_agent="specify_your_app_name_here")
    elif service == 'Yandex':
        geolocator = Yandex(user_agent="specify_your_app_name_here")
    elif service == 'ArcGIS':
        geolocator = ArcGIS(user_agent="specify_your_app_name_here")
    else:
        return False

    g2 = geolocator.reverse(f'{float(coords[0])}, {float(coords[1])}')
    return g2


def get_coordinates_by_address(addr = 'Москва Ореховый проезд 39 к2', service = 'ArcGIS'):
    geocode = geocode_address(addr)
    if service=='Open':
        result = (float(geocode['lat']), float(geocode['lon']))
    elif service == 'ArcGIS':
        result = (float(geocode['location']['y']), float(geocode['location']['x']))
    # TODO - add ya and google
    #return (geocode['Point']['pos'].split()[::-1])
    return result


def get_address_by_coords(coords):
    # TODO - check other services
    reverse = reverse_geocode(coords, 'ArcGIS')
    address = reverse.raw['Address'].replace(',', '')
    return address


def check_district_is_valid(district):
    if district in ['Zyablikovo', 'Orekhovo-Borisovo Severnoye', 'Orekhovo-Borisovo Yuzhnoye', 'Зябликово', 'Орехово-Борисово Северное', 'Орехово-Борисово Южное']:
        result = True
    elif district in ['Brateyevo', 'Братеево']  and check_point_is_under_edge_of_area(coord[0],coord[1]):
        result = True
    else:
        result = False
    return result


def check_address_in_zone_full(addr):
    # TODO - add other services
    # TODO - refactor - self repeating here
    coords = get_coordinates_by_address(addr)
    reverse = reverse_geocode(coords, 'ArcGIS')
    district = reverse.raw['District'].split('МО ')[-1]
    #geocode = geocode_address(addr, 'ArcGIS')
    #coords = tuple(g2.raw['Point']['pos'].split()[::-1])
    #coords = geocode['geometry']['location']['lat'],['geometry']['location']['lng']
    #reverse = reverse_geocode(coords, 'ArcGIS')
    #district = g2[0]._address.split(',')[0].split('район ')[-1]
    #district = geocode['address_components'][4]['long_name']

    return check_district_is_valid(district)


def check_coords_in_zone_full(coords):
    reverse = reverse_geocode(coords, 'ArcGIS')
    district = reverse.raw['District'].split('МО ')[-1]
    return check_district_is_valid(district)



def check_point_is_under_edge_of_area(x2, y2, x0=55.638142, y0=37.781631, x1=55.630814, y1=37.752349):

    '''
        x0-y1 : coordinates of the edge of valid area
        (in my case only 1 edge is neaded)
        x2,y2 - point to be checked
        if its inside valid area(above the edge line) - return True
    '''

    a = (y1-y0)/(x1-x0)
    b = y0-x0*a
    # coefficient of perpendicular to the edge line
    a_new = -1/a
    b_new = x2/a+y2
    # coordinates of cross between edge and its perpendicular
    x_cross = (b_new-b)/(a-a_new)
    y_cross = a_new*x_cross+b_new

    return y2<y_cross


   








