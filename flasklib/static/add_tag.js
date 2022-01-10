/* Author: xdudaj02 */
let modal_tag = document.getElementById("add-tag-modal");

let btn_tag = document.getElementById("add-tag-btn");

let close_tag = document.getElementById("add-tag-close");

if (btn_tag != null) {
  btn_tag.onclick = function () {
    modal_tag.style.display = "block";
  };
}
if (close_tag != null) {
  close_tag.onclick = function () {
    modal_tag.style.display = "none";
  };
}
