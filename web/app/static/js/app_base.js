function overlayFunction() {
    overlay_logout.classList.toggle("hidden");
}

// Selectors
let logout = document.getElementById("logout");
let overlay_logout = document.getElementById("overlay_logout");
let yesBtn = document.getElementById("yesBtn");
let noBtn = document.getElementById("noBtn");

logout.addEventListener("click", overlayFunction)
noBtn.addEventListener("click", overlayFunction)
yesBtn.addEventListener("click", function () {
    fetch("logout");
    location.href = '/account/';
})