let modal_tag = document.getElementById("create-tag-modal");

let btn_tag = document.getElementById("create-tag-btn");

let close_tag = document.getElementById("create-tag-close");

btn_tag.onclick = function() {
  modal_tag.style.display = "block";
}

close_tag.onclick = function() {
  modal_tag.style.display = "none";
}
