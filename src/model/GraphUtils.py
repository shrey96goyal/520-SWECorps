import osmnx as ox
import networkx as nx
from model.LocationDetails import convertLocToStr

G = ox.graph_from_place('Sutherland Shire Council', network_type='walk')

def getNodeIDForPoint(G, latitude, longitude):
    nodeID = ox.distance.nearest_nodes(G, longitude, latitude)
    return nodeID

def getGraphForLocation(location):
    assert type(location) is dict
    if not 'city' in location or location['city'] == '':
        return None
    locationString = convertLocToStr(location)
    G = ox.graph_from_place(locationString, network_type='walk', simplify=False)
    # print("Here")
    ox.save_graphml(G, "Amherst.graphml")
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

def getRouteDistance(Graph, route):
    numNodes = len(route)
    totalDistance = 0
    for i in range(0, numNodes-1):
        totalDistance += getEdgeLength(Graph, route[i], route[i+1])
    return totalDistance

# def getAllPaths(Graph, distance_limit, source, target):
