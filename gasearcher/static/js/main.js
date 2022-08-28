let selected = -1
let middle = -1
let found = -1
let trying = -1

if (found == -1) {
    let co = document.cookie.split(';');
    console.log(co);
    if (co.length > 1) {
        found = parseInt(co[1].split('=')[1]);
        // trying = parseInt(co[1].split('=')[2]) + 1;
    } else {
        document.cookie = 'index=' + 0;
        found = 0;
        trying = 0;
    }
}

function searching() {
    // send text query
    let query = document.getElementById('search_text').value;
    if (query.length > 0) {
        location.href = '?query="' + query + '"&found=' + found;
    }
}

function sim_search() {
    // send query for similarity search
    if (selected > -1) {
        location.href = '?id=' + selected + '&found' + found;
    }
}

function show_context(id) {
    // show images in context of database
    middle = id;
    document.getElementsByClassName("context")[0].innerHTML = '';
    for (let i = -5; i < 6; i++) {
        const image = document.createElement("img");
        image.id = (parseInt(id) + i).toString();
        image.setAttribute('src', '../static/data/photos/' + ("0000" + (parseInt(id) + i + 1)).slice(-5) + '.jpg');
        image.addEventListener('dblclick', function () {
            control_and_send(image.id);
        });
        image.addEventListener("click", function () {
            select(image.id, false);
        });
        document.getElementsByClassName("context")[0].appendChild(image);
    }
}

function select(id, new_c = false) {
    // select image and show it context
    if (selected > -1) {
        document.getElementById(selected).setAttribute("class", "unselected");
        // todo - selecting on context
    }
    selected = id;
    document.getElementById(id).setAttribute("class", "selected");
    if (new_c) {
        document.getElementsByClassName('previous')[0].style.visibility = 'visible';
        document.getElementsByClassName('next')[0].style.visibility = 'visible';
        show_context(id);
    }
}

function control_and_send(id) {
    // control result and if correct send query for new image
    let find_id = parseInt(document.getElementsByClassName("find_img")[0].id.slice(0, -1));
    if (id == find_id) {
        alert("Right answer. New image will be generate...")
        found++;
        document.cookie = 'index=' + found;
        location.href = '?answer=' + id + '&found=' + found;
    } else {
        alert("Wrong answer. Try again...");
    }
}

function add_text(text) {
    // add text to text search and set focus to end
    const input = document.getElementById('search_text');
    let end = input.value.length;
    if (end > 0) {
        input.value += ' ' + text;
    } else {
        input.value += text;
    }
    end = input.value.length;
    input.setSelectionRange(end, end);
    input.focus();
}
