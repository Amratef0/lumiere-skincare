document.addEventListener("DOMContentLoaded", function () {

  const form = document.getElementById("loginForm");

  if (!form) return;

  form.addEventListener("submit", function (e) {

    let valid = true;

    const email = document.getElementById("login-email");
    const password = document.getElementById("login-password");

    // reset
    document.querySelectorAll(".form-error").forEach(el => {
      el.textContent = "";
      el.classList.remove("show");
    });

    // email
    if (!email.value.trim()) {
      document.getElementById("login-email-error").textContent = "Email required";
      document.getElementById("login-email-error").classList.add("show");
      valid = false;
    }

    // password
    if (!password.value.trim()) {
      document.getElementById("login-password-error").textContent = "Password required";
      document.getElementById("login-password-error").classList.add("show");
      valid = false;
    }

    if (!valid) {
      e.preventDefault();
    }

  });

});