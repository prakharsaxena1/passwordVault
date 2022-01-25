// Range
let myRange = document.getElementById("myRange");
let lengthValue = document.getElementById("lengthValue");
lengthValue.innerHTML = myRange.value;
myRange.oninput = function () {
    lengthValue.innerHTML = this.value;
}

// Buttons
let resetBtn = document.getElementById("resetBtn");
let generateBtn = document.getElementById("generateBtn");
// Settings Input
let symbols = document.getElementById("symbols");
let numbers = document.getElementById("numbers");
let symbolCase = document.getElementById("symbolCase");
// Set password
let setPass = document.getElementById("setPass");

generateBtn.addEventListener("click", function () {
    let str = "";
    symbols.checked ? str += "Y" : str += "N";
    numbers.checked ? str += "Y" : str += "N";
    symbolCase.checked ? str += "Y" : str += "N";
    let passData = {
        "settings": str,
        "length": myRange.value
    }

    fetch("js_requests/getPassword", {
        method: "POST",
        body: JSON.stringify(passData),
        headers: headers
    }).then(function (response) {
        return response.json();
    }).then(function (data) {
        console.log(data);
        setPass.innerHTML = data["password"];
    })
});

resetBtn.addEventListener("click", function () {
    symbols.checked = false;
    numbers.checked = false;
    symbolCase.checked = false;
    myRange.value = 16;
});
