function toggleFilters() {
    const sidebar = document.querySelector("#filterSidebar");

    if (sidebar) {
        sidebar.classList.toggle("active");
    }
}

// Close when clicking outside the sidebar
document.addEventListener("click", function (event) {
    const sidebar = document.querySelector("#filterSidebar");
    const toggleButton = document.querySelector(".filter-toggle");

    if (!sidebar.classList.contains("active")) return;

    const clickedInsideSidebar = sidebar.contains(event.target);
    const clickedToggleButton = toggleButton.contains(event.target);

    if (!clickedInsideSidebar && !clickedToggleButton) {
        sidebar.classList.remove("active");
    }
});

document.addEventListener("DOMContentLoaded", function () {

    const headers = document.querySelectorAll(".filter-header");

    headers.forEach(header => {

        header.addEventListener("click", function () {

            const section = header.parentElement;
            const content = section.querySelector(".filter-content");

            section.classList.toggle("open");

            if (section.classList.contains("open")) {
                content.style.maxHeight = content.scrollHeight + "px";
            } else {
                content.style.maxHeight = null;
            }

        });

    });

});