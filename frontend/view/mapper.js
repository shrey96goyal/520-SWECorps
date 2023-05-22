console.log("Retrieving map");
// Create a map 
var map = L.map('map').setView([42.343488, -72.502818], 15);

L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 19,
    attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
}).addTo(map);

// Initialize for logic to zoom in/out depending on markers on the map
var topleft = null; 
var topRight = null; 
var bottomLeft = null; 
var bottomRight = null; 

var location1 = null;
var location2 = null;
var marker1 = null;
var marker2 = null;

// Maintain lattude, longitude of source and target
var start_lat_lng = null;
var end_lat_lng = null;
var route = null;

// Getting the text areas for source and target, result label
var start_input = document.querySelector('#start');
var end_input = document.querySelector('#end');
var result = document.getElementById('result');

// Logic to zoom in/out depending on 1 marker or two markers on the map
async function calcBoundingBox(bbox){
 if (location1 == null || location2 == null){
  console.log("Calculating bounding box for setting focus on the map when one of the locations is not set");
    var poly = L.polygon([
      bbox.getSouthEast(),
      bbox.getNorthEast(),
      bbox.getNorthWest(),
      bbox.getSouthWest()
    ]);
    topleft = bbox.getNorthWest();
    topRight = bbox.getNorthEast();
    bottomLeft = bbox.getSouthWest();
    bottomRight = bbox.getSouthEast(); 
 }
 else{
  console.log("Calculating bounding box for setting focus on the map when both the locations are set");
    topleft = location1.getNorthWest();
    topRight = location1.getNorthEast();
    bottomLeft = location1.getSouthWest();
    bottomRight = location1.getSouthEast(); 

    topleft = L.latLng(Math.max(topleft.lat, location2.getNorthWest().lat), Math.min(topleft.lng, location2.getNorthWest().lng));
    topRight = L.latLng(Math.max(topRight.lat, location2.getNorthEast().lat), Math.max(topRight.lng, location2.getNorthEast().lng));
    bottomLeft = L.latLng(Math.min(bottomLeft.lat, location2.getSouthWest().lat), Math.min(bottomLeft.lng, location2.getSouthWest().lng));
    bottomRight = L.latLng(Math.min(bottomRight.lat, location2.getSouthEast().lat), Math.max(bottomRight.lng, location2.getSouthEast().lng));
    var poly = L.polygon([bottomRight,topRight,topleft,bottomLeft]);
 }
 return poly;
}

// Logic for adding source location, adding marker for source location, zoom in/out
var start_loc = L.Control.geocoder({
  defaultMarkGeocode: false,
  geocoder: L.Control.Geocoder.google({apiKey: 'AIzaSyCLWLZWWVKz107DGJoCh64jj0zs8gU9YnU'}),
  geocoder_autocomplete: true,
}).on('markgeocode', async function (x) {
  var lat_long = x.geocode.center;
  var loc_name = x.geocode.name;
  start_input.value = loc_name;
  
  console.log("Clear existing route on the map!");
  if (route != null){
    map.removeLayer(route);
  }

  var bbox = x.geocode.bbox;
  location1 = bbox;
  start_lat_lng = lat_long;
  var poly = await calcBoundingBox(bbox);
  map.fitBounds(poly.getBounds());

  console.log("Reset the marker to new source location");
  if (marker1 != null)
    {
      map.removeLayer(marker1);
    }
  marker1 = new L.marker(lat_long);
  marker1.addTo(map);
}).addTo(map);

// Logic for adding destination location, adding marker for destination location, zoom in/out
var end_loc = L.Control.geocoder({
  defaultMarkGeocode: false,
  geocoder: L.Control.Geocoder.google({apiKey: 'AIzaSyCLWLZWWVKz107DGJoCh64jj0zs8gU9YnU'}),
  geocoder_autocomplete: true,
}).on('markgeocode', async function (x) {
  var lat_long = x.geocode.center;
  var loc_name = x.geocode.name;
  end_input.value = loc_name;

  console.log("Clear existing route on the map!");
  if (route != null){
    map.removeLayer(route);
  }
  
  var bbox = x.geocode.bbox;
  location2 = bbox;
  end_lat_lng = lat_long;
  var poly = await calcBoundingBox(bbox);
  map.fitBounds(poly.getBounds());

  console.log("Reset the marker to new target location");
  if (marker2 != null)
    {
      map.removeLayer(marker2);
    }
  marker2 = new L.marker(lat_long);
  marker2.addTo(map);
}).addTo(map);

// Input validation for distance percentage textbox
function isNumberKey(evt) {
  var charCode = (evt.which) ? evt.which : evt.keyCode
  if (charCode > 31 && (charCode < 48 || charCode > 57)){
    console.log("Invalid character entered");
    return false;
  }
  return true;
}

// Calling backend API, displaying route
const elevation = async () => {

  // Get selected elevation, Default no elevation
    let elevationValue = document.querySelector("input[name='eleType']:checked").value;

  // Get input distance percentage, default 0
    let distancePer = document.querySelector("#distance").value;
    if (distancePer == ''){
      distancePer = 0;
    }

  // If input latitude, longitude is not entered, raise error and return
    if (start_lat_lng == null || end_lat_lng == null){
      result.innerHTML = "Source or destination not entered!";
      return;
    }

    console.log("Request parameters -> Elevation, Distance Percentage, Source, Destination")
    console.log(elevationValue, distancePer, start_lat_lng, end_lat_lng);
    requestURL = 'http://127.0.0.1:5000/path?elevation='+elevationValue+'&distance='+distancePer+'&src_lat='+start_lat_lng.lat+'&src_lang='+start_lat_lng.lng;
    requestURL += '&dest_lat='+end_lat_lng.lat+'&dest_lang='+end_lat_lng.lng;

    console.log(requestURL);
    result.innerHTML = "Request sent, waiting for response!";
  
  // Call backend API
    const response = await fetch(requestURL);

  // If API returns 500 response
    if (response.status == 500){
      result.innerHTML = "Bad request, server could not return response!";
      return;
    }

    const responseJSON = await response.json(); 
    // responseJSON = {"route" : [[42.3434424, -72.5042974, 2, 62.753], [42.3439034, -72.5042604, 2, 61.651], [42.3440327, -72.5042531, 2, 61.783]], distance:100, elevation:200};

  // If API returns 400 error
    if (responseJSON.hasOwnProperty("message")) {
      result.innerHTML = responseJSON.message;
      return;
    }

  // If API returns route successfully, show the route on map
    routePoints = [];
    if (route != null){
      result.innerHTML = "";
      map.removeLayer(route);
    }
    
    for (let x of responseJSON["route"]) {
      point = [x[0], x[1]];
      routePoints.push(point);
    }

    console.log("Length of route in response -> ")
    console.log(routePoints.length);
    route = L.polyline(routePoints, {color: 'blue'});
    route.addTo(map);
    map.fitBounds(route.getBounds());

  // Show result distance and elevation
    result.innerHTML = "Calculated Distance : "+responseJSON["distance"]+"<br/>Calculated elevation : "+responseJSON["elevation"];  
}
