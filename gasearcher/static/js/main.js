let selected = -1

function searching() {
    let query = document.getElementById('search_text').value;
    if (query.length > 0) {
        location.href = '?query="' + query + '"';
    }
}

function sim_search() {
    if (selected > -1) {
        location.href = '?id=' + selected;
    }
}

function show_context(id) {
    document.getElementsByClassName("context")[0].innerHTML = '';
    for (let i = -5; i < 4; i++) {
        const image = document.createElement("img");
        image.id = (id + i).toString();
        image.setAttribute('src', '../static/data/photos/' + ("0000" + (id + 1 + i)).slice(-5) + '.jpg');
        document.getElementsByClassName("context")[0].appendChild(image);
    }
}

function select(id) {
    if (selected > -1) {
        document.getElementById(selected).setAttribute("class", "unselected");
    }
    selected = id;
    document.getElementById(id).setAttribute("class", "selected");
    show_context(document.getElementById(id).id)
}

function control_and_send(id) {
    let find_id = parseInt(document.getElementsByClassName("find_img")[0].id.slice(0, -1));
    if (id == find_id) {
        location.href = '?answer=' + id;
    }
}

function add_text(text) {
    document.getElementById('search_text').value += ' ' + text;
}
