// UI
const signUpButton = document.getElementById('m2signUp');
const signInButton = document.getElementById('m2signIn');
const container = document.getElementById('container');

// Login
let usernameIn = document.getElementById("username");
let passwordIn = document.getElementById("password");
let userfileIn = document.getElementById("userfile");
let submitIn = document.getElementById("submitIN");

// Register
let usernameUp = document.getElementById("usernameUp");
let passwordUp = document.getElementById("passwordUp");
let emailUp = document.getElementById("emailUp");
let numberUp = document.getElementById("numberUp");
let submitUp = document.getElementById("submitUP");

// Event listeners
signUpButton.addEventListener('click', () => {
    container.classList.add("right-panel-active");
});

signInButton.addEventListener('click', () => {
    container.classList.remove("right-panel-active");
});

submitIn.addEventListener('click', (e) => {
    e.preventDefault();
    console.log("login");
    // Read file
    // make key
    // make fernet object
    // try to decrypt object
    // if decryption successful then login
    // move to profile page
});

submitUp.addEventListener('click', (e) => {
    e.preventDefault();
    console.log("register");
    // get all data from form
    // make key
    // make fernet object
    // encrypt the data and store that in a file to download
    // move to profile page
    
});