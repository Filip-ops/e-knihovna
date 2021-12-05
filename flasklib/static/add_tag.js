/* Author: xdudaj02 */
let modal_tag = document.getElementById("add-tag-modal");

let btn_tag = document.getElementById("add-tag-btn");

let close_tag = document.getElementById("add-tag-close");

btn_tag.onclick = function() {
  modal_tag.style.display = "block";
}

close_tag.onclick = function() {
  modal_tag.style.display = "none";
}
