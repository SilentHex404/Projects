document.addEventListener("DOMContentLoaded", () => {
    const overlay = document.querySelector(".overlay");
    const deleteCard = document.querySelector(".delete-team-member-card");
    const closeBtn = document.getElementById("close-btn");
    const deleteInput = document.getElementById("delete-user-id");
    const toggleButtons = document.querySelectorAll(".toggle");

    toggleButtons.forEach(button => {
        button.addEventListener("click", (e) => {
            e.preventDefault();
            const userId = button.getAttribute("data-user-id");
            deleteInput.value = userId;
            overlay.style.display = "block";
            deleteCard.style.display = "block";
        });
    });

    closeBtn.addEventListener("click", () => {
        overlay.style.display = "none";
        deleteCard.style.display = "none";
        deleteInput.value = "";
    });
});
