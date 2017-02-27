var map = L.map('map').setView([51.505, -0.09], 13);

var mealData = {
    "user_location" : "Bristol",
    "meal" : "lasagne",
    "ingredients" : [
    {
        "name" : "onion",
        "origin" : [55.378051,-3.435973]},
    {"name" : "beef",
     "origin" : [55.378051,-3.435973]},
    {"name" : "prosciutto",
     "origin" : [41.87194,12.56738]},
    {"name" : "tomato",
      "origin" : [40.463667,-3.74922]},
    {"name" : "pasta",
        "origin" : [41.87194,12.56738]},
    {"name" : "mozzarella",
    "origin" : [41.87194,12.56738]}]
};

var distanceHeader = document.getElementById("distance");
var mealHeader = document.getElementById("meal");
mealHeader.innerText = mealData.meal;
L.tileLayer('http://{s}.tile.osm.org/{z}/{x}/{y}.png', {
    attribution: '&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors'
}).addTo(map);
getLocation();

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
    for(var i=0; i < mealData.ingredients.length; i++){
        var ingredient = mealData.ingredients[i];
        var loc = ingredient.origin;
        var line = [userPosition, loc];
        L.polyline(line, {color: 'red'}).addTo(map);
        L.marker(loc).addTo(map)
        .bindPopup(ingredient.name)
        .openPopup();
        total_distance += distance(userPosition, loc);
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

function deg2rad(deg) {
  return deg * (Math.PI/180)
}