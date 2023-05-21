from flask import Flask, request, jsonify
from flask_cors import CORS
from model.GraphUtils import getRouteDistance, getLatLongForRoute, getRouteElevation
from model.graph.Graph import Graph

app = Flask(__name__)

@app.route("/path", methods=['GET'])
def path():
    # Parse Input request
    args = request.args

    # Source Lat, Source, Long, Dest lat, Dest long
    # graph = Graph(42.343488, -72.502818, 42.377260, -72.519954)
    graph = Graph(args)
    if graph.graph is None:
        return jsonify({'message':"Please give locations within the same city"}), 400

    # Path type, x%
    path = graph.getPath()
    if path is None:
        return jsonify({'message':"No path found"}), 400

    routeDistance = round(getRouteDistance(graph.graph, path))
    latLongRoute = getLatLongForRoute(graph.graph, path)
    routeElevation = round(getRouteElevation(graph.graph, path))

    # Sample plot
    # routes = [shortest_route, elevationPath]
    # routeColors = ['r', 'y']
    # fig, ax = ox.plot_graph_routes(G, routes, route_colors=routeColors, route_linewidth=6, node_size=0)

    return jsonify({'route': latLongRoute,
                    'distance': routeDistance,
                    'elevation': routeElevation})

if __name__ == "__main__":
    CORS(app)
    app.run()
