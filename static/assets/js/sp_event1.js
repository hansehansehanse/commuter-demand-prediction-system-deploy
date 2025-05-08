document.querySelectorAll("form[id^='editEventForm']").forEach((form) => {
    form.addEventListener("submit", function (e) {
      e.preventDefault();
  
      const eventId = this.id.replace("editEventForm", "");
  
      const data = {
        event_code: document.getElementById(`edit_event_code${eventId}`).value,
        event_name: document.getElementById(`edit_event_name${eventId}`).value,
        event_type: document.getElementById(`edit_event_type${eventId}`).value,
        date: document.getElementById(`edit_event_date${eventId}`).value,
        id: document.getElementById(`edit_event_id${eventId}`).value,
      };
  
      const csrfToken = getCSRFToken();  // Same CSRF helper you used in the user form
  
      fetch("/cdps/admin/datasetTemporal/edit-event/", {
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
          console.log("✅ Event edit success:", result);
          window.location.reload(); // Optional: reload to reflect changes
        })
        .catch(error => {
          console.error("❌ Event edit error:", error);
          const errorBox = document.getElementById(`event-error-message${eventId}`);
          if (errorBox) {
            errorBox.innerText = "Error updating event.";
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
  
        fetch("/cdps/admin/datasetTemporal/delete-event/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": csrfToken,
            },
            body: JSON.stringify({ event_code: eventCode }),
        })
        .then(response => {
            if (!response.ok) throw new Error("Delete failed");
            return response.json();
        })
        .then(result => {
            console.log("🗑️ Event deleted:", result);
            window.location.reload();
        })
        // .catch(error => {                                                                      # removed catch since it contradicts with sp_event1.js
        //     console.error("❌ Delete error:", error);
        //     alert("Something went wrong. See console for details.");
        // });
    });
  });
  



  document.querySelectorAll("form[id^='editHolidayEventForm']").forEach((form) => {
    form.addEventListener("submit", function (e) {
      e.preventDefault();
  
      const eventId = this.id.replace("editHolidayEventForm", "");
  
      const data = {
        event_code: document.getElementById(`edit_event_code${eventId}`).value,
        event_name: document.getElementById(`edit_event_name${eventId}`).value,
        
        date: document.getElementById(`edit_event_date${eventId}`).value,
        id: document.getElementById(`edit_event_id${eventId}`).value,
      };
  
      const csrfToken = getCSRFToken();  // Same CSRF helper you used in the user form
  
      fetch("/cdps/admin/holiday-event/edit-holidayevent/", {  // Update URL to match your Django URL for editing a holiday event
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
        console.log("✅ Holiday event edit success:", result);
        window.location.reload(); // Optional: reload to reflect changes
      })
      .catch(error => {
        console.error("❌ Holiday event edit error:", error);
        const errorBox = document.getElementById(`holiday-event-error-message${eventId}`);
        if (errorBox) {
          errorBox.innerText = "Error updating holiday event.";
          errorBox.style.display = "block";
        }
      });
    });
  });
  