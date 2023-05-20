var map = L.map('map').setView([42.343488, -72.502818], 15);

L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 19,
    attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
}).addTo(map);

var topleft = null; 
var topRight = null; 
var bottomLeft = null; 
var bottomRight = null; 
var isBBoxSet = false;

var markersQueue = [];
// queue.push(2);         // queue is now [2]
// queue.push(5);         // queue is now [2, 5]
// var i = queue.shift(); // queue is now [5]

// async function calcBoundingBox(bbox){
//  if (!isBBoxSet){
//   console.log("Inside If");
//     var poly = L.polygon([
//       bbox.getSouthEast(),
//       bbox.getNorthEast(),
//       bbox.getNorthWest(),
//       bbox.getSouthWest()
//     ]);
//     topleft = bbox.getNorthWest();
//     topRight = bbox.getNorthEast();
//     bottomLeft = bbox.getSouthWest();
//     bottomRight = bbox.getSouthEast(); 
//     isBBoxSet = true;
//  }
//  else{
//     topleft = L.latLng(Math.min(topleft.lat, bbox.getNorthWest().lat), Math.max(topleft.lng, bbox.getNorthWest().lng));
//     topRight = L.latLng(Math.max(topRight.lat, bbox.getNorthEast().lat), Math.max(topRight.lng, bbox.getNorthEast().lng));
//     bottomLeft = L.latLng(Math.min(bottomLeft.lat, bbox.getSouthWest().lat), Math.min(bottomLeft.lng, bbox.getSouthWest().lng));
//     bottomRight = L.latLng(Math.max(bottomRight.lat, bbox.getSouthEast().lat), Math.min(bottomRight.lng, bbox.getSouthEast().lng));
//     var poly = L.polygon([bottomRight,topRight,topleft,bottomLeft]);
//     console.log("hhhh");
//  }
//  return poly;
// }
var markerArray = [];

async function calcBoundingBox(){
  console.log("hihi");
  for (var i = 0; i < markersQueue.length; i++) {
    console.log("cd");
    marker = new L.marker([markersQueue[i].lat, markersQueue[i].lng]);
    markerArray.push(marker);
  }
  console.log(markerArray.length);

  // var group = new L.featureGroup(markerArray);
  // map.fitBounds(group.getBounds());

  let latlngs = markerArray.map(marker => marker.getLatLng())
  let latlngBounds = L.latLngBounds(latlngs)
  map.fitBounds(latlngBounds);
  // console.log("dsjdns");
}

var start_input = document.querySelector('#start');
var end_input = document.querySelector('#end');

var start_loc = L.Control.geocoder({
  defaultMarkGeocode: true,
  geocoder: L.Control.Geocoder.nominatim({
    geocodingQueryParams: { limit: 5 },
  }),
  geocoder_autocomplete: true,
}).on('markgeocode', async function (x) {
  var lat_long = x.geocode.center;
  var loc_name = x.geocode.name;
  start_input.value = loc_name;
  markersQueue.push(lat_long);
  // var bbox = x.geocode.bbox;
  // var poly = await calcBoundingBox(bbox);
  // map.fitBounds(poly.getBounds());
  // await calcBoundingBox();
  // console.log("Length");
  // console.log(markersQueue);
}).addTo(map);

var end_loc = L.Control.geocoder({
  defaultMarkGeocode: true,
  geocoder: L.Control.Geocoder.nominatim({
    geocodingQueryParams: { limit: 5 },
  }),
  geocoder_autocomplete: true,
}).on('markgeocode', async function (x) {
  var lat_long = x.geocode.center;
  var loc_name = x.geocode.name;
  end_input.value = loc_name;
  markersQueue.push(lat_long);
  // await calcBoundingBox();
  // var bbox = x.geocode.bbox;
  // var poly = await calcBoundingBox();
  // map.fitBounds(poly.getBounds());
  // console.log("Length");
  // console.log(markersQueue);
}).addTo(map);

// start_input.addEventListener('focus', function () {
//   start_loc.addTo(map);
// });


// end_input.addEventListener('focus', function () {
//   end_loc.addTo(map);
// });

/*
start_input.addEventListener('blur', function () {
  start_container.classList.remove('active');
  start_container.removeChild(start_loc.getContainer());
});

end_input.addEventListener('blur', function () {
  end_container.classList.remove('active');
  end_container.removeChild(end_loc.getContainer());
});
*/



function elevation () {
    let selectedEle = $("input[name='eleType']:checked").val();
    let start = $("#start").val();
    let end = $("#end").val();
    let distance_per = $("#distance").val();
    console.log('hi');

    const xhr = new XMLHttpRequest();
    xhr.open('GET', 'http://127.0.0.1:5000/');
    xhr.onload = function() {
      if (xhr.status === 200) {
        const data = JSON.parse(xhr.responseText);
        console.log(data);
      } else {
        console.error(`Error: ${xhr.status}`);
      }
    };
    xhr.onerror = function() {
      console.error('Request error');
    };
    xhr.send();

    // $.get(`/dummy?eleType=${selectedEle}`,
    // {
    //   start: start,
    //   end: end,
    //   distance_per: distance_per
    // },
    // function(data, status){
    //   // alert("Data: " + data + "\nStatus: " + status);

    // });
}
