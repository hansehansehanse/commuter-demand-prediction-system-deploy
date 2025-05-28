document.addEventListener("DOMContentLoaded", function () {
    const form = document.getElementById("addHistoricalEventForm");

    if (!form) return;

    form.addEventListener("submit", function (e) {
        e.preventDefault();

        const data = {
            event_name: document.getElementById("historical_event_name").value,
            event_type: document.getElementById("historical_event_type").value,
            date: document.getElementById("historical_event_date").value,
        };

        console.log("🕰️ Submit historical event clicked");
        console.log("📦 Event data:", data);

        const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

        fetch("/cdps/admin/historicalDatasetUpload/addHistoricalEvent/", {

            
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": csrfToken,
            },
            body: JSON.stringify(data)
        })
        .then(response => response.json())
        .then(result => {
            console.log("✅ Response:", result);

            const responseBox = document.getElementById("historicalFormResponse");
            responseBox.style.display = 'block';
            responseBox.classList.remove('alert-danger', 'alert-success');

            if (result.status === 'error') {
                responseBox.classList.add('alert-danger');
                responseBox.textContent = result.message || "Unknown error occurred.";
            } else {
                responseBox.classList.add('alert-success');
                responseBox.textContent = "Event added successfully!";
                window.location.reload();
            }
        })
        .catch(error => {
            console.error("❌ JS Error:", error);
        });
    });
});



document.querySelectorAll("form[id^='editHistoricalEventForm']").forEach((form) => {
    form.addEventListener("submit", function (e) {
      e.preventDefault();
  
      const eventId = this.id.replace("editHistoricalEventForm", "");
  
      const data = {
        event_code: document.getElementById(`edit_historical_event_code${eventId}`).value,
        event_name: document.getElementById(`edit_historical_event_name${eventId}`).value,
        event_type: document.getElementById(`edit_historical_event_type${eventId}`).value,
        date: document.getElementById(`edit_historical_event_date${eventId}`).value,
        id: document.getElementById(`edit_historical_event_id${eventId}`).value,
      };
  
      const csrfToken = getCSRFToken();  // Assumes this function already exists
  
      fetch("/cdps/admin/historicalDatasetUpload/editHistoricalEvent/", {
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
          console.log("✅ Historical event edit success:", result);
          window.location.reload(); // Optional
        })
        .catch(error => {
          console.error("❌ Edit historical event error:", error);
          const errorBox = document.getElementById(`historical-event-error-message${eventId}`);
          if (errorBox) {
            errorBox.innerText = "Error updating historical event.";
            errorBox.style.display = "block";
          }
        });
    });
  });



  document.querySelectorAll(".delete-event-btn").forEach((button) => {  
    button.addEventListener("click", function () {
        const eventId = this.getAttribute("data-event-id");
        const eventCode = document.getElementById(`delete_event_code${eventId}`).value;
        const csrfToken = getCSRFToken();

        fetch("/cdps/admin/historicalDatasetUpload/deleteHistoricalEvent/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": csrfToken,
            },
            body: JSON.stringify({ event_code: eventCode }),
        })
            .then((response) => {
                if (!response.ok) throw new Error("Delete failed");
                return response.json();
            })
            .then((result) => {
                console.log("🗑️ Historical Event deleted:", result);
                window.location.reload();
            })
            // .catch((error) => {                                                          # removed catch since it contradicts with sp_addHistoricalEvent2.js
            //     console.error("❌ Delete error:", error);
            //     alert("Something went wrong. See console for details.");
            // });
    });
});


//!!!! bat 2 delete ko
// document.querySelectorAll(".delete-event-btn").forEach((button) => {
//     button.addEventListener("click", function () {
//         const eventId = this.getAttribute("data-event-id");
//         const eventCode = document.getElementById(`delete_event_code${eventId}`).value;
//         const csrfToken = getCSRFToken();
  
//         fetch("/cdps/admin/historicalDatasetUpload/deleteHistoricalEvent/", {
//             method: "POST",
//             headers: {
//                 "Content-Type": "application/json",
//                 "X-CSRFToken": csrfToken,
//             },
//             body: JSON.stringify({ event_code: eventCode }),
//         })
//         .then(response => {
//             if (!response.ok) throw new Error("Delete failed");
//             return response.json();
//         })
//         .then(result => {
//             console.log("🗑️ Event deleted:", result);
//             window.location.reload();
//         })
//         .catch(error => {
//             console.error("❌ Delete error:", error);
//             alert("Something went wrong. See console for details.");
//         });
//     });
//   });



