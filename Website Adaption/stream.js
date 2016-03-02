
/*
/* Stream js
/* This code recieves the information from the user and passes that information through to my stream finder application using ajax.
The application returns the link with the proper html to appear for the user
-----------------------------------------------------------------------------------*/  

$(document).ready(function() {
    console.log("ready!");
    var submitButton = $("#submit");
    var subreddit = $("#subreddit");
    var team = $("#team");
    var type = $("#type");
    submitButton.click(function() {
        $.ajax({
            url: "/stream/api",
            type: "get",
            data: {
	            subreddit: subreddit.val(),
	            team: team.val(),
	            type: type.val()
            },
            success: function(response) {
	            //console.log("<a href ="+ response + "target='_blank'>" + response + "</a>");
	            $('#answer').replaceWith("<a href ="+ response + " target='_blank'>" + response + "</a>");
            },
            error: function(xhr) {
	            console.log(xhr)
	            $('#answer').replaceWith("<p>Error! Please Try Again Later</p>");
            }
        });
        return false;
    });
});
