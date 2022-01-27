// Selectors
let sharepassForm = document.getElementById("sharepassForm");
let textArea_input = document.getElementById("textArea_input");
let key = document.getElementById("key");
let contact = document.getElementById("contact");
let enc_category = document.getElementById("enc_category");
let textArea_output = document.getElementById("textArea_output");

// Event Listeners
enc_category.addEventListener("change", function () {
    if (enc_category.value == "SE") {
        key.disabled = true;
        key.style.backgroundColor = "#D3D3D3";
    } else {
        key.disabled = false;
        key.removeAttribute("style");
    }
});

sharepassForm.addEventListener("submit", function (e) {
    e.preventDefault();
    let passData = {
        "encCode": textArea_input.value,
        "encType": enc_category.value,
        "contact": contact.value
    }
    if (enc_category.value == "UE") {
        passData["key"] = key.value
    }
    fetch("", {
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
        textArea_output.value = data["data"];
    });
});
