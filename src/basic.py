import osmnx as ox
from flask import Flask, request
from model.LocationDetails import getCommonLocation, convertLocToStr
from model.GraphUtils import getGraphForLocation, getNearestNodes, getRouteDistance, getShortestRoute

app = Flask(__name__)

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
    shortest_route = getShortestRoute(G, orig_node, dest_node)
    shortest_path_length = getRouteDistance(G, shortest_route)
    # print(shortest_path_length)
    return "Hello, World!"

@app.route("/salvador")
def salvador():
    # http://127.0.0.1:5000/salvador?name=abc
    print(request.args.get("name"))

    return {1:"Hello, Salvador"}

if __name__ == "__main__":
    app.run()
    # 66597275
    # 3602737605

# https://www.technewstoday.com/install-and-use-make-in-windows/