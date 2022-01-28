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
function removeNote(ele) {
  let id = ele.parentElement.id;
  let passData = { "id": id }
  fetch("js_requests/deleteNote", {
    method: "DELETE",
    body: JSON.stringify(passData),
    headers: headers
  }).then(function (response) {
    return response.json();
  }).then(function (data) {
    if (data["success"] == "true") {
      let temp = document.getElementById(id);
      temp.classList.add("scaleRemove");
      temp.addEventListener("transitionend", () => {
        temp.remove();
      });
    } else {
      console.log("Unable to remove");
    }
  })
}
function actionNote(ele) {
  // Get ID
  let id = ele.parentElement.id;
  // Remove Overlay
  addOverlay();
  title_AN.value = document.getElementById(id+"title_AN").innerText;
  desc_AN.value = document.getElementById(id + "desc_AN").innerText;
  addNoteForm.holdID = id;
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
    weekday: 'short',
    day: 'numeric',
    year: 'numeric',
    month: 'long',
    hour: 'numeric',
    minute: 'numeric',
    second: 'numeric'
  });
  let passData = { "title_AN": title_AN.value, "desc_AN": desc_AN.value, "lastUpdated": lastUpdated }
  if (addNoteForm.holdID == undefined) {
    fetch("js_requests/add_note", { method: "POST", body: JSON.stringify(passData), headers: headers })
      .then(function (response) {
        return response.json();
      })
      .then(function (data) {
        if (data["success"] == "false") {
          handleError(data);
        } else {
          // Add element
          let note = `<div class="note" id="${data["id"]}">
       <i class="fas fa-times" onclick="removeNote(this)"></i>
          <!-- main note -->
          <div class="noteContent">
            <h5 class="dateUpdated" id="${data["id"]}lastUpdated">${lastUpdated}</h5>
            <h2 class="noteTitle" id="${data["id"]}title_AN">${title_AN.value}</h2>
            <p class="noteDescription" id="${data["id"]}desc_AN">${desc_AN.value}</p>
          </div>          
          <!-- Update button -->
          <div class="update" onclick="actionNote(this)">Update</div>
        </div>`;
          notesBox.innerHTML += note;
        }
      });
  } else {
    passData["id"] = addNoteForm.holdID;
    addNoteForm.holdID = undefined;
    fetch("js_requests/updateNote", { method: "PUT", body: JSON.stringify(passData), headers: headers })
      .then(function (response) {
        return response.json();
      })
      .then(function (data) {
        console.log(data);
        if (data["success"] == "false") {
          handleError(data);
        } else {
          if (passData["title_AN"] != "") {
            document.getElementById(passData["id"] + "title_AN").innerText = passData["title_AN"];
          }
          if (passData["desc_AN"] != "") {
            document.getElementById(passData["id"] + "desc_AN").innerText = passData["desc_AN"];
          }
          if (passData["lastUpdated"] != "") {
            document.getElementById(passData["id"] + "lastUpdated").innerText = passData["lastUpdated"];
          }
        }
      });
  }
  // Remove Overlay
  remOverlay();
});
