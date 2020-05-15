$(document).ready(function(){
    console.log("event.js ready")
    $.get("navbar.html", function(data){
        $("#navbar").replaceWith(data);
    });
    $.get("navbar_after_login.html", function(data){
        $("#navbar-logged").replaceWith(data);
    });
    $(document).on("click", "button#create_project",function(){
        window.location.href='./create_project.html';
    });
    $(document).on("click", "button#login",function(){
        window.location.href='./index.html';
    });
	$(function(){
		$("#open-login-page").load("login.html");
	});
});