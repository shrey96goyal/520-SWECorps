var map = L.map('map').setView([51.505, -0.09], 13);

L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 19,
    attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
}).addTo(map);

var start_input = document.querySelector('#start');
var end_input = document.querySelector('#end');

var start_loc = L.Control.geocoder({
  defaultMarkGeocode: false,
  geocoder: L.Control.Geocoder.nominatim({
    geocodingQueryParams: { limit: 5 },
  }),
  geocoder_autocomplete: true,
}).on('markgeocode', function (x) {
  var lat_long = x.geocode.center;
  var loc_name = x.geocode.name;
  start_input.value = loc_name;
}).addTo(map);

var end_loc = L.Control.geocoder({
  defaultMarkGeocode: false,
  geocoder: L.Control.Geocoder.nominatim({
    geocodingQueryParams: { limit: 5 },
  }),
  geocoder_autocomplete: true,
}).on('markgeocode', function (x) {
  var lat_long = x.geocode.center;
  var loc_name = x.geocode.name;
  end_input.value = loc_name;
}).addTo(map);

start_input.addEventListener('focus', function () {
  start_loc.addTo(map);
});


end_input.addEventListener('focus', function () {
  end_loc.addTo(map);
});

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
    $.get(`/dummy?eleType=${selectedEle}`,
    {
      start: start,
      end: end,
      distance_per: distance_per
    },
    function(data, status){
      alert("Data: " + data + "\nStatus: " + status);
    });
}
