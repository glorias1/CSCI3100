$(document).ready(function(){
    console.log("event.js ready")
    $.get("navbar.html", function(data){
        $("#navbar").replaceWith(data);
    });
    $.get("navbar_after_login.html", function(data){
        $("#navbar-logged").replaceWith(data);
    });
});