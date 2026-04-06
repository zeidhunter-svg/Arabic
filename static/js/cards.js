document.addEventListener("DOMContentLoaded", () => {
    const cards = document.querySelectorAll("[data-flip-card]");

    cards.forEach((card) => {
        card.addEventListener("click", (event) => {
            if (event.target.closest("a, button, input, label")) {
                return;
            }
            card.classList.toggle("is-flipped");
        });
    });
});
