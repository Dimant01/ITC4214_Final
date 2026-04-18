document.addEventListener("DOMContentLoaded", function () {

    const buttons = document.querySelectorAll(".carousel-btn");

    buttons.forEach(btn => {
        btn.addEventListener("click", () => {

            const targetId = btn.dataset.target;
            const track = document.getElementById(targetId);

            const scrollAmount = track.offsetWidth * 0.6;

            if (btn.classList.contains("left")) {
                track.scrollBy({ left: -scrollAmount, behavior: "smooth" });
            } else {
                track.scrollBy({ left: scrollAmount, behavior: "smooth" });
            }
        });
    });

});