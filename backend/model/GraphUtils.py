import osmnx as ox
import networkx as nx
from model.LocationDetails import convertLocToStr
import os

G = ox.graph_from_place('Sutherland Shire Council', network_type='walk')

'''
Return the Node ID for input point from osmx
'''
def getNodeIDForPoint(G, latitude, longitude):
    nodeID = ox.distance.nearest_nodes(G, longitude, latitude)
    return nodeID

'''
Load and save the graph for location
'''
def getGraphForLocation(location):
    assert type(location) is dict
    if not 'city' in location or location['city'] == '':
        return None

    apiKey = 'AIzaSyCLWLZWWVKz107DGJoCh64jj0zs8gU9YnU'
    if os.path.isfile(location['city'] + '.graphml'):
        print('Loading local file')
        G = ox.load_graphml(location['city'] + '.graphml')
    else:
        locationString = convertLocToStr(location)
        G = ox.graph_from_place(locationString, network_type='drive', simplify=True)
        # Load Elevation Data
        G = ox.elevation.add_node_elevations_google(G, api_key=apiKey)
        G = ox.elevation.add_edge_grades(G)

        # Save
        ox.save_graphml(G, location['city'] + ".graphml")

    return G

'''
Return the nearest node from osmnx for given longitude, latitude
'''
def getNearestNodes(Graph, longitude, latitude):
    return ox.nearest_nodes(Graph, longitude, latitude)

'''
Return shortest route from osmnx given two points
'''
def getShortestRoute(Graph, source, target):
    return ox.distance.shortest_path(Graph, source, target)

'''
Return the distance/edge length between two points
'''
def getEdgeLength(Graph, source, target):
    return Graph.get_edge_data(source, target)[0]['length']

'''
Return 0 if elevation is less than 0, otherwise return elevation
'''
def getEdgeAbsElevation(Graph, source, target):
    elevation = Graph.get_edge_data(source, target)[0]['grade']
    if elevation < 0:
        return 0
    return elevation

'''
Return the total distance of the route
'''
def getRouteDistance(Graph, route):
    numNodes = len(route)
    totalDistance = 0
    for i in range(0, numNodes-1):
        totalDistance += getEdgeLength(Graph, route[i], route[i+1])
    return totalDistance

'''
Returns the total elevation for the route
'''
def getRouteElevation(Graph, route):
    numNodes = len(route)
    totalElev = 0
    for i in range(0, numNodes - 1):
        totalElev += getEdgeAbsElevation(Graph, route[i], route[i + 1])
    return totalElev

'''
Returns array of latitude, longitude for nodes along the route
'''
def getLatLongForRoute(Graph, route):
    latLongArray = []
    for node in route:
        nodeData = Graph.nodes(data = True)[node]
        latLongArray.append([nodeData['y'], nodeData['x']])

    return latLongArray