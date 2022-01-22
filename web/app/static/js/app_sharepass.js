// Selectors
// Form
let sharepassForm = document.getElementById("sharepassForm");
// form input
let textFilled = document.getElementById("textFilled");
let keyFilled = document.getElementById("keyFilled");
let encryption_category = document.getElementById("encryption_category");
let contactSelect = document.getElementById("contactSelect");
let enc_out = document.getElementById("enc_out");
// form buttons
let clearBtn = document.getElementById("clearBtn");
let shareBtn = document.getElementById("shareBtn");


// functions
function clearText() {
    textFilled.value = "";
    keyFilled.value = "";
    encryption_category.value = "SE";
    contactSelect.value = "0";
    enc_out.value = "";
}
// Event listeners
// Clear button
clearBtn.addEventListener("click", clearText);
// Share button
shareBtn.addEventListener("click", function (e) {
    e.preventDefault();
    let passData = {
        "text": textFilled.value,
        "method": encryption_category.value,
        "key": keyFilled.value
    }
    console.log(passData);
    fetch("js_requests/sharePass", {
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
        console.log(data["msg"]);
    });

    clearText();
});