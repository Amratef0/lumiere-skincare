document.addEventListener("DOMContentLoaded", function () {

  const form = document.getElementById("productForm");

  if (!form) return;

  const name        = document.getElementById("pf-name");
  const category    = document.getElementById("pf-category"); // hidden
  const price       = document.getElementById("pf-price");
  const image       = document.getElementById("pf-image");
  const description = document.getElementById("pf-description");

  function showError(id, msg) {
    const err = document.getElementById(id + "-error");
    if (err) {
      err.textContent = msg;
      err.classList.add("show");
    }
  }

  function clearErrors() {
    document.querySelectorAll(".form-error").forEach(el => {
      el.textContent = "";
      el.classList.remove("show");
    });
  }

  form.addEventListener("submit", function (e) {

    clearErrors();

    let valid = true;

    if (!name.value.trim()) {
      showError("pf-name", "Name is required");
      valid = false;
    } else if (name.value.trim().length < 2) {
      showError("pf-name", "Minimum 2 characters");
      valid = false;
    }

    if (!category.value.trim()) {
      showError("pf-category", "Select or enter category");
      valid = false;
    }

    if (!price.value.trim()) {
      showError("pf-price", "Price is required");
      valid = false;
    } else if (isNaN(price.value) || Number(price.value) <= 0) {
      showError("pf-price", "Invalid price");
      valid = false;
    }

    if (!image.value.trim()) {
      showError("pf-image", "Image is required");
      valid = false;
    }

    if (!description.value.trim()) {
      showError("pf-description", "Description required");
      valid = false;
    } else if (description.value.trim().length < 10) {
      showError("pf-description", "Minimum 10 characters");
      valid = false;
    }

    // 💥 أهم سطر
    if (!valid) {
      e.preventDefault();

      const firstError = document.querySelector(".form-error.show");
      if (firstError) {
        firstError.scrollIntoView({ behavior: "smooth", block: "center" });
      }
    }

  });

});
document.addEventListener("DOMContentLoaded", function () {

  const select = document.getElementById("pf-category-select");
  const custom = document.getElementById("pf-category-custom");
  const hidden = document.getElementById("pf-category");

  select.addEventListener("change", function () {

    if (select.value === "Other") {
      custom.style.display = "block";
      hidden.value = "";
    } else {
      custom.style.display = "none";
      hidden.value = select.value;
    }

  });

  custom.addEventListener("input", function () {
    hidden.value = custom.value;
  });

});