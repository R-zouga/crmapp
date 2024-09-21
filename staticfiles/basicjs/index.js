const messageClose = document.querySelector(".messages i");
if (messageClose) {
    messageClose.addEventListener("click", () => {
        messageClose.parentElement.classList.add("hidden");
    });
}