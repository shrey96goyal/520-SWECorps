import sys
sys.path.append("..")

from flask import Flask, request, jsonify
from flask_cors import CORS
from model.GraphUtils import getRouteDistance, getLatLongForRoute, getRouteElevation
from model.graph.Graph import Graph

app = Flask(__name__)

@app.route("/path", methods=['GET'])
def path():
    print("Received request.")
    # Parse Input request
    args = request.args
    input_elevation = args.get("elevation")
    input_distance = args.get("distance")
    input_src_lat = args.get("src_lat")
    input_src_lang = args.get("src_lang")
    input_dest_lat = args.get("dest_lat")
    input_dest_lang = args.get("dest_lang")
    # Allowed evelation options, for validating input
    elevation_allowed_options = ["0", "1", "2"]

    # Perform input validation
    if (not input_src_lat or not input_src_lang or not input_dest_lat or not input_dest_lang):
        return jsonify({'message':"Source or destination can not be empty"}), 400
    
    if (input_elevation not in elevation_allowed_options):
        return jsonify({'message':"Incorrect elevation received"}), 400
    
    if (int(input_distance) < 0):
        return jsonify({'message':"Incorrect distance percentage received"}), 400
    
    # Source Lat, Source, Long, Dest lat, Dest long
    graph = Graph(args)
    if graph.graph is None:
        return jsonify({'message':"Please give locations within the same city"}), 400

    # Path type, x%
    path = graph.getPath()
    if path is None:
        return jsonify({'message':"No path found"}), 400

    # Calculate distance, latitude, longitude, elevation of the resultant route
    routeDistance, latLongRoute, routeElevation = path[0], path[1], path[2]


    return jsonify({'route': latLongRoute,
                    'distance': routeDistance,
                    'elevation': routeElevation})

if __name__ == "__main__":
    CORS(app)
    app.run()
