// Get CSRF token from hidden input
function getCSRFToken() {
    const tokenInput = document.querySelector('[name=csrfmiddlewaretoken]');
    if (!tokenInput) {
        console.error("CSRF token input not found!");
        return '';
    }
    return tokenInput.value;
}
//-------------------------------------------------------------------------

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
        .then(response => response.json()) // Parse the JSON response
        .then(result => {
            console.log("✅ Success:", result);
            
            if (result.status === 'error') {
                // If there's an error, show the error message from the server in the modal
                const errorMessage = document.getElementById("error-message");
                errorMessage.style.display = 'block'; // Make the error message visible
                errorMessage.textContent = result.message || "An unknown error occurred. Please try again.";
            } else {
                // If success, reload the page or reset the form
                // alert("User added successfully!");
                window.location.reload();
            }
        })
        .catch(error => {
            // Prevent generic error alert by handling errors here
            console.error("❌ Error:", error);
            // Optionally, you can log the error here without showing an alert
            // alert("An unexpected error occurred.");
        });
    });
});


//-------------------------------------------------------------------------
document.querySelectorAll("form[id^='editUserForm']").forEach((form) => {
  form.addEventListener("submit", function (e) {
      e.preventDefault();

      const userId = this.id.replace("editUserForm", "");
      const data = {
          first_name: document.getElementById(`edit_first_name${userId}`).value,
          last_name: document.getElementById(`edit_last_name${userId}`).value,
          email: document.getElementById(`edit_email${userId}`).value,
          phone_number: document.getElementById(`edit_phone_number${userId}`).value,
          access_level: document.getElementById(`edit_access_level${userId}`).value,
          verified: document.getElementById(`edit_verified${userId}`).checked,
          password: document.getElementById(`edit_password${userId}`).value,
          user_code: document.getElementById(`edit_user_code${userId}`).value,
      };

      const csrfToken = getCSRFToken();

      fetch("/cdps/admin/accountManagement/edit-user/", {
          method: "POST",
          headers: {
              "Content-Type": "application/json",
              "X-CSRFToken": csrfToken,
          },
          body: JSON.stringify(data),
      })
      .then(response => {
          if (!response.ok) throw new Error("Network response was not ok");
          return response.json();
      })
      .then(result => {
          console.log("✅ Edit success:", result);
          window.location.reload();  // Reload page after edit
      })
      .catch(error => {
          console.error("❌ Edit error:", error);
          const errorBox = document.getElementById(`error-message${userId}`);
          if (errorBox) {
              errorBox.innerText = "Error updating user.";
              errorBox.style.display = "block";
          }
      });
  });
});

//-------------------------------------------------------------------------
document.querySelectorAll(".delete-user-btn").forEach((button) => {
  button.addEventListener("click", function () {
      const userId = this.getAttribute("data-user-id");
      const userCode = document.getElementById(`delete_user_code${userId}`).value;
      const csrfToken = getCSRFToken();

      fetch("/cdps/admin/accountManagement/delete-user/", {
          method: "POST",
          headers: {
              "Content-Type": "application/json",
              "X-CSRFToken": csrfToken,
          },
          body: JSON.stringify({ user_code: userCode }),
      })
      .then(response => {
          if (!response.ok) throw new Error("Delete failed");
          return response.json();
      })
      .then(result => {
          console.log("🗑️ User deleted:", result);
          window.location.reload();
      })
      .catch(error => {
          console.error("❌ Delete error:", error);
          alert("Something went wrong. See console for details.");
      });
  });
});

//-------------------------------------------------------------------------
//-------------------------------------------------------------------------
