// =+=+==+=+= ANIMATIONS =+=+==+=+=
// +++++++++ Variables +++++++++
// Login_box
let login_box = document.getElementById("login_box");
// register_box
let register_box = document.getElementById("register_box");
// overlay
let panel1 = document.getElementById("panel1");
let panel2 = document.getElementById("panel2");
let goto_register_button = document.getElementById("goto_register_button");
let goto_login_button = document.getElementById("goto_login_button");

// move panel up
function move_panel_up() {
    panel1.classList.add("goUp");
    panel2.classList.add("goUp");
    panel1.classList.remove("goDown");
    panel2.classList.remove("goDown");
}

// move panel down
function move_panel_down() {
    panel1.classList.add("goDown");
    panel2.classList.add("goDown");
    panel1.classList.remove("goUp");
    panel2.classList.remove("goUp");
}

// move panelBox left
function move_panelBox_left() {
    login_box.classList.add("goLeft");
    register_box.classList.add("goLeft");
    login_box.classList.remove("goRight");
    register_box.classList.remove("goRight");
}

// move panelBox right
function move_panelBox_right() {
    login_box.classList.remove("goLeft");
    register_box.classList.remove("goLeft");
    login_box.classList.add("goRight");
    register_box.classList.add("goRight");
}

// +++++++++ Event Listeners +++++++++
goto_register_button.addEventListener("click", function () {
    move_panel_up();
    move_panelBox_left();
});

goto_login_button.addEventListener("click", function () {
    move_panel_down();
    move_panelBox_right();
});

