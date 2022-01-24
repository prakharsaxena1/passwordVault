function overlayFunction() {
    overlay_logout.classList.toggle("hidden");
}

function handleError(data) {
    let errorBox = `<div class="errorBox">
          <div class="errMsg"><i class="fas fa-exclamation-triangle"></i>${data["msgT"]}</div>
          <p class="errMsgDesc">${data["msgD"]}</p>
          <div id="okBtn" onclick="toggleErrorBox()">Ok</div>
        </div>`
    errorOverlay.innerHTML = errorBox;
    errorOverlay.classList.toggle("hidden");
}

// Selectors
let logout = document.getElementById("logout");
let overlay_logout = document.getElementById("overlay_logout");
let yesBtn = document.getElementById("yesBtn");
let noBtn = document.getElementById("noBtn");
// error overlay
let errorOverlay = document.getElementById("errorOverlay");
let okBtn = document.getElementById("okBtn");

logout.addEventListener("click", overlayFunction);
noBtn.addEventListener("click", overlayFunction);
yesBtn.addEventListener("click", function () {
    fetch("logout");
    location.href = '/account/';
});

function toggleErrorBox() {
    errorOverlay.classList.toggle("hidden");
};