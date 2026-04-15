document.addEventListener("DOMContentLoaded", function () {
    const cardDetails = document.querySelector("#card-details");
    const radios = document.querySelectorAll('input[name="payment_method"]');

    function toggleCard() {
        const selected = document.querySelector('input[name="payment_method"]:checked');
        cardDetails.style.display = (selected && selected.value === "card") ? "block" : "none";
    }

    radios.forEach(r => r.addEventListener("change", toggleCard));
    toggleCard();
});