//*********************************  Signup visisble  *****************************************

const signupbutton = document.getElementById("signupbutton");
const signupForm = document.getElementById("signupform");
const overlay = document.getElementById("overlay");

// Function to show the signup form
signupbutton.addEventListener("click", function(event) {
    event.stopPropagation(); // Prevent the click from propagating
    signupForm.style.display = "block";
    overlay.style.display = "block";
});

// Function to close the signup form
function closeSignupForm() {
    signupForm.style.display = "none";
    overlay.style.display = "none";
}

// Close the form when clicking outside of it
document.addEventListener("click", function(event) {
    if (signupForm.style.display === "block" && !signupForm.contains(event.target) && event.target !== signupbutton) {
        closeSignupForm();
    }
});

// Prevent closing the form when clicking inside it
signupForm.addEventListener("click", function(event) {
    event.stopPropagation();
});

// Close form on overlay click
overlay.addEventListener("click", closeSignupForm);

//*********************************  End Signup  *****************************************

//*********************************  login button  *****************************************
const loginbutton = document.getElementById("loginbutton");
const loginForm = document.getElementById("loginform");


loginbutton.addEventListener("click", function(event) {
    event.stopPropagation(); // Prevent the click from propagating
    loginForm.style.display = "block";
    overlay.style.display = "block";
    signupForm.style.display = "none"
});

// Function to close the login form
function closeloginForm() {
    loginForm.style.display = "none";
}

// Close the form when clicking outside of it
document.addEventListener("click", function(event) {
    if (loginForm.style.display === "block" && !loginForm.contains(event.target) && event.target !== loginbutton) {
        closeloginForm();
    }
});

// Prevent closing the form when clicking inside it
loginForm.addEventListener("click", function(event) {
    event.stopPropagation();
});

// Close form on overlay click
overlay.addEventListener("click", closeloginForm);

//********************************* End login button  *****************************************

//*********************************  Signup Validation  *****************************************
// Update the validateForm function to show error messages
function validateForm() {
    // Clear previous error messages
    document.getElementById("name-error").innerHTML = "";
    document.getElementById("phone-error").innerHTML = "";
    document.getElementById("email-error").innerHTML = "";
    document.getElementById("username-error").innerHTML = "";
    document.getElementById("password1-error").innerHTML = "";
    document.getElementById("password2-error").innerHTML = "";

    var name1 = document.getElementById("name").value.trim();
    if (name1.length === 0 || name1.length > 50) {
        document.getElementById("name-error").innerHTML = "Please enter a name within 50 characters and not empty.";
        document.getElementById("name-error").style.display = "block"; // Make the error message visible
        return false;
    }

    // Phone validation
    var phone = document.getElementById("phone").value;
    if (phone.length !== 10 || isNaN(phone)) {
        document.getElementById("phone-error").innerHTML = "Enter a valid 10-digit phone number.";
        document.getElementById("phone-error").style.display = "block"; // Make the error message visible
        return false;
    }

    // Email validation
    var email = document.getElementById("signupemail").value;
    if (!email.endsWith("@gmail.com")) {
        document.getElementById("email-error").innerHTML = "Enter a valid Gmail address.";
        document.getElementById("email-error").style.display = "block"; // Make the error message visible
        return false;
    }

    // Username Validation
    var username = document.getElementById("username").value.trim();
    if (username.length <= 5 || username.length === 0 ) {
        document.getElementById("username-error").innerHTML = "Please enter a username more than 5 and less than 7 characters and not empty.";
        document.getElementById("username-error").style.display = "block"; // Make the error message visible
        return false;
    }

    // Password validation
    var pass1 = document.getElementById("password1").value;
    var pass2 = document.getElementById("password2").value;
    var passwordPattern = /^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$/;
    // At least one letter, one number, and 8+ characters

    if (pass1 !== pass2) {
        document.getElementById("password1-error").innerHTML = "Passwords do not match.";
        document.getElementById("password2-error").innerHTML = "Passwords do not match.";
        document.getElementById("password1-error").style.display = "block"; // Make the error message visible
        document.getElementById("password2-error").style.display = "block"; // Make the error message visible
        return false;
    } else if (!passwordPattern.test(pass1)) {
        document.getElementById("password1-error").innerHTML = "Password must contain at least one letter, one number, and be at least 8 characters.";
        document.getElementById("password1-error").style.display = "block"; // Make the error message visible
        return false;
    }

    return true; // All validations passed
}

// *********************************  End Signup Validation  *****************************************

    // Automatically hide messages after 5 seconds
    setTimeout(function() {
        const messages = document.getElementById('messages');
        if (messages) {
            messages.style.display = 'none';
        }
    }, 1000);  // Adjust time as needed (5000 ms = 5 seconds)


//**************************************** password eye visibility *********************************************
    function togglePasswordVisibility(passwordFieldId, toggleIconId) {
        const passwordField = document.getElementById(passwordFieldId);
        const toggleIcon = document.getElementById(toggleIconId);
    
        toggleIcon.addEventListener("click", function () {
            if (passwordField.type === "password") {
                passwordField.type = "text";  // Show password
                toggleIcon.src = 'static/images/eye.png';
            } else {
                passwordField.type = "password";  // Hide password
                toggleIcon.src = 'static/images/hidden.png';
            }
        });
    }
    
    // Initialize toggle for each password field
    togglePasswordVisibility("password1", "togglePassword1");
    togglePasswordVisibility("password2", "togglePassword2");
    togglePasswordVisibility("loginpassword", "toggleLoginPassword");
    
//**************************************** password eye visibility *********************************************
