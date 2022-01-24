// Selectors
let contactsBox = document.getElementById("contactsBox");
let yourEmail = document.getElementById("yourEmail");

// Forms
let addContactForm = document.getElementById("addContactForm");
let changeEmailForm = document.getElementById("changeEmailForm");

// addContactForm selectors
let name_AC = document.getElementById("name_AC");
let email_AC = document.getElementById("email_AC");

// changeEmailForm selectors
let email_CE = document.getElementById("email_CE");

// Event Listeners
addContactForm.addEventListener("submit", function (e) {
    let name = name_AC.value.charAt(0).toUpperCase() + name_AC.value.slice(1);
    // Prevent reloading
    e.preventDefault();
    // Make a post request
    let passData = {
        'cname': name,
        'cemail': email_AC.value
    }

    fetch("js_requests/addContact", {
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
            let contact = `<div class="contact">
            <h2 class="contactName">${name}</h2>
            <h2 class="contactEmail">${email_AC.value}</h2>
            </div>`;
            contactsBox.innerHTML += contact;
            name_AC.value = "";
            email_AC.value = "";
        }
    });
});

changeEmailForm.addEventListener("submit", function (e) {
    // Prevent reloading
    e.preventDefault();
    // Make a post request
    let passData = {
        "updatedEmail": email_CE.value
    }
    fetch("js_requests/changeEmail", {
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
            yourEmail.innerHTML = email_CE.value;
            email_CE.value = "";
        }
    });
    
});
