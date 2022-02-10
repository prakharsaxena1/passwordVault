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
function deleteThis(ele) {
    let id = ele.parentElement.id;
    let passData = { "id": id }
    fetch("js_requests/deletePassword", { method: "DELETE", body: JSON.stringify(passData), headers: headers })
        .then(function (response) {
            return response.json();
        })
        .then(function (data) {
            if (data["success"] == "true") {
                let temp = document.getElementById(id);
                temp.classList.add("slowRemove");
                temp.addEventListener("transitionend", () => {
                    temp.remove();
                });
            } else {
                console.log("Unable to remove");
            }
        });
}
function showPassword() {
    if (password.type === "password") {
        password.type = "text";
    } else {
        password.type = "password";
    }
}
function actionPassword(ele) {
    // Get ID
    let id = ele.parentElement.id;
    // Remove Overlay
    addOverlay();
    // Get data
    fetch("js_requests/getPasswordFromID", { method: "POST", body: JSON.stringify({ "id": id }), headers: headers })
        .then(function (response) {
            return response.json();
        })
        .then(function (data) {
            if (data["success"] == "true") {
                site.value = data["data"][0],
                url.value = data["data"][1],
                login.value = data["data"][2],
                password.value = data["data"][3],
                category.value = data["data"][4],
                addPassForm.holdID = data["data"][6]
            } else {
                console.log("Unable to fetch data");
            }
        });
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
let site = document.getElementById("site");
let url = document.getElementById("url");
let login = document.getElementById("login");
let password = document.getElementById("password");
let category = document.getElementById("categories");

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
        "site": site.value, "url": url.value, "login": login.value,
        "password": password.value, "category": category.value, "lastUpdated": lastUpdated
    }
    if (addPassForm.holdID == undefined) {
        fetch("js_requests/add_password", { method: "POST", body: JSON.stringify(passData), headers: headers })
            .then(function (response) {
                return response.json();
            })
            .then(function (data) {
                if (data["success"] == "false") {
                    handleError(data);
                } else {
                    // Add element
                    let card = `<div class="card" id="${data['id']}" >
                        <a href="${url.value}" target="_blank" class="cardFaceBox ${category.value}" id="${data['id']}site">${site.value}</a>
                        <div class="cardDetailsBox" onclick="actionPassword(this)">
                        <h3 class="cardDetail">Login: <span id="${data['id']}login">${login.value}</span></h3>
                        <h3 class="cardDetail cardDetailCategory">Category: <span id="${data['id']}category">${category.value}</span></h3>
                        <h3 class="cardDetail">Last Updated: <span id="${data['id']}lastUpdated">${lastUpdated}</span></h3>
                        </div>
                        <div class="deleteBtn" onclick="deleteThis(this)">Delete</div></div>`;
                    cardBox.innerHTML += card;
                }
            });
    } else {
        passData["id"] = addPassForm.holdID;
        addPassForm.holdID = undefined;
        fetch("js_requests/updatePassword", { method: "PUT", body: JSON.stringify(passData), headers: headers })
            .then(function (response) {
                return response.json();
            })
            .then(function (data) {
                if (data["success"] == "false") {
                    handleError(data);
                } else {
                    // Update element
                    if (passData["site"] != "") {
                        document.getElementById(passData["id"] + "site").innerText = passData["site"];
                    }
                    if (passData["url"] != "") {
                        document.getElementById(passData["id"] + "site").href = passData["url"];
                    }
                    if (passData["login"] != "") {
                        document.getElementById(passData["id"] + "login").innerText = passData["login"];
                    }
                    if (passData["category"] != "") {
                        document.getElementById(passData["id"] + "category").innerText = passData["category"];
                        document.getElementById(passData["id"] + "site").classList.add(passData["category"]);
                    }
                    document.getElementById(passData["id"] + "lastUpdated").innerText = passData["lastUpdated"];

                }
            });
    }
    // Remove Overlay
    remOverlay();
});
