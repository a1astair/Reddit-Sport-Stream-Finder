
/*
/* Stream js
/* This code recieves the information from the user and passes that information through to my stream finder application using ajax.
The application returns the link with the proper html to appear for the user
-----------------------------------------------------------------------------------*/  

$(document).ready(function() {
    var subreddit = $("#subreddit");
    var submitSport = $('#submitsport');
    submitSport.click(function() {
        $.ajax({
                url: "/stream/api/sport",
                type: "get",
                data: {
	                subreddit: subreddit.val()
                },
                success: function(response) {
                    var allTeams = jQuery.parseJSON(response)
                    var i;
                    $('#teamdisplay').replaceWith("<p>Team(s)</p>");
                    $('#teams').replaceWith(
                        $('<select id="teams" class="mytext"></select>')
                    );
	                for(i = 0; i < allTeams.length; i++) {
	                    $('#teams').append(
	                        $('<option></option>').val(allTeams[i]).html(allTeams[i])
                        );
                    }
	                
                },
                error: function(xhr) {
	                console.log(xhr)
                }
            });
            return false;
        });
    var type = $("#type");
    var submitButton = $("#submit");
    
    submitButton.click(function() {
        $.ajax({
            url: "/stream/api",
            type: "get",
            data: {
                subreddit: subreddit.val(),
	            team: $("#teams").val(),
	            type: type.val()
            },
            success: function(response) {
	            //Will add the submit button so they can resubmit instead of having to refresh the page to try again
	            //$('#submit').replaceWith('<input type="Submit"value="Submit" id="submit">');
	            $('#submit').replaceWith("<p>Enjoy!</p><a href ="+ response + " target='_blank'>" + response + "</a><br>");
            },
            error: function(xhr) {
	            console.log(xhr)
	            $('#answer').replaceWith("<p>No Stream Found! Please Try Again Later</p>");
            }
        });
        return false;
    });
});
