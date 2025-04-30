// // Get CSRF token from hidden input
// function getCSRFToken() {
//     const tokenInput = document.querySelector('[name=csrfmiddlewaretoken]');
//     if (!tokenInput) {
//         console.error("CSRF token input not found!");
//         return '';
//     }
//     return tokenInput.value;
// }

// document.addEventListener("DOMContentLoaded", function () {
//     const form = document.getElementById("addEventForm");

//     if (!form) return;

//     form.addEventListener("submit", function (e) {
//         e.preventDefault();  // Prevent the form from being submitted immediately
//         console.log("Data1");

//         // Check if the elements are actually being selected
//         const event_name = document.getElementById("event_name");
//         const event_type = document.getElementById("event_type");
//         const date = document.getElementById("date");

//         console.log("event_name:", event_name);
//         console.log("event_type:", event_type);
//         console.log("date:", date);

//         if (event_name && event_type && date) {
//             const data = {
//                 event_name: event_name.value,
//                 event_type: event_type.value,
//                 date: date.value,
//             };
//             console.log("Data2:", data);

//             // Send data to the server using fetch
//             fetch("/cdps/admin/datasetTemporal/addEvent/", {
//                 method: "POST",
//                 headers: {
//                    "Content-Type": "application/json",
//                    "X-CSRFToken": getCSRFToken(),
//                 },
//                 body: JSON.stringify(data),
//              })
//              .then(response => response.json())
//              .then(result => {
//                  console.log(result);
//                  if (result.status === "success") {
//                     //  alert("Event added successfully!");
//                     window.location.reload();
//                  }
//              })
//              .catch(error => {
//                  console.error("Error adding event:", error);
//              });
             
//         } else {
//             console.error("One or more form elements are missing!");
//         }
//     });
// });

// Get CSRF token from hidden input
function getCSRFToken() {
    const tokenInput = document.querySelector('[name=csrfmiddlewaretoken]');
    if (!tokenInput) {
        console.error("CSRF token input not found!");
        return '';
    }
    return tokenInput.value;
}

document.addEventListener("DOMContentLoaded", function () {
    const form = document.getElementById("addEventForm");

    if (!form) return;

    form.addEventListener("submit", function (e) {
        e.preventDefault();  // Prevent the form from being submitted immediately

        const event_name = document.getElementById("event_name");
        const event_type = document.getElementById("event_type");
        const day = document.getElementById("event_day");
        const month = document.getElementById("event_month");
        const year = document.getElementById("event_year");  // Optional

        if (event_name && event_type && day && month) {
            const data = {
                event_name: event_name.value,
                event_type: event_type.value,
                day: parseInt(day.value),
                month: parseInt(month.value),
                year: year?.value ? parseInt(year.value) : null
            };

            // Send data to the server using fetch
            fetch("/cdps/admin/datasetTemporal/addEvent/", {
                method: "POST",
                headers: {
                   "Content-Type": "application/json",
                   "X-CSRFToken": getCSRFToken(),
                },
                body: JSON.stringify(data),
             })
             .then(response => response.json())
             .then(result => {
                 if (result.status === "success") {
                    window.location.reload();
                 } else {
                    console.error("Server error:", result.message);
                 }
             })
             .catch(error => {
                 console.error("Error adding event:", error);
             });
        } else {
            console.error("One or more form elements are missing!");
        }
    });
});
