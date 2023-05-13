import osmnx as ox
from flask import Flask, request
from model.LocationDetails import getCommonLocation, convertLocToStr
from model.GraphUtils import getGraphForLocation, getNearestNodes, getRouteDistance, getShortestRoute, getEdgeLength, getEdgeAbsElevation

app = Flask(__name__)

import heapq
from geopy import distance
def aStarSearch(G, origNode, destNode, shortestDistance, distRestriction, minElevation = 1):

    maxDistance = shortestDistance * (1 + distRestriction)
    print('shortest distance is ' + str(shortestDistance))
    print('max distance is ' + str(maxDistance))
    s = {}
    openList = [(0, origNode, [origNode], 0, 0)]
    possiblePaths = []
    destNodeData = G.nodes(data=True)[destNode]
    while len(openList) > 0 and openList[0][3] <= maxDistance:
        f, node, path, g, dist = openList[0]
        print(str(len(openList)) + 'hi')
        openList.pop(0)
        nodeData = G.nodes(data=True)[node]
        if node == destNode:
            print('adding')
            # path.append(node)
            possiblePaths = path
            print(dist)
            if dist <= maxDistance:
                break
        else:
            s[node] = (g, dist)
            for edges in G.out_edges(node):
                nextNode = edges[1]
                if nextNode in path:
                    continue
                nextG = g + getEdgeAbsElevation(G, node, nextNode)*minElevation
                nextDist = dist + getEdgeLength(G, node, nextNode)
                if nextDist > maxDistance:
                    continue
                if nextNode not in s or s[nextNode][0] > nextG or s[nextNode][1] > nextDist:
                    nextNodeData = G.nodes(data=True)[nextNode]
                    nextNodePath = path.copy()
                    nextF = nextG
                    if nextNode != destNode:
                        nextF += minElevation*(abs(destNodeData['elevation'] - nextNodeData['elevation'])/(distance.distance((nextNodeData['y'], nextNodeData['x']), (destNodeData['y'], destNodeData['x'])).km * 1000))
                    nextNodePath.append(nextNode)
                    openList.append((nextF, nextNode, nextNodePath, nextG, nextDist))

        heapq.heapify(openList)

    print(len(possiblePaths))


@app.route("/")
def home():
    source = [42.343488, -72.502818]
    destination = [42.377260, -72.519954]
    l = getCommonLocation(source, destination)
    G = getGraphForLocation(l)
    orig_node = getNearestNodes(G, source[1], source[0]) # Longitude, Latitude
    dest_node = getNearestNodes(G, destination[1], destination[0])
    # print(orig_node)
    # print(dest_node)
    for edges in G.out_edges(orig_node):
        n1 = edges[1]



    shortest_route = getShortestRoute(G, orig_node, dest_node)
    shortest_path_length = getRouteDistance(G, shortest_route)
    aStarSearch(G, orig_node, dest_node, shortest_path_length, 0.3, -1)
    # print(shortest_path_length)
    #7184243985
    return "Hello, World!"


if __name__ == "__main__":
    app.run()
    # 66597275
    # 3602737605

# https://www.technewstoday.com/install-and-use-make-in-windows/