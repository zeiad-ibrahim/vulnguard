// When someone clicks the Sign Up button, this code runs
document.getElementById("signupForm").addEventListener("submit", function(event) { 
    event.preventDefault(); // Stop the form from sending right away

    var email = document.getElementById("email").value.trim(); // Get what the user typed in the email field and remove extra spaces
    var password = document.getElementById("newPassword").value.trim(); // Get what the user typed in the password field and remove extra spaces
    var confirmPassword = document.getElementById("confirmPassword").value.trim(); // Get what the user typed in the confirm password field and remove extra spaces
    var message = document.getElementById("message"); // This is to be able to show messages to the user
    let valid = true; // This will be used for validation to track if all checks pass

    if (email === "" || password === "" || confirmPassword === "") { // Checks if any of the fields are empty
        message.textContent = "Please make sure no fields are left empty"; // If any are empty then this message will be outputted
        message.className = "error"; // Error will occur
        valid = false; // Stop if something is empty
    }

    if (valid && password.length < 8) { // Checks if password is less than 8 characters
        message.textContent = "Password needs to be at least 8 characters long"; // If it is then this message will be outputted
        message.className = "error"; // Error will occur
        valid = false; // Stop if password is shorter than 8 characters
    }

    if (valid) { 
        var uppercase = false; 
        var lowercase = false; 
        var number = false; 
        for (var i = 0; i < password.length; i++) { // Runs a for loop function for each character in the password inputted
            if (password[i] >= 'A' && password[i] <= 'Z') { // Checks if the character is an uppercase letter
                uppercase = true; 
            } else if (password[i] >= 'a' && password[i] <= 'z') { // Checks if the character is a lowercase letter
                lowercase = true; 
            } else if (password[i] >= '0' && password[i] <= '9') { // Checks if the character is a number
                number = true; 
            }
        }
        if (uppercase == false || lowercase == false || number == false) { // Makes sure that all three conditions are met
            message.textContent = "Password needs at least one uppercase letter, one lowercase letter, and one number"; 
            message.className = "error"; // If not a message will be outputted and error will happen
            valid = false; // Stop if password doesn’t meet all conditions
        }
    }

    if (valid && password != confirmPassword) { // Checks if the password and confirm password are the same
        message.textContent = "The passwords don't match, please check and try again"; // If not this message will be outputted
        message.className = "error"; // Error will occur
        valid = false; // Stop if passwords aren’t the same
    }

    if (valid) {  // Only proceed with the fetch if all validations pass
        // next few lines will send the data to the Python code if all requirements are met:
        fetch("/signup", {
            method: "POST",
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ email: email, password: password, confirm_password: confirmPassword })
        })
        // Get the answer from Python file:
        .then(function(response) { return response.json(); })
        .then(function(data) {
            // Show a message depending on what Python says:
            if (data.success) {
                message.textContent = "Account created successfully"; // If answer from Python is success then this message will be outputted
                message.className = "success"; // No error will occur and data are successfully inputted
                window.location.href = "/mainpage"; // Direct the user to the homepage
            } else {
                message.textContent = data.error; // If answer from Python code is not success this message will be outputted
                message.className = "error"; // Error will occur
            }
        })
        .catch(function(error) {
            message.textContent = "Something went wrong. Try again."; // If something else goes wrong then error is showed
            message.className = "error"; // Error will occur
            console.log("Error:", error);
        });
    }
});
