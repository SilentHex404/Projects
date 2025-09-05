document.addEventListener("DOMContentLoaded", () => {
const modal = document.getElementById("flag-modal");
const openBtn = document.querySelector(".chall-info-actions button");
const closeBtn = document.getElementById("close-modal");
const flagInput = document.getElementById("flag-input");

openBtn.addEventListener("click", () => {
    modal.style.display = "flex";
});

closeBtn.addEventListener("click", () => {
    modal.style.display = "none";
});

window.addEventListener("click", (e) => {
    if (e.target === modal) {
        modal.style.display = "none";
    }
});
});
