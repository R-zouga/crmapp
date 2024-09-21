const aside = document.querySelector("aside");
const menu = document.querySelector(".bx-menu");

if (aside) {
    menu.classList.toggle("hidden");
    // console.log("good")
}


menu.addEventListener("click", () => {
    aside.classList.toggle("show_aside");
    console.log("heello");
})