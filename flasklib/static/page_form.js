/* Author: xdudaj02 */
let page_start = document.getElementById("page_start");
let page_end = document.getElementById("page_end");

page_start.oninput = function () {
    if (parseInt(page_end.value) <= parseInt(page_start.value) || page_end.value === "") {
        page_end.value = page_start.value;
    }
}

page_end.oninput = function () {
    if (parseInt(page_end.value) <= parseInt(page_start.value)) {
        page_end.value = page_start.value;
    }
}

let add_tag = document.getElementsByClassName('btn-add-tag')[0]
if (add_tag != null) {
    add_tag.onmouseover = function() {
        add_tag.parentElement.parentElement.style.border = "1px solid black"
        add_tag.parentElement.parentElement.style.color = "black"
        add_tag.parentElement.parentElement.style.boxShadow = "-1px 0 1px lightgreen, -1px 1px 1px lightgreen, " +
            "-1px -1px 1px lightgreen, 1px 0 1px lightgreen, 1px -1px 1px lightgreen, 1px 1px 1px lightgreen, " +
            "0 -1px 1px lightgreen, 0 1px 1px lightgreen"
    };
    add_tag.onmouseout = function() {
        add_tag.parentElement.parentElement.style.border = "1px solid lightgrey"
        add_tag.parentElement.parentElement.style.color = "darkgrey"
        add_tag.parentElement.parentElement.style.boxShadow = "none"
    };
}
