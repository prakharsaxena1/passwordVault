// var options = { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' };
// var today = new Date();

// console.log(today.toLocaleDateString("en-US")); // 9/17/2016
// console.log(today.toLocaleDateString("en-US", options)); // Saturday, September 17, 2016

// Functions
function remOverlay() {
    overlay_ID.classList.add("hidden");
    addNoteBox_ID.classList.add("hidden");
}
function addOverlay() {
    overlay_ID.classList.remove("hidden");
    addNoteBox_ID.classList.remove("hidden");
    // Set values
    title_AN.value = "";
    desc_AN.value = "";
}

// Selectors
// for hidden
let overlay_ID = document.getElementById("overlay_ID");
let addNoteBox_ID = document.getElementById("addNoteBox_ID");
// Form
let addNoteForm = document.getElementById("addNoteForm");
// buttons
let createNoteBtn = document.getElementById("createNoteBtn");
let cancelBtn = document.getElementById("cancelBtn");
let addNoteBtn = document.getElementById("addNoteBtn");
// notesBox
let notesBox = document.getElementById("notesBox");
// Inside Overlay
let title_AN = document.getElementById("title_AN");
let desc_AN = document.getElementById("desc_AN");


// Event Listeners
createNoteBtn.addEventListener("click", addOverlay);
cancelBtn.addEventListener("click", remOverlay);
addNoteBtn.addEventListener("click", remOverlay);

addNoteForm.addEventListener("submit", function (e) {
    // Prevent reloading
    e.preventDefault();
    // Make a post request
    let lastUpdated = new Date().toLocaleDateString("en-US");
    let passData = {
        "title_AN": title_AN.value,
        "desc_AN": desc_AN.value,
        "lastUpdated": lastUpdated
    }
    fetch("js_requests/add_note", {
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
    let note = `<div class="note">
      <!-- Control buttons -->
      <div class="btns">
        <div class="update">Update</div>
        <div class="delete">Delete</div>
      </div>
      <!-- main note -->
      <div class="noteContent">
        <h5 class="dateUpdated">${lastUpdated}</h5>
        <h2 class="noteTitle">${title_AN.value}</h2>
        <p class="noteDescription">${desc_AN.value}</p>
      </div>
      <div class="btns">
        <div class="pin">pin note</div>
      </div>
    </div>`;
    notesBox.innerHTML += note;
    // Remove Overlay
    remOverlay();
});
