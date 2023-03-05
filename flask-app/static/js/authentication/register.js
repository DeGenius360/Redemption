$(document).ready( function() {
    // Run when the confirm button in modal been clicked
    $(document).on("click", "#registerFormButton" , function(event) {
        // Get the first name
        var firstname = $("#exampleFirstName").val();
        // Get the last name
        var lastname = $("#exampleLastName").val();
        // Get the email input
        var email = $("#exampleInputEmail").val();
        // Get the password input
        var passwd = $("#examplePasswordInput").val();
        // Get the repeated password input
        var passwdRepeat = $("#exampleRepeatPasswordInput").val();

        // Validate if two password is same
        // Two password are same, continue
        if (passwd == passwdRepeat) {
            $.ajax({
                type : "POST",
                url : "/registerresponse",
                contentType: "application/json",
                data : JSON.stringify({
                            firstname: firstname,
                            lastname: lastname,
                            email: email,
                            passwd: passwd
                        }),  
                dataType: "json",
                // Communication to the server success
                success: function(data) {
                            // If register status is success
                            if(data.status == true) {
                                // Redirect the user to Dashboard page
                                window.location.href = '/dashboard';
                            }
                            // If register status is  failed
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
        }
        // Two password are different
        else
        {
            // Output error message
            $('#notificationModalMessage').empty();
            $("#notificationModalMessage").append( "<p>Password does not match!</p>" );
            $('#modal-1').modal('toggle');
        }
    });
});
