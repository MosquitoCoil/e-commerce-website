document.addEventListener("DOMContentLoaded", () => {
  const profileModal = document.getElementById("profileModal");
  const profileContent = document.getElementById("profileContent");
  const editModal = document.getElementById("editProfileModal");
  const editForm = document.getElementById("editProfileForm");

  // Load profile data when profile modal opens
  if (profileModal && profileContent) {
    profileModal.addEventListener("show.bs.modal", () => {
      profileContent.innerHTML = `<li class="list-group-item">Loading...</li>`;
      fetch("/client/profile/data")
        .then((res) => res.json())
        .then((data) => {
          if (data.error) {
            profileContent.innerHTML = `<li class="list-group-item text-danger">${data.error}</li>`;
          } else {
            profileContent.innerHTML = `
              <li class="list-group-item"><strong>Username:</strong> ${
                data.username
              }</li>
              <li class="list-group-item"><strong>First Name:</strong> ${
                data.firstname
              }</li>
              <li class="list-group-item"><strong>Last Name:</strong> ${
                data.lastname || "N/A"
              }</li>
              <li class="list-group-item"><strong>Address:</strong> ${
                data.address || "N/A"
              }</li>
              <li class="list-group-item"><strong>Account Type:</strong> ${
                data.is_admin === "admin" ? "Admin" : "User"
              }</li>
              <li class="list-group-item"><strong>Joined:</strong> ${
                data.created_at
              }</li>
            `;
          }
        })
        .catch(() => {
          profileContent.innerHTML = `<li class="list-group-item text-danger">Error loading profile</li>`;
        });
    });
  }

  // Handle Edit Profile form submit (instead of modal open)
  if (editForm) {
    editForm.addEventListener("submit", (e) => {
      e.preventDefault();

      fetch("/client/edit-profile", {
        method: "POST",
        body: new FormData(editForm),
      })
        .then((res) => res.json())
        .then((data) => {
          if (data.success) {
            showToast(
              data.message || "Profile updated successfully!",
              "success"
            );
            bootstrap.Modal.getInstance(editModal).hide();

            // Refresh profile modal if open
            if (profileModal) {
              bootstrap.Modal.getOrCreateInstance(profileModal).show();
            }
          } else {
            showToast(data.message || "Failed to update profile", "danger");
          }
        })
        .catch((err) => {
          console.error("Error updating profile:", err);
          showToast("Error updating profile", "danger");
        });
    });
  }
});

// ✅ Show toast helper
function showToast(message, type = "success") {
  const toastContainer =
    document.querySelector(".toast-container") || createToastContainer();

  const toastEl = document.createElement("div");
  toastEl.className = `toast align-items-center text-bg-${type} border-0 mb-2`;
  toastEl.setAttribute("role", "alert");
  toastEl.setAttribute("aria-live", "assertive");
  toastEl.setAttribute("aria-atomic", "true");
  toastEl.innerHTML = `
    <div class="d-flex">
      <div class="toast-body">${message}</div>
      <button type="button" class="btn-close btn-close-white me-2 m-auto"
        data-bs-dismiss="toast" aria-label="Close"></button>
    </div>
  `;

  toastContainer.appendChild(toastEl);
  const toast = new bootstrap.Toast(toastEl, { delay: 3000 });
  toast.show();

  toastEl.addEventListener("hidden.bs.toast", () => {
    toastEl.remove();
  });
}

// ✅ Create toast container if missing
function createToastContainer() {
  const container = document.createElement("div");
  container.className =
    "toast-container position-fixed top-0 start-50 translate-middle-x p-3";
  container.style.zIndex = "2000"; // higher than header/navbar
  document.body.appendChild(container);
  return container;
}
