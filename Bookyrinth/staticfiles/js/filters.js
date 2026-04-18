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