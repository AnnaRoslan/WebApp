window.onload = () => {
    document.getElementById("firstName").addEventListener("focusout", () => validateFirstName());
    document.getElementById("lastName").addEventListener("focusout", () => validateLastName());
    document.getElementById("email").addEventListener("focusout", () => validateEmail());
    document.getElementById("password").addEventListener("focusout", () => validatePassword());
    document.getElementById("password2").addEventListener("focusout", () => validatePassword2());
    document.getElementById("login").addEventListener("focusout", () => validateLogin());
    document.getElementById("register").onclick = () => register();
}



function validateFirstName() {
    var field = document.getElementById("firstName");
    if (field.value === "" || field.value.match(/^([A-Z]|�|�|�|�|�|�|�|�)([a-z]|�|�|�|�|�|�|�|�)*/gm) === null) {
        field.classList.add("is-invalid");
        document.getElementById("firstNameText").textContent = "First Name is not valid";
        return false;
    } else {
        field.classList.remove("is-invalid");
        document.getElementById("firstNameText").textContent = "";
        return true;
    }
}

function validateLastName() {
    var field = document.getElementById("lastName");
    if (field.value === "" || field.value.match(/^([A-Z]|�|�|�|�|�|�|�|�)([a-z]|�|�|�|�|�|�|�|�)*/gm) === null) {
        field.classList.add("is-invalid");
        document.getElementById("lastNameText").textContent = "Last name  is not valid";
        return false;
    } else {
        field.classList.remove("is-invalid");
        document.getElementById("lastNameText").textContent = "";
        return true;
    }
}

function validateEmail() {
    var field = document.getElementById("email");
    if (field.value === "" || field.value.match(
            /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/) === null) {
        field.classList.add("is-invalid");
        document.getElementById("emailText").textContent = "email is not valid";
        return false;
    } else {
        field.classList.remove("is-invalid");
        document.getElementById("emailText").textContent = "";
        return true;
    }
}

function validatePassword() {
    var field = document.getElementById("password");
    validatePassword2()
    if (field.value.length < 3) {
        field.classList.add("is-invalid");
        document.getElementById("passwordText").textContent = "Password is not strong enough";
        return false;
    } else {
        field.classList.remove("is-invalid");
        document.getElementById("passwordText").textContent = "";
        return true;
    }
}

function validatePassword2() {
    var field = document.getElementById("password2");
    var passwd = document.getElementById("password");
    if (!(field.value == passwd.value) || field.value.length < 3) {
        field.classList.add("is-invalid");
        document.getElementById("password2Text").textContent = "Password are not the same!";
        return false;
    } else {
        field.classList.remove("is-invalid");
        document.getElementById("password2Text").textContent = "";
        return true;
    }
}

function validateLogin() {
    var field = document.getElementById("login");
    var isValid = false;

    if (field.value === "" || field.value.length < 4 || field.value.match(/^[a-z]{3,12}/) === null) {
        field.classList.add("is-invalid");
        document.getElementById("loginText").textContent = "Login is not valid";
    } else {
        field.classList.remove("is-invalid");
        document.getElementById("loginText").textContent = "";
        isValid = true;
    }
    return isValid;
}


function isValid() {
    return validateFirstName() && validateEmail() && validateLastName() && validatePassword() && validatePassword2() && validateLogin();
}


function register() {
    if (!isValid()) {
        return false;
    }
}