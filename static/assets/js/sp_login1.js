
function togglePassword() {
    const passwordField = document.getElementById("password");
    const toggleBtn = passwordField.nextElementSibling;
    if (passwordField.type === "password") {
        passwordField.type = "text";
        toggleBtn.textContent = "Hide";
    } else {
        passwordField.type = "password";
        toggleBtn.textContent = "Show";
    }
}


function fillAdmin() {
    document.getElementById('email').value = 'admin@example.com';
    document.getElementById('password').value = 'adminpassword123';
}

function fillBusManager() {
    document.getElementById('email').value = 'busmanager@example.com';
    document.getElementById('password').value = 'busmanagerpassword123';
}


function togglePassword() {
    const passwordInput = document.getElementById("password");
    const icon = document.getElementById("togglePasswordIcon");

    if (passwordInput.type === "password") {
        passwordInput.type = "text";
        icon.classList.remove("bi-eye");
        icon.classList.add("bi-eye-slash");
    } else {
        passwordInput.type = "password";
        icon.classList.remove("bi-eye-slash");
        icon.classList.add("bi-eye");
    }
}

