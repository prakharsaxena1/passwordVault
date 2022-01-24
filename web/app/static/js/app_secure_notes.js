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
  let date = new Date();
  let lastUpdated = date.toLocaleString('en-US', {
    weekday: 'short', // long, short, narrow
    day: 'numeric', // numeric, 2-digit
    year: 'numeric', // numeric, 2-digit
    month: 'long', // numeric, 2-digit, long, short, narrow
    hour: 'numeric', // numeric, 2-digit
    minute: 'numeric', // numeric, 2-digit
    second: 'numeric', // numeric, 2-digit
  });
  console.log(lastUpdated);
  let passData = {
    "title_AN": title_AN.value,
    "desc_AN": desc_AN.value,
    "lastUpdated": lastUpdated,
    "isPinned": "NP"
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
    if (data["success"] == "false") {
      handleError(data);
    } else {
      // Add element
      let note = `<div class="note">
          <!-- main note -->
          <div class="noteContent">
            <h5 class="dateUpdated">${lastUpdated}</h5>
            <h2 class="noteTitle">${title_AN.value}</h2>
            <p class="noteDescription">${desc_AN.value}</p>
          </div>          
          <!-- Update button -->
          <div class="update">Update</div>
        </div>`;
      notesBox.innerHTML += note;
    }
  });
  // Remove Overlay
  remOverlay();
});
