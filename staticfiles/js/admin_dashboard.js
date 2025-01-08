document.addEventListener("DOMContentLoaded", () => {
    // Handle View Details
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

    // Handle Edit
    document.querySelectorAll(".edit-btn").forEach(button => {
        button.addEventListener("click", () => {
            const id = button.dataset.id;

            fetch(`/get-appointment-details/${id}/`)
                .then(response => response.json())
                .then(data => {
                    document.getElementById("edit-id").value = data.id;
                    document.getElementById("edit-name").value = data.name;
                    document.getElementById("edit-service").value = data.service;
                    document.getElementById("edit-date").value = data.date;
                    document.getElementById("edit-time").value = data.time;

                    openModal("edit-modal");
                });
        });
    });

    // Submit Edit Form
    document.getElementById("edit-form").addEventListener("submit", function (event) {
        event.preventDefault();
        const id = document.getElementById("edit-id").value;

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

    // Handle Cancel
    document.querySelectorAll(".cancel-btn").forEach(button => {
        button.addEventListener("click", () => {
            const id = button.dataset.id;
            document.getElementById("confirm-cancel-btn").dataset.id = id;

            openModal("cancel-modal");
        });
    });

    document.getElementById("confirm-cancel-btn").addEventListener("click", () => {
        const id = document.getElementById("confirm-cancel-btn").dataset.id;

        fetch(`/cancel-appointment/${id}/`, {
            method: "POST",
            headers: {
                "X-CSRFToken": document.querySelector("[name=csrfmiddlewaretoken]").value,
            },
        })
            .then(response => response.json())
            .then(data => {
                alert(data.message);
                location.reload();
            });
    });
});

function openModal(modalId) {
    document.getElementById(modalId).style.display = "block";
}

function closeModal() {
    document.querySelectorAll("[id$='modal']").forEach(modal => (modal.style.display = "none"));
}
