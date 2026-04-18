document.addEventListener("DOMContentLoaded", function () {
    const birthInput = document.querySelector("#id_birth_date");

    if (birthInput) {
        const today = new Date();

        const yyyy = today.getFullYear();
        const mm = String(today.getMonth() + 1).padStart(2, "0");
        const dd = String(today.getDate()).padStart(2, "0");

        const maxDate = `${yyyy}-${mm}-${dd}`;

        birthInput.setAttribute("max", maxDate);
    }
});