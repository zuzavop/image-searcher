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
    for (let i = -5; i < 6; i++) {
        const image = document.createElement("img");
        image.id = (parseInt(id) + i).toString();
        image.setAttribute('src', '../static/data/photos/' + ("0000" + (parseInt(id) + i + 1)).slice(-5) + '.jpg');
        image.addEventListener('dblclick', function () {
            control_and_send(i);
        });
        document.getElementsByClassName("context")[0].appendChild(image);
    }
}

function select(id) {
    if (selected > -1) {
        document.getElementById(selected).setAttribute("class", "unselected");
    }
    selected = id;
    document.getElementById(id).setAttribute("class", "selected");
    show_context(id)
}

function control_and_send(id) {
    let find_id = parseInt(document.getElementsByClassName("find_img")[0].id.slice(0, -1));
    if (id == find_id) {
        alert("Right answer. New image will be generate...")
        location.href = '?answer=' + id;
    } else {
        alert("Wrong answer. Try again...");
    }
}

function add_text(text) {
    if (document.getElementById('search_text').value.length > 0) {
        document.getElementById('search_text').value += ' '  + text;
    } else {
        document.getElementById('search_text').value += text;
    }

}
