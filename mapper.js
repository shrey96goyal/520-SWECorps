var map = L.map('map').setView([51.505, -0.09], 13);

L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 19,
    attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
}).addTo(map);

var latlngs = [
    [40.7589, -73.9851],  
    [40.7598, -73.9816],
    [40.7624, -73.9793],
    [40.7659, -73.9779],
    [40.7694, -73.9768],
    [40.7728, -73.9749],
    [40.7761, -73.9723],
    [40.7788, -73.9693],
    [40.7829, -73.9654]   
];
var polyline = L.polyline(latlngs, {color: 'red'}).addTo(map);
map.fitBounds(polyline.getBounds());
L.marker(latlngs[0]).addTo(map).bindPopup('Input Location Name')
.openPopup();
L.marker(latlngs[latlngs.length-1]).addTo(map).bindPopup('Output Location Name')
.openPopup();

function elevation (ele) {
    let start = $("#start").val();
    let end = $("#end").val();
    let distance_per = $("#idstance").val();
    $.get(`/dummy?eleType=${ele}`,
    {
      start: start,
      end: end,
      distance_per: distance_per
    },
    function(data, status){
      alert("Data: " + data + "\nStatus: " + status);
    });
}