/* Author: xdudaj02 */
let modal_note = document.getElementById("add-note-modal");

let btn_note = document.getElementById("add-note-btn");

let close_note = document.getElementById("add-note-close");

if (btn_note != null) {
  btn_note.onclick = function() {
    modal_note.style.display = "block";
  }
}

if (close_note != null) {
  close_note.onclick = function () {
    modal_note.style.display = "none";
  }
}
