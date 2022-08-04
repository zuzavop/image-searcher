let selected = -1

function searching() {
    let query = document.getElementById('search_text').value;
    if(query.length > 0) {
        location.href = '?query="' + query + '"';
    }
}

function sim_search() {
    if(selected > -1) {
        location.href = '?id=' + selected;
    }
}

function show_context() {
    list_photo.forEach(function (i, index) {
        const image = document.createElement("img");
        image.id = i.toString();
        image.setAttribute('src', '../static/data/photos/' + ("0000" + (i+1)).slice(-5) + '.jpg');
        document.getElementsByClassName("context")[0].appendChild(image);
    });
}

function select(id) {
    document.getElementById(id).setAttribute("class", "unselected");
    selected = id;
    document.getElementById(id).setAttribute("class", "selected");
    show_context()
}
