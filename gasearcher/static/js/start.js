const startMainWindow = {
    createImageTable: function() {
        const tb = document.getElementsByClassName('div-table')[0];
        for (let i = 0; i < config.lines; i++) {
            const tr = document.createElement('tr');
            tr.id = i.toString() + 'tr';
            tb.appendChild(tr);
        }
    },

    createImageBlock: function(id, values, num) {
        let div = startMainWindow.createImage(id, num);
        const buttons = document.createElement('div');
        buttons.className = "image-buttons";
        div.appendChild(buttons);
        startMainWindow.createButtons(buttons, values, id);
        return ++num;
    },

    createImage: function (id, num) {
        const div = document.createElement('td');
        div.className = 'img-div';
        document.getElementById(Math.floor(num / config.photosOnLine) + 'tr').appendChild(div);
        const image = document.createElement("img");
        div.appendChild(image);
        image.id = id.toString();
        image.setAttribute('src', config.photosAddress + ("0000" + (parseInt(id) + 1)).slice(-5) + '.jpg');
        image.addEventListener("click", function (e) {
            if (e.ctrlKey) {
                mainWindow.controlAndSend(image.id);
            } else {
                mainWindow.select(image.id);
            }
        });
        return div;
    },

    createButtons: function(buttons, values, id) {
        // create buttons with labels/classes
        let i = 1;
        for (let e in values) {
            const but = document.createElement("button");
            buttons.appendChild(but);
            if (i > 3) {
                but.className = "more-b hidden";
            }
            but.id = "b" + id;
            but.textContent = classes[values[e]];
            but.style.background = startMainWindow.percToColor(percentClass[values[e]]);
            but.addEventListener("click", function () {
                mainWindow.addText(but.textContent, but.id.slice(1));
            });
            i++;
        }
        const but = document.createElement("button");
        but.textContent = '+';
        but.className = "plus-but";
        but.addEventListener("click", function () {
            startMainWindow.popUp(buttons, but);
        });
        buttons.appendChild(but);
    },

    popUp: function(buttons, button) {
        // create button for showing more labels
        const butt = buttons.getElementsByClassName("more-b");
        for (let b of butt) {
            b.classList.toggle("hidden");
        }
        if (button.textContent === "+") {
            button.textContent = "-";
        } else {
            button.textContent = "+";
        }
    },

    createTopClasses: function(topClasses) {
        for (let c in topClasses) {
            const but = document.createElement("button");
            but.textContent = classes[parseInt(topClasses[c])];
            but.addEventListener("click", function () {
                mainWindow.addText(but.textContent);
            });
            document.getElementById("search-text").after(but);
        }
        document.getElementById("search-text").after(document.createElement('br'));
    },

    createContext: function() {
        const buttPrev = document.createElement("button");
        buttPrev.setAttribute("class", "previous cont-butt");
        buttPrev.textContent = '<';
        buttPrev.addEventListener("click", function () {
            mainWindow.showContext(parseInt(mainWindow.middle) - config.contextShift);
        });
        document.getElementsByClassName("popup-window")[0].appendChild(buttPrev);

        const buttNext = document.createElement("button");
        buttNext.setAttribute("class", "next cont-butt");
        buttNext.textContent = '>';
        buttNext.addEventListener("click", function () {
            mainWindow.showContext(parseInt(mainWindow.middle) + config.contextShift);
        });
        document.getElementsByClassName("popup-window")[0].appendChild(buttNext);
    },

    createWanted: function(fin) {
        // create image of currently search image
        const div = document.createElement("div");
        div.className = "find-img-div";
        const img = document.createElement("img");
        img.id = fin.toString() + 'r';
        img.setAttribute("class", "find-img");
        img.setAttribute('src', config.photosAddress + ("0000" + (fin + 1)).slice(-5) + '.jpg');
        div.appendChild(img);
        const button = document.createElement("button");
        button.textContent = "Next";
        button.id = "next-button";
        button.class = "bar-item";
        button.addEventListener("click", function () {
            mainWindow.nextSearch();
        });
        div.appendChild(button)
        document.getElementsByClassName("sidebar")[0].appendChild(div);
    },

    hideBarButtons: function () {
        document.getElementById('search-text').style.visibility = 'hidden';
        document.getElementById('clear').style.visibility = 'hidden';
        document.getElementById('next-button').style.visibility = 'hidden';
        document.getElementById('text-searcher').innerText = 'Next';
    },

    percToColor: function(per) {
        per = 100 - (per * config.percGrow)
        let r, g, b = 0;
        if (per < 99) {
            r = 255;
            g = Math.round((255 / 99) * per);
        } else {
            g = 255;
            r = Math.round((25500 / 99) - (255 / 99) * per);
        }
        let h = r * 0x10000 + g * 0x100 + b;
        return '#' + ('000000' + h.toString(16)).slice(-6);
    }
};
