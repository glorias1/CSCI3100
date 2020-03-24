$(document).ready(function(){
    console.log("event.js ready")
    $.get("navbar.html", function(data){
        $("#navbar").replaceWith(data);
    });
});