document.addEventListener("DOMContentLoaded", function () {
    const menu = document.querySelector(".burger-menu");
    const button = document.querySelector(".burger-button");

    button.addEventListener("click", function () {
        menu.classList.toggle("active");
    });

    document.addEventListener("click", function (e) {
        if (!menu.contains(e.target)) {
            menu.classList.remove("active");
        }
    });
});