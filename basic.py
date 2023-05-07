import osmnx as ox
G = ox.graph_from_place('Sutherland Shire Council', network_type='drive')
# ox.plot_graph(G)

from geopy.geocoders import Nominatim

def getNodeIDForPoint(G, latitude, longitude):
    nodeID = ox.distance.nearest_nodes(G, longitude, latitude)
    return nodeID

def convertLocToStr(location):
    locationArray = []
    if location['city'] != '':
        locationArray.append(location['city'])

    if location['state'] != '':
        locationArray.append(location['state'])

    if location['country'] != '':
        locationArray.append(location['country'])

    return ', '.join(locationArray)

# Latitude, Longitude
def getCommonLocation(src_point, dest_point):
    geolocator = Nominatim(user_agent="basicApp3")
    location_src = geolocator.reverse(str(src_point[0]) + ", " + str(src_point[1]))
    location_dest = geolocator.reverse(str(dest_point[0]) + ", " + str(dest_point[1]))

    source = location_src.raw['address']
    dest = location_dest.raw['address']

    srcCountry = source.get('country','')
    srcState = source.get('state', '')
    srcCity = source.get('city', '')
    if srcCity == '':
        srcCity = source.get('town', '')

    destCountry = dest.get('country', '')
    destState = dest.get('state', '')
    destCity = dest.get('city', '')
    if destCity == '':
        destCity = dest.get('town', '')

    commonLocation = {'country':'', 'state':'', 'city':''}

    if srcCountry != destCountry:
        return commonLocation
    commonLocation['country'] = srcCountry

    if srcState != destState:
        return commonLocation
    commonLocation['state'] = srcState

    if srcCity != destCity:
        return commonLocation
    commonLocation['city'] = srcCity

    return commonLocation

def getGraphForLocation(location):
    assert type(location) is dict
    if not 'city' in location or location['city'] == '':
        return None
    locationString = convertLocToStr(location)
    G = ox.graph_from_place(locationString, network_type='drive', simplify=False)

    G1 = ox.add_node_elevations_google(G, '', url_template='https://api.open-elevation.com/api/v1/lookup?locations={}&key={}')
    return G

# get_details((19, 73), (19, 73))
from flask import Flask, request

app = Flask(__name__)


@app.route("/")
def home():
    return "Hello, World!"

@app.route("/salvador")
def salvador():
    # http://127.0.0.1:5000/salvador?name=abc
    print(request.args.get("name"))

    return {1:"Hello, Salvador"}

if __name__ == "__main__":
    l = getCommonLocation([42.343488, -72.502818], [42.377260, -72.519954])
    print(l)
    print(convertLocToStr(l))
    G = getGraphForLocation(l)
    print('hi')
    # app.run(debug=True, port=5000)
    # 66597275
    # 3602737605

# https://www.technewstoday.com/install-and-use-make-in-windows/