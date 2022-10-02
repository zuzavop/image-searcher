function create_image(id, num) {
    const div = document.createElement('td');
    div.className = 'img_div';
    document.getElementById(Math.floor(num / config.photos_on_line) + 'tr').appendChild(div);
    const image = document.createElement("img");
    div.appendChild(image);
    image.id = id.toString();
    image.setAttribute('src', config.photos_address + ("0000" + (parseInt(id) + 1)).slice(-5) + '.jpg');
    image.addEventListener("click", function (e) {
        if (e.ctrlKey) {
            control_and_send(image.id);
        } else {
            select(image.id);
        }
    });
    return div;
}

function pop_up(buttons, button) {
    // create button for showing more labels
    const butt = buttons.getElementsByClassName("more_b");
    for (let b of butt) {
        b.classList.toggle("hidden");
    }
    if (button.textContent == "+") {
        button.textContent = "-";
    } else {
        button.textContent = "+";
    }
}

function create_buttons(buttons, values) {
    // create buttons with labels/classes
    let i = 1;
    for (let e in values) {
        const but = document.createElement("button");
        buttons.appendChild(but);
        if (i > 3) {
            but.className = "more_b hidden";
        }
        but.textContent = classes[values[e]];
        but.style.background = perc2color(percent_class[values[e]]);
        but.addEventListener("click", function () {
            add_text(but.textContent);
        });
        i++;
    }
    const but = document.createElement("button");
    but.textContent = '+';
    but.className = "plus_but";
    but.addEventListener("click", function () {
        pop_up(buttons, but);
    });
    buttons.appendChild(but);
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
        show_context(parseInt(middle) - config.context_shift);
    });
    document.getElementsByClassName("popup_window")[0].appendChild(butt_p);

    const butt_n = document.createElement("button");
    butt_n.setAttribute("class", "next cont_butt");
    butt_n.textContent = '>';
    butt_n.addEventListener("click", function () {
        show_context(parseInt(middle) + config.context_shift);
    });
    document.getElementsByClassName("popup_window")[0].appendChild(butt_n);
}

function create_wanted(fin) {
    // create image of currently search image
    const img = document.createElement("img");
    img.id = fin.toString() + 'r';
    img.setAttribute("class", "find_img");
    img.setAttribute('src', config.photos_address + ("0000" + (fin + 1)).slice(-5) + '.jpg');
    document.getElementsByClassName("sidebar")[0].appendChild(img);
}

function perc2color(per) {
    per = 100 - (per * config.perc_grow)
    let r, g, b = 0;
    if (per < 99) {
        r = 255;
        g = Math.round((255 / 99) * per);
    } else {
        g = 255;
        r = Math.round((25500 / 99) - (255 / 99) * per);
    }
    let h = r * 0x10000 + g * 0x100 + b * 0x1;
    return '#' + ('000000' + h.toString(16)).slice(-6);
}