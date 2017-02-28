var map = L.map('map').setView([51.505, -0.09], 13);

var carbonData = {
    "Air" : 1600,
    "Van" : 200,
    "HGV" : 180,
    "Coastal" : 50
};
//horrible bodge
var producers = JSON.parse(document.getElementById("producers").innerText);
var ingredients = JSON.parse(document.getElementById("ingredients").innerText);
var locations = JSON.parse(document.getElementById("locations").innerText);
var weights = JSON.parse(document.getElementById("weights").innerText);
var icons = JSON.parse(document.getElementById("icons").innerText);

var distanceHeader = document.getElementById("distance");
var carbonHeader = document.getElementById("carbon");
L.tileLayer('http://{s}.tile.osm.org/{z}/{x}/{y}.png', {
    attribution: '&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors'
}).addTo(map);
getLocation();

function httpGet(theUrl)
{
    var xmlHttp = new XMLHttpRequest();
    xmlHttp.open( "GET", theUrl, false ); // false for synchronous request
    xmlHttp.send( null );
    console.log(xmlHttp.status)
    if (xmlHttp.readyState == 4 && xmlHttp.status == 200) {
        return 1; //image icon found
    } else {
        return 0; //image icon not found
    }
}

function getFoodIcon(index) {

    return  "http://" + icons[index];
   
}

function getLocation() {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(showPosition);
    } else {
        alert("Geolocation is not supported by this browser.");
    }
}

function showPosition(position){
    var loc = [position.coords.latitude, position.coords.longitude];
    L.marker(loc).addTo(map)
        .bindPopup('Your location')
        .openPopup();
    showFoodSources(loc);
}

function showFoodSources(userPosition){
    var total_distance = 0;
    var topLeft = [0,0];
    var bottomRight = [0,0];
    var total_carbon = 0;
    console.log(producers);
    for(var i=0; i < producers.length; i++){
        console.log(producers[i]);
        var country = producers[i];
        var loc = locations[i];
        var line = [userPosition, loc];
        var iconurl = icons[i]

        var icon = new L.icon({iconUrl: "http://"+iconurl,iconSize:[40,40]});
        L.polyline(line, {color: 'red'}).addTo(map);
        console.log(iconurl);
        if(iconurl !== null){
            L.marker(loc, {icon: icon}).addTo(map)
            .bindPopup(ingredients[i])
            .openPopup();
        }else{
            L.marker(loc).addTo(map)
                .bindPopup(ingredients[i])
                .openPopup();
        }
        var dist =  distance(userPosition, loc);
        total_distance += dist;
        var weight = weights[i];
        total_carbon += carbonUsed(dist, weight);
        if(loc[0] < topLeft[0]){
            topLeft[0] = loc[0];
        }
        if(loc[0] > bottomRight[0]){
            bottomRight[0] = loc[0];
        }
        if(loc[1] > topLeft[1]){
            topLeft[1] = loc[1];
        }
        if(loc[1] < bottomRight[1]){
            bottomRight[1] = loc[1];
        }
    }
    map.fitBounds(L.latLngBounds([topLeft, bottomRight]));
    map.setView(userPosition);
    distanceHeader.innerText += total_distance.toFixed(0) + "km";
    carbonHeader.innerText += total_carbon.toFixed(0) + "g";

}

function distance(locA, locB) {
  var R = 6371; // Radius of the earth in km
  var dLat = deg2rad(locB[0]-locA[0]);  // deg2rad below
  var dLon = deg2rad(locB[1]-locA[1]);
  var a =
    Math.sin(dLat/2) * Math.sin(dLat/2) +
    Math.cos(deg2rad(locA[0])) * Math.cos(deg2rad(locB[0])) *
    Math.sin(dLon/2) * Math.sin(dLon/2)
    ;
  var c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1-a));
  var d = R * c; // Distance in km
  return d;
}
function carbonUsed(distance, weight){
    return (distance * carbonData.HGV) * (weight * 0.000001);
}
function percentageAroundEarth(distance){
    return Math.round(distance/40075.017);
}

function deg2rad(deg) {
  return deg * (Math.PI/180)
}

