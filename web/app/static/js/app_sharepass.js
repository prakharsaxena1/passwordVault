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
    keyFilled.disabled = false;
    keyFilled.removeAttribute("style");
    encryption_category.value = "UE";
    contactSelect.value = "0";
    enc_out.value = "";
}
// Event listeners
// encryption_category
encryption_category.addEventListener("change", function () {
    if (encryption_category.value == "SE") {
        keyFilled.disabled = true;
        keyFilled.style.backgroundColor = "#D3D3D3";
    } else {
        keyFilled.disabled = false;
        keyFilled.removeAttribute("style");
    }
})
// Clear button
clearBtn.addEventListener("click", clearText);
// Share button
sharepassForm.addEventListener("submit", function (e) {
    e.preventDefault();
    let passData = {
        "text": textFilled.value,
        "method": encryption_category.value,
        "contact": contactSelect.value,
        "key": keyFilled.value
    }

    fetch("js_requests/sharePass", { method: "POST", body: JSON.stringify(passData), headers: headers })
        .then(function (response) {
            return response.json();
        }).then(function (data) {
            enc_out.value = data["msg"];
        });

    clearText();
});