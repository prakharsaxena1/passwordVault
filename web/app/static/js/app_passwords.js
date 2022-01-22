// Functions
function remOverlay() {
    overlay_ID.classList.add("hidden");
    addBox_ID.classList.add("hidden");
}
function addOverlay() {
    overlay_ID.classList.remove("hidden");
    addBox_ID.classList.remove("hidden");
    // Set values
    site.value = "";
    url.value = "";
    login.value = "";
    password.value = "";
    category.value = "other";
}

// Selectors
// for hidden
let overlay_ID = document.getElementById("overlay_ID");
let addBox_ID = document.getElementById("addBox_ID");
// buttons
let addBtn = document.getElementById("addBtn");
let cancelBtn = document.getElementById("cancelBtn");
let saveBtn = document.getElementById("saveBtn");
// Form
let addPassForm = document.getElementById("addPassForm");
// cardBox
let cardBox = document.getElementById("cardBox");
// Inside Overlay
let site = document.getElementsByName("site")[0];
let url = document.getElementsByName("url")[0];
let login = document.getElementsByName("login")[0];
let password = document.getElementsByName("password")[0];
let category = document.getElementsByName("category")[0];


// Event Listeners
cancelBtn.addEventListener("click", remOverlay);
saveBtn.addEventListener("click", remOverlay);
addBtn.addEventListener("click", addOverlay);

addPassForm.addEventListener("submit", function (e) {
    // Prevent reloading
    e.preventDefault();
    // Make a post request
    let lastUpdated = new Date().toString().slice(0, 21);
    let passData = {
        "site": site.value,
        "url": url.value,
        "login": login.value,
        "password": password.value,
        "category": category.value,
        "lastUpdated": lastUpdated
    }    
    fetch("js_requests/add_password", {
        method: "POST",
        body: JSON.stringify(passData),
        headers: {
            "X-CSRFToken": document.getElementsByName("csrfmiddlewaretoken")[0].value,
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
    }).then(function (response) {
        return response.json();
    }).then(function (data) {
        console.log(data);
    });
    // Add element
    let card = `<div class="card">
    <a href="${url.value}" target="_blank" class="cardFaceBox ${category.value}">${site.value}</a>
    <div class="cardDetailsBox">
    <h3 class="cardDetail">Login: ${login.value}</h3>
    <h3 class="cardDetail">Category: ${category.value}</h3>
    <h3 class="cardDetail">Last Updated: ${lastUpdated}</h3>
    </div>
    </div>`;
    cardBox.innerHTML += card;
    // Remove Overlay
    remOverlay();
});
