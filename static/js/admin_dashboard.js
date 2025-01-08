document.addEventListener("DOMContentLoaded", () => {
    // View Details
    document.querySelectorAll(".view-details").forEach(button => {
        button.addEventListener("click", () => {
            const id = button.dataset.id;

            fetch(`/get-appointment-details/${id}/`)
                .then(response => response.json())
                .then(data => {
                    document.getElementById("user-name").textContent = data.name;
                    document.getElementById("user-email").textContent = data.email;
                    document.getElementById("user-phone").textContent = data.phone_number || "Not provided";

                    openModal("user-details-modal");
                });
        });
    });

    // Edit Appointment
    document.querySelectorAll(".edit-btn").forEach(button => {
        button.addEventListener("click", () => {
            const id = button.dataset.id;
            const row = button.closest("tr");

            fetch(`/get-appointment-details/${id}/`)
                .then(response => response.json())
                .then(data => {
                    removeExistingModals(); // Ensure no overlapping modals

                    // Dynamically insert the edit modal just below the row
                    const modal = createEditModal(data);
                    row.insertAdjacentElement("afterend", modal);

                    document.getElementById("edit-form").addEventListener("submit", function (event) {
                        event.preventDefault();
                        const formData = new FormData(this);

                        fetch(`/edit-appointment/${id}/`, {
                            method: "POST",
                            body: formData,
                            headers: {
                                "X-CSRFToken": document.querySelector("[name=csrfmiddlewaretoken]").value,
                            },
                        })
                            .then(response => response.json())
                            .then(data => {
                                alert(data.message);
                                if (data.success) location.reload();
                            });
                    });
                });
        });
    });

    // Cancel Appointment
    document.querySelectorAll(".cancel-btn").forEach(button => {
        button.addEventListener("click", () => {
            const id = button.dataset.id;
            const row = button.closest("tr");

            removeExistingModals(); // Ensure no overlapping modals

            // Dynamically insert the cancel modal just below the row
            const modal = createCancelModal(id);
            row.insertAdjacentElement("afterend", modal);

            document.getElementById("confirm-cancel-btn").addEventListener("click", () => {
                fetch(`/cancel-appointment-admin/${id}/`, {
                    method: "POST",
                    headers: {
                        "X-CSRFToken": document.querySelector("[name=csrfmiddlewaretoken]").value,
                    },
                })
                    .then(response => response.json())
                    .then(data => {
                        alert(data.message);
                        if (data.success) location.reload();
                    });
            });
        });
    });
});

// Helper function to create an Edit modal dynamically
function createEditModal(data) {
    const modal = document.createElement("tr");
    modal.classList.add("dynamic-modal");
    modal.innerHTML = `
        <td colspan="7">
            <div>
                <h3>Edit Appointment</h3>
                <form id="edit-form">
                    <input type="hidden" name="id" id="edit-id" value="${data.id}">
                    <label for="edit-name">Name:</label>
                    <input type="text" name="name" id="edit-name" value="${data.name}">
                    <label for="edit-service">Service:</label>
                    <select name="service" id="edit-service">
                        <option value="Quick Consultation" ${
                            data.service === "Quick Consultation" ? "selected" : ""
                        }>Quick Consultation</option>
                        <option value="Full Consultation" ${
                            data.service === "Full Consultation" ? "selected" : ""
                        }>Full Consultation</option>
                    </select>
                    <label for="edit-date">Date:</label>
                    <input type="date" name="date" id="edit-date" value="${data.date}">
                    <label for="edit-time">Time:</label>
                    <input type="time" name="time" id="edit-time" value="${data.time.slice(0, 5)}">
                    <button type="submit">Save</button>
                    <button type="button" onclick="removeExistingModals()">Cancel</button>
                </form>
            </div>
        </td>
    `;
    return modal;
}

// Helper function to create a Cancel modal dynamically
function createCancelModal(id) {
    const modal = document.createElement("tr");
    modal.classList.add("dynamic-modal");
    modal.innerHTML = `
        <td colspan="7">
            <div>
                <h3>Cancel Appointment</h3>
                <p>Are you sure you want to cancel this appointment?</p>
                <button id="confirm-cancel-btn">Yes</button>
                <button onclick="removeExistingModals()">No</button>
            </div>
        </td>
    `;
    return modal;
}

// Helper function to remove existing modals
function removeExistingModals() {
    document.querySelectorAll(".dynamic-modal").forEach(modal => modal.remove());
}
