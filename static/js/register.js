document.addEventListener("DOMContentLoaded", function () {

  const form = document.getElementById("registerForm");
  if (!form) return;

  form.addEventListener("submit", function (e) {

    let valid = true;

    const name = document.getElementById("reg-name");
    const email = document.getElementById("reg-email");
    const password = document.getElementById("reg-password");
    const confirm = document.getElementById("reg-confirm");
    const terms = document.getElementById("reg-terms");

    // reset errors
    document.querySelectorAll(".form-error").forEach(el => {
      el.textContent = "";
      el.classList.remove("show");
    });

    //  Name
    if (!name.value.trim()) {
      showError("reg-name-error", "Name is required");
      valid = false;
    }

    //  Email
    const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!email.value.trim()) {
      showError("reg-email-error", "Email is required");
      valid = false;
    } else if (!emailPattern.test(email.value)) {
      showError("reg-email-error", "Invalid email format");
      valid = false;
    }

    //  Password
    if (!password.value) {
      showError("reg-password-error", "Password is required");
      valid = false;
    } else if (password.value.length < 6) {
      showError("reg-password-error", "Minimum 6 characters");
      valid = false;
    }

    // Confirm Password
    if (confirm.value !== password.value) {
      showError("reg-confirm-error", "Passwords do not match");
      valid = false;
    }

    // Terms
    if (!terms.checked) {
      showError("reg-terms-error", "You must accept terms");
      valid = false;
    }

    if (!valid) {
      e.preventDefault();
    }

  });

  // helper function
  function showError(id, message) {
    const el = document.getElementById(id);
    if (el) {
      el.textContent = message;
      el.classList.add("show");
    }
  }

});