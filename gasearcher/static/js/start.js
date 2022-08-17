function create_image(id, num) {
    const div = document.createElement('td');
    div.className = 'img_div';
    document.getElementById(Math.floor(num / 12) + 'tr').appendChild(div);
    const image = document.createElement("img");
    div.appendChild(image);
    image.id = id.toString();
    image.setAttribute('src', '../static/data/photos/' + ("0000" + (parseInt(id) + 1)).slice(-5) + '.jpg');
    image.addEventListener("click", function () {
        select(image.id);
    });
    image.addEventListener('dblclick', function () {
        control_and_send(image.id);
    });
    return div;
}

function create_buttons(buttons, values) {
    for (let e in values) {
        const but = document.createElement("button");
        buttons.appendChild(but);
        but.textContent = classes[values[e]];
        but.addEventListener("click", function () {
            add_text(but.textContent);
        });
    }
}

function create_top_classes(top_classes) {
    for (let c in top_classes) {
        const but = document.createElement("button");
        but.textContent = classes[parseInt(top_classes[c])];
        but.addEventListener("click", function () {
            add_text(but.textContent);
        });
        document.getElementById("search_text").after(but);
    }
    document.getElementById("search_text").after(document.createElement('br'));
}

function create_context() {
    const butt_p = document.createElement("button");
    butt_p.setAttribute("class", "previous cont_butt");
    butt_p.textContent = '<';
    butt_p.addEventListener("click", function () {
        show_context(parseInt(middle) - 1);
    });
    document.getElementsByClassName("right")[0].appendChild(butt_p);

    const butt_n = document.createElement("button");
    butt_n.setAttribute("class", "next cont_butt");
    butt_n.textContent = '>';
    butt_n.addEventListener("click", function () {
        show_context(parseInt(middle) + 1);
    });
    document.getElementsByClassName("right")[0].appendChild(butt_n);
}

function create_wanted(fin) {
    const img = document.createElement("img");
    img.id = fin.toString() + 'r';
    img.setAttribute("class", "find_img");
    img.setAttribute('src', '../static/data/photos/' + ("0000" + (fin + 1)).slice(-5) + '.jpg');
    document.getElementsByClassName("sidebar")[0].appendChild(img);
}