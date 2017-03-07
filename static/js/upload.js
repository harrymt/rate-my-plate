var imageUploadForm = document.getElementById("imageUpload");

var sendImage = function(result){
    var display = document.getElementById("displayimg");
    display.src =  result.target.result;
    var request = new XMLHttpRequest();
    request.open('POST', "https://ratemyplate.world/", true);
    request.setRequestHeader("Content-type", "application/json");
    request.send(data);
    var data = JSON.stringify({image: result.target.result});
}

function upload(){
    var imageUrl = imageUploadForm.value;
    var fReader = new FileReader();
    fReader.readAsDataURL(imageUploadForm.files[0]);
    fReader.onloadend = sendImage;

    console.log(imageUrl);
}