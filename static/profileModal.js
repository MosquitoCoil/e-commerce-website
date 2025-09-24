document.addEventListener("DOMContentLoaded", () => {
  const profileModal = document.getElementById("profileModal");
  const profileContent = document.getElementById("profileContent");
  const editModal = document.getElementById("editProfileModal");
  const editForm = document.getElementById("editProfileForm");

  if (profileModal && profileContent) {
    profileModal.addEventListener("show.bs.modal", () =>
      loadProfileData(profileContent)
    );
  }

  if (editForm) {
    editForm.addEventListener("submit", (e) =>
      handleProfileUpdate(e, editForm, editModal, profileModal)
    );
  }
});

// Function to load the profile data
function loadProfileData(profileContent) {
  profileContent.innerHTML = `<li class="list-group-item">Loading...</li>`;

  fetch("/client/profile/data")
    .then((res) => res.json())
    .then((data) => {
      profileContent.innerHTML = data.error
        ? `<li class="list-group-item text-danger">${data.error}</li>`
        : generateProfileHTML(data);
    })
    .catch(() => {
      profileContent.innerHTML = `<li class="list-group-item text-danger">Error loading profile</li>`;
    });
}

// Generate profile HTML
function generateProfileHTML(data) {
  return `
    <li class="list-group-item"><strong>Username:</strong> ${data.username}</li>
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
    <li class="list-group-item"><strong>Joined:</strong> ${data.created_at}</li>
  `;
}

// Handle the profile update
function handleProfileUpdate(event, editForm, editModal, profileModal) {
  event.preventDefault();

  fetch("/client/edit-profile", {
    method: "POST",
    body: new FormData(editForm),
  })
    .then((res) => res.json())
    .then((data) => {
      const message =
        data.message ||
        (data.success
          ? "Profile updated successfully!"
          : "Failed to update profile");
      const type = data.success ? "success" : "danger";
      showToast(message, type);

      if (data.success) {
        bootstrap.Modal.getInstance(editModal).hide();
        if (profileModal) {
          bootstrap.Modal.getOrCreateInstance(profileModal).show();
        }
      }
    })
    .catch((err) => {
      console.error("Error updating profile:", err);
      showToast("Error updating profile", "danger");
    });
}

// Show toast helper
function showToast(message, type = "success") {
  const toastContainer =
    document.querySelector(".toast-container") || createToastContainer();
  const toastEl = createToastElement(message, type);

  toastContainer.appendChild(toastEl);
  const toast = new bootstrap.Toast(toastEl, { delay: 3000 });
  toast.show();

  toastEl.addEventListener("hidden.bs.toast", () => {
    toastEl.remove();
  });
}

// Create toast element
function createToastElement(message, type) {
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
  return toastEl;
}

// Create toast container if missing
function createToastContainer() {
  const container = document.createElement("div");
  container.className =
    "toast-container position-fixed top-0 start-50 translate-middle-x p-3";
  container.style.zIndex = "2000"; // higher than header/navbar
  document.body.appendChild(container);
  return container;
}
