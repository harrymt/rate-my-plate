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

console.log(mealData);
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
    map.setView(loc, 2);
    showFoodSources();
}

function showFoodSources(){
    for(var i=0; i < mealData.ingredients.length; i++){
        var ingredient = mealData.ingredients[i];
        console.log(ingredient);
        var loc = ingredient.origin;
        L.marker(loc).addTo(map)
        .bindPopup(ingredient.name)
        .openPopup();
    }
}