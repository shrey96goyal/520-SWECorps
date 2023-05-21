import osmnx as ox
import networkx as nx
from model.LocationDetails import convertLocToStr
import os

G = ox.graph_from_place('Sutherland Shire Council', network_type='walk')

def getNodeIDForPoint(G, latitude, longitude):
    nodeID = ox.distance.nearest_nodes(G, longitude, latitude)
    return nodeID

def getGraphForLocation(location):
    assert type(location) is dict
    if not 'city' in location or location['city'] == '':
        return None

    apiKey = 'AIzaSyCLWLZWWVKz107DGJoCh64jj0zs8gU9YnU'
    if os.path.isfile(location['city'] + '.graphml'):
        print('Loading local file')
        G = ox.load_graphml(location['city'] + '.graphml')
    # x = ox.load_graphml('a.graphml')
    else:
        locationString = convertLocToStr(location)
        G = ox.graph_from_place(locationString, network_type='drive', simplify=False)
        # Load Elevation Data
        G = ox.elevation.add_node_elevations_google(G, api_key=apiKey)
        G = ox.elevation.add_edge_grades(G)

        # Save
        ox.save_graphml(G, location['city'] + ".graphml")


    # print("Here")
    # G1 = ox.add_node_elevations_google(G, '', url_template='https://api.open-elevation.com/api/v1/lookup?locations={}&key={}')
    return G

def getNearestNodes(Graph, longitude, latitude):
    return ox.nearest_nodes(Graph, longitude, latitude)

def getShortestRoute(Graph, source, target):
    route = nx.shortest_path(Graph, source, target, method='dijkstra')
    print(len(route))
    print(nx.shortest_path_length(Graph, source, target, method='dijkstra'))
    return route

def getEdgeLength(Graph, source, target):
    return Graph.get_edge_data(source, target)[0]['length']
def getEdgeAbsElevation(Graph, source, target):
    return Graph.get_edge_data(source, target)[0]['grade_abs']

def getRouteDistance(Graph, route):
    numNodes = len(route)
    totalDistance = 0
    for i in range(0, numNodes-1):
        totalDistance += getEdgeLength(Graph, route[i], route[i+1])
    return totalDistance

def getRouteElevation(Graph, route):
    numNodes = len(route)
    totalElev = 0
    for i in range(0, numNodes - 1):
        totalElev += getEdgeAbsElevation(Graph, route[i], route[i + 1])
    return totalElev

def getLatLongForRoute(Graph, route):
    latLongArray = []
    for node in route:
        nodeData = Graph.nodes(data = True)[node]
        latLongArray.append([nodeData['y'], nodeData['x']])

    return latLongArray

# def getAllPaths(Graph, distance_limit, source, target):
