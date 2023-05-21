var map = L.map('map').setView([42.343488, -72.502818], 15);

L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 19,
    attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
}).addTo(map);

var topleft = null; 
var topRight = null; 
var bottomLeft = null; 
var bottomRight = null; 

var location1 = null;
var location2 = null;
var marker1 = null;
var marker2 = null;

var start_lat_lng = null;
var end_lat_lng = null;

var start_input = document.querySelector('#start');
var end_input = document.querySelector('#end');


async function calcBoundingBox(bbox){
 if (location1 == null || location2 == null){
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

var start_loc = L.Control.geocoder({
  defaultMarkGeocode: false,
  geocoder: L.Control.Geocoder.google({apiKey: 'AIzaSyCLWLZWWVKz107DGJoCh64jj0zs8gU9YnU'}),
  geocoder_autocomplete: true,
}).on('markgeocode', async function (x) {
  var lat_long = x.geocode.center;
  var loc_name = x.geocode.name;
  start_input.value = loc_name;
  
  var bbox = x.geocode.bbox;
  location1 = bbox;
  start_lat_lng = lat_long;
  var poly = await calcBoundingBox(bbox);
  map.fitBounds(poly.getBounds());
  if (marker1 != null)
    {
      map.removeLayer(marker1);
    }
  marker1 = new L.marker(lat_long);
  // map.addLayer(marker1);
  marker1.addTo(map);
}).addTo(map);

var end_loc = L.Control.geocoder({
  defaultMarkGeocode: false,
  geocoder: L.Control.Geocoder.google({apiKey: 'AIzaSyCLWLZWWVKz107DGJoCh64jj0zs8gU9YnU'}),
  geocoder_autocomplete: true,
}).on('markgeocode', async function (x) {
  var lat_long = x.geocode.center;
  var loc_name = x.geocode.name;
  end_input.value = loc_name;

  var bbox = x.geocode.bbox;
  location2 = bbox;
  end_lat_lng = lat_long;
  var poly = await calcBoundingBox(bbox);
  map.fitBounds(poly.getBounds());
  if (marker2 != null)
    {
      map.removeLayer(marker2);
    }
  marker2 = new L.marker(lat_long);
  // map.addLayer(marker2);
  marker2.addTo(map);
}).addTo(map);


const elevation = async () => {

    let elevationValue = 0;
    let elevationElement = document.querySelector("input[name='eleType']:checked");
    if (elevationElement != null){
      elevationValue = elevationElement.value;
    } 

    let distancePer = document.querySelector("#distance").value;
    if (distancePer == ''){
      distancePer = 0;
    }

    // console.log(elevationValue, distancePer, start_lat_lng, end_lat_lng);
    requestURL = 'http://127.0.0.1:5000/path?elevation='+elevationValue+'&distance='+distancePer+'&src_lat='+start_lat_lng.lat+'&src_lang='+start_lat_lng.lng;
    requestURL += '&dest_lat='+end_lat_lng.lat+'&dest_lang='+end_lat_lng.lng;

    // console.log(requestURL);
    // const response = await fetch(requestURL);
    // const myJson = await response.json(); 
    const myJson = {"route" : [[42.3434424, -72.5042974, 2, 62.753], [42.3439034, -72.5042604, 2, 61.651], [42.3440327, -72.5042531, 2, 61.783]]};

    routePoints = [];
    var routing = L.Routing.control({
      waypoints:routePoints,
      draggableWaypoints: false,
      routeWhileDragging: false,
      show: false,
      lineOptions: {
        addWaypoints: false,
        styles: [{ color: '#242c81', weight: 2 }]
      }
    }).addTo(map);
    
    for (let x of myJson["route"]) {
      console.log("sjsnj");
      console.log(x);
      point = L.latLng(x[0], x[1]);
      // console.log(point);
      routePoints.push(point);
    }
    // console.log("Route points");
    // console.log(routePoints);
    var routing = L.Routing.control({
      waypoints:routePoints,
      draggableWaypoints: false,
      routeWhileDragging: false,
      show: false,
      lineOptions: {
        addWaypoints: false,
        styles: [{ color: '#242c81', weight: 2 }]
      }
    }).addTo(map);
}
