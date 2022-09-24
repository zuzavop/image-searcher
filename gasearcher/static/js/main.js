let selected = -1;
let middle = -1;
let found = -1; // index of currently search image
let trying = -1; // number of trying on current image
let last_query = ""; // text of last query
const att = 3; // number of trying before next search image

function getCookie(name) {
  const value = `; ${document.cookie}`;
  const parts = value.split(`; ${name}=`);
  if (parts.length === 2) return parts.pop().split(';').shift();
}

// setting cookies and local variables about attempts
if (found == -1) {
    let co = document.cookie.split(';');
    if (co.length > 1) {
        found = parseInt(getCookie("index"));
        trying = parseInt(getCookie("trying")) + 1;
        last_query = getCookie("last_query").slice(1,-1);
    } else {
        document.cookie = 'index=0';
        document.cookie = 'trying=0';
        document.cookie = 'last_query=""';
        found = 0;
        trying = 0;
    }
}

function searching() {
    // send text query
    let query = document.getElementById('search_text').value;
    if (trying == att) {
        found++;
        document.cookie = 'index=' + found;
        document.cookie = 'trying=-1';
        document.cookie = 'last_query=""';
        location.href = '?s=0';
    } else if (query.length > 0) {
        if (trying == (att-1)) { // display alert - last search
            if (!confirm("Last search before displaying new search image...")) {
                return;
            }
        }
        document.cookie = 'trying=' + trying;
        document.cookie = 'last_query="' + query + '"';
        location.href = '?query="' + query + '"';
    }
}

function sim_search() {
    // send query for similarity search
    if (selected > -1) {
        location.href = '?id=' + selected;
    }
}

function clear_search() {
    // clear text of search
    document.getElementById('search_text').value = '';
}

function show_context(id) {
    // show images in context of database
    middle = id;
    document.getElementsByClassName("context")[0].innerHTML = '';
    let new_id;
    for (let i = -7; i < 8; i++) {
        new_id = parseInt(id) + i
        const image = document.createElement("img");
        image.id = "w" + (new_id).toString();
        image.setAttribute('src', '../static/data/sea_photos/' + ("0000" + (new_id + 1)).slice(-5) + '.jpg');
        image.addEventListener("click", function (e) {
            if(e.ctrlKey) {
                if (id == parseInt(image.id.slice(1))) control_and_send(parseInt(image.id.slice(1)));
            } else {
                select(image.id, false);
            }
        });
        document.getElementsByClassName("context")[0].appendChild(image);
    }
}

function select(id, new_c = true) {
    // select image and show it context
    if (selected != -1) {
        document.getElementById(selected).setAttribute("class", "unselected");
    }
    if (new_c & selected == id) {
        let parent = document.querySelector(".modal_parent");
        parent.style.display = "block";
        // document.getElementsByClassName('previous')[0].style.visibility = 'visible';
        // document.getElementsByClassName('next')[0].style.visibility = 'visible';
        show_context(id);
    }
    selected = id;
    document.getElementById(id).setAttribute("class", "selected");
}

function control_and_send(id) {
    console.log(id)
    // control result and if correct send query for new image
    let find_id = parseInt(document.getElementsByClassName("find_img")[0].id.slice(0, -1));
    if (id == find_id) {
        alert("Right answer. New image will be generate...")
        found++;
        document.cookie = 'index=' + found;
        document.cookie = 'trying=-1';
        document.cookie = 'last_query=""';
        location.href = '?answer=' + id;
    } else {
        alert("Wrong answer. Try again...");
    }
}

function add_text(text) {
    // add text to text search and set focus to end
    const input = document.getElementById('search_text');
    let end = input.value.length;
    if (end > 0) {
        input.value += ', ' + text;
    } else {
        input.value += text;
    }
    end = input.value.length;
    input.setSelectionRange(end, end);
    input.focus();
}

function next_search() {
    found++;
    document.cookie = 'index=' + found;
    document.cookie = 'trying=-1';
    document.cookie = 'last_query=""';
    location.href = '?s=0';
}

function close_window() {
    let parent = document.querySelector(".modal_parent");
    parent.style.display = "none";
}