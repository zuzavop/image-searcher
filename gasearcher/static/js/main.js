let selected = -1
let middle = -1

function searching() {
    // send text query
    let query = document.getElementById('search_text').value;
    if (query.length > 0) {
        location.href = '?query="' + query + '"';
    }
}

function sim_search() {
    // send query for similarity search
    if (selected > -1) {
        location.href = '?id=' + selected;
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
        location.href = '?answer=' + id;
    } else {
        alert("Wrong answer. Try again...");
    }
}

function add_text(text) {
    // add text to text search and set focus to end
    const input = document.getElementById('search_text');
    const end = input.value.length;
    if (end > 0) {
        input.value += ' ' + text;
    } else {
        input.value += text;
    }
    input.setSelectionRange(end, end);
    input.focus();
}
