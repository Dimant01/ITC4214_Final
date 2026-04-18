document.addEventListener("DOMContentLoaded", function () {

    const btn = document.querySelector("#like-btn");

    if (!btn) return;

    btn.addEventListener("click", function () {

        const bookId = this.dataset.bookId;

        fetch(`/catalog/book/${bookId}/like/`, {
            method: "POST",
            headers: {
                "X-CSRFToken": getCookie("csrftoken"),
            },
        })
        .then(res => res.json())
        .then(data => {

            const text = this.querySelector(".like-text");
            const heart = this.querySelector(".heart");
            const count = document.querySelector("#like-count");

            // update count
            count.textContent = data.likes_count;

            if (data.liked) {
                this.classList.add("liked");
                text.textContent = "Liked";
                heart.style.transform = "scale(1.3)";
            } else {
                this.classList.remove("liked");
                text.textContent = "Like";
                heart.style.transform = "scale(1)";
            }
        });

    });

    // CSRF helper
    function getCookie(name) {
        let cookieValue = null;

        if (document.cookie && document.cookie !== "") {
            const cookies = document.cookie.split(";");

            for (let cookie of cookies) {
                cookie = cookie.trim();

                if (cookie.startsWith(name + "=")) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
});