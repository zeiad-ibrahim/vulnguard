document.getElementById("loginForm").addEventListener("submit", function(event) { 
    event.preventDefault(); // prevent the form from submitting immediately

    var email = document.getElementById("email").value.trim(); // fetches the email input and remove extra spaces
    var password = document.getElementById("password").value.trim(); // feetches the password input and remove extra spaces
    var message = document.getElementById("message"); // gets the message element to be able to display errors or success
    let valid = true; // set a flag to track if all validations pass

    if (email === "" || password === "") { // Check if email or password is empty
        message.textContent = "Please make sure no fields are left empty"; // Display error if fields are empty
        message.className = "error"; // set the message class to error
        valid = false; // Set valid variable to false
    }

    if (valid) { // send data to the server if validations pass
        fetch('/login', { 
            method: 'POST', // set request method to POST
            headers: { 'Content-Type': 'application/json' }, // set content type to JSON
            body: JSON.stringify({ email: email, password: password }) // Converts email and password to JSON
        })
        .then(function(response) { return response.json(); }) // Converts the server response to JSON
        .then(function(data) { 
            if (data.success) {
                message.textContent = "Login successful!"; // Display success message
                message.className = "success"; // set message class to success
                window.location.href = '/mainpage'; // directs user to the homepage route
            } else {
                message.textContent = "Invalid Email or Password"; // display error message from server
                message.className = "error"; // sets message class to error
            }
        })
        .catch(function(error) { // to handle any network or server errors
            message.textContent = "Something went wrong. Try again."; // Display generic error message
            message.className = "error"; // set message class to error
            console.log("Error:", error); //
        });
    }
});