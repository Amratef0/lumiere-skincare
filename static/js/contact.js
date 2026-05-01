document.addEventListener("DOMContentLoaded", function () {

    const contactForm = document.getElementById("contactForm");

    if (!contactForm) 
        return;
    
    contactForm.addEventListener("submit", function (e) {

        let valid = true;

        const name = document.getElementById("name");
        const email = document.getElementById("email");
        const message = document.getElementById("message");
        const subject = document.getElementById("subject");

        // reset
        document
            .querySelectorAll(".form-error")
            .forEach(el => {
                el.textContent = "";
                el.classList.remove("show");
            });

        if (name.value.trim().length === 0) {
            const err = document.getElementById("name-error");
            err.textContent = "Name required";
            err.classList.add("show");
            valid = false;
        }

        if (!email.value.includes("@")) {
            const err = document.getElementById("email-error");
            err.textContent = "Invalid email";
            err.classList.add("show");
            valid = false;
        }

        if (!subject.value) {
            const err = document.getElementById("subject-error");
            err.textContent = "Select a subject";
            err.classList.add("show");
            valid = false;
        }

        if (message.value.length < 20) {
            const err = document.getElementById("message-error");
            err.textContent = "Min 20 chars";
            err.classList.add("show");
            valid = false;
        }

        if (!valid) {
            e.preventDefault(); // 🔥 أهم سطر
            return ;
        }

    });

    // ========================= 🔥 CHARACTER COUNTER =========================

    const msgTextarea = document.getElementById("message");
    const charCounter = document.querySelector(".char-counter");

    if (msgTextarea && charCounter) {
        const max = 500;

        msgTextarea.addEventListener("input", () => {
            const len = msgTextarea.value.length;
            charCounter.textContent = `${len} / ${max}`;

            if (len > max * 0.9) {
                charCounter.style.color = "red";
            } else {
                charCounter.style.color = "";
            }
        });
    }

});