var map = L.map('map').setView([51.505, -0.09], 13);

L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 19,
    attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
}).addTo(map);


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
