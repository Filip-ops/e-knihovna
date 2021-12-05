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

{
    let del_tags = document.getElementsByClassName('btn-del-tag');
    for (let i = 0; i < del_tags.length; ++i) {
        del_tags[i].onmouseover = function() {
            del_tags[i].parentElement.parentElement.style.border = "1px solid black"
            del_tags[i].parentElement.parentElement.style.color = "black"
            del_tags[i].parentElement.parentElement.style.boxShadow = "-1px 0 1px indianred, -1px 1px 1px indianred, " +
                "-1px -1px 1px indianred, 1px 0 1px indianred, 1px -1px 1px indianred, 1px 1px 1px indianred, " +
                "0 -1px 1px indianred, 0 1px 1px indianred"
        };
        del_tags[i].onmouseout = function() {
            del_tags[i].parentElement.parentElement.style.border = "1px solid lightgrey"
            del_tags[i].parentElement.parentElement.style.color = "darkgrey"
            del_tags[i].parentElement.parentElement.style.boxShadow = "none"
        };
    }
}

let add_tag = document.getElementsByClassName('btn-add-tag')[0]
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
