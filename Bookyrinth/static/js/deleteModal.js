document.addEventListener("DOMContentLoaded", function () {

    const modal = document.querySelector("#deleteModal");
    const modalText = document.querySelector("#modal-text");
    const confirmBtn = document.querySelector("#confirmDeleteBtn");

    function openDeleteModal(bookTitle, deleteUrl) {
        modalText.innerText =
            "Are you sure you want to delete:\n\n" + bookTitle + " ?";

        confirmBtn.href = deleteUrl;

        modal.classList.add("active");
    }

    function closeDeleteModal() {
        modal.classList.remove("active");
    }

    /* =========================
       EVENT DELEGATION (ALL CLICKS)
       ========================= */
    document.addEventListener("click", function (event) {

        /* OPEN MODAL (DELETE BUTTON) */
        const deleteBtn = event.target.closest(".catalog-delete");
        if (deleteBtn) {
            event.preventDefault();
            openDeleteModal(deleteBtn.dataset.title, deleteBtn.dataset.url);
            return;
        }

        /* CLOSE MODAL (CLICK OUTSIDE MODAL BOX) */
        if (event.target.classList.contains("modal-overlay")) {
            closeDeleteModal();
            return;
        }

        /* CLOSE MODAL (CANCEL BUTTON) */
        if (event.target.closest(".modal-cancel")) {
            closeDeleteModal();
            return;
        }
    });

});