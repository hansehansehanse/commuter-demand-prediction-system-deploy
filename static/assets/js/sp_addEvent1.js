document.addEventListener("DOMContentLoaded", function () {
    // Grab the form by its ID
    const form = document.getElementById("addEventForm");

    if (!form) return;

    form.addEventListener("submit", function (e) {
        e.preventDefault();  // stop the normal POST

        // Collect all inputs by their IDs
        const data = {
            event_name: document.getElementById("event_name").value,
            event_type: document.getElementById("event_type").value,
            date: document.getElementById("date").value,
        };

        console.log("🔘 Submit button clicked");
        console.log("📦 Event data:", data);

        // Send it to Django using fetch
        const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

        fetch("/cdps/admin/datasetTemporal/addEvent/", {
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
                const errorMessage = document.getElementById("formResponse");
                errorMessage.classList.add('alert-danger');  // Add error styling
                errorMessage.style.display = 'block'; // Make the error message visible
                errorMessage.textContent = result.message || "An unknown error occurred. Please try again.";
            } else {
                // If success, reload the page or reset the form
                window.location.reload();  // Reload the page to reflect the new event
            }
        })
        .catch(error => {
            console.error("❌ Error:", error);
            // Optionally, you can log the error here without showing an alert
        });
    });
});
