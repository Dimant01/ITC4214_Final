document.addEventListener("DOMContentLoaded", () => {

    const deleteBtn = document.querySelector("#deleteBtn");
    const modal = document.querySelector("#deleteModal");
    const cancelBtn = document.querySelector("#cancelDelete");
    const confirmBtn = document.querySelector("#confirmDelete");

    const form = deleteBtn.closest("form");

    deleteBtn.onclick = () => {
        modal.style.display = "flex";
    };

    cancelBtn.onclick = () => {
        modal.style.display = "none";
    };

    confirmBtn.onclick = () => {
        form.submit();
    };

});