$(document).ready( function() {
    // Run when the confirm button in modal been clicked
    $(document).on("click", "#loginFormButton" , function(event) {
        // Get the email input
        var email = $("#exampleInputEmail").val();
        // Get the password input
        var passwd = $("#exampleInputPassword").val();

        $.ajax({
            type : "POST",
            url : "/loginresponse",
            contentType: "application/json",
            data : JSON.stringify({
                        email: email,
                        password: passwd
                    }),  
            dataType: "json",
            // Communication to the server success
            success: function(data) {
                        // If login success
                        if(data.status == true) {
                            // Redirect the user to Dashboard page
                            window.location.href = '/dashboard';
                        }
                        // If login failed
                        if(data.status == false) {
                            $('#notificationModalMessage').empty();
                            $("#notificationModalMessage").append( "<p>" + data.errormessage + "</p>" );
                            $('#modal-1').modal('toggle');
                        }
                    },
            // Communication to the server failed
            error: function(data) {
                        alert("Failed to connect to the server!");
                    },
        });
    });
});
