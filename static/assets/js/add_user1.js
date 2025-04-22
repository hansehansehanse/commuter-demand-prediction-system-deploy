// Get CSRF token from hidden input
function getCSRFToken() {
    const tokenInput = document.querySelector('[name=csrfmiddlewaretoken]');
    if (!tokenInput) {
        console.error("CSRF token input not found!");
        return '';
    }
    return tokenInput.value;
}

// document.addEventListener("DOMContentLoaded", function () {
//     const submitBtn = document.getElementById("submitUserBtn");
//     alert("hi 1")
//     if (submitBtn) {
//         submitBtn.addEventListener("click", function () {
//             console.log("🔘 Submit button clicked");

//             const firstName = document.getElementById("first_name").value;
//             const lastName = document.getElementById("last_name").value;
//             const email = document.getElementById("email").value;
//             const phoneNumber = document.getElementById("phone_number").value;
//             const accessLevel = document.getElementById("access_level").value;
//             const verified = document.getElementById("verified").checked;
//             const password = document.getElementById("password").value;

//             const userData = {
//                 first_name: firstName,
//                 last_name: lastName,
//                 email: email,
//                 phone_number: phoneNumber,
//                 access_level: accessLevel,
//                 verified: verified,
//                 password: password,
//             };

//             console.log("📦 User data:", userData);

//             console.log("firstName value:", document.getElementById("first_name").value);

//             alert("hi 2")
//         //     fetch("/cdps/admin/accountManagement/add-user/", {
//         //         method: "POST",
//         //         headers: {
//         //             "Content-Type": "application/json",
//         //             "X-CSRFToken": getCSRFToken(),
//         //         },
//         //         body: JSON.stringify(userData),
//         //     })
//         //         .then((response) => {
//         //             if (response.ok) {
//         //                 console.log("✅ User added successfully!");
//         //                 location.reload(); // Refresh to see updated table
//         //             } else {
//         //                 console.error("❌ Failed to add user:", response.statusText);
//         //             }
//         //         })
//         //         .catch((error) => {
//         //             console.error("🚨 Error submitting user data:", error);
//         //         });
//         // });

// });



// static/assets/js/add_user1.js
document.addEventListener("DOMContentLoaded", function () {
    // Grab the form by its ID
    const form = document.getElementById("addUserForm");

    if (!form) return;
    console.log("i see form");

    form.addEventListener("submit", function (e) {
        e.preventDefault();  // stop the normal POST

        // Collect all inputs by their IDs
        const data = {
            first_name: document.getElementById("first_name").value,
            last_name: document.getElementById("last_name").value,
            email: document.getElementById("email").value,
            phone_number: document.getElementById("phone_number").value,
            access_level: document.getElementById("access_level").value,
            verified: document.getElementById("verified").checked,  // fix: use .checked for checkbox
            password: document.getElementById("password").value,
        };

        console.log("🔘 Submit button clicked");
        console.log("📦 User data:", data);



        // Send it to Django using fetch
        const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

        fetch("/cdps/admin/accountManagement/add-user/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": csrfToken,
            },
            body: JSON.stringify(data)
        })
        .then(response => {
            if (!response.ok) throw new Error("Network response was not ok");
            return response.json();
        })
        .then(result => {
            console.log("✅ Success:", result);
            // alert(result.message || "User added!");
            window.location.reload();
        })
        .catch(error => {
            console.error("❌ Error:", error);
            alert("Something went wrong. See console for details.");
        });
    });
});
