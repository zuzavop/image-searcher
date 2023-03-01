const createMainWindow = {
    init: function () {
        if (!navigator.cookieEnabled) {
            if(confirm(text.cookies_warning)) {
                location.reload();
            }
        }

        // load help text
        utils.loadHelp('help-context');

        // create button in context
        if (config.shiftInContextEnabled) {
            createMainWindow.createContext();
        }

        // hide similarity searcher button if similarity search isn't enable
        if (!config.similaritySearchEnabled) {
            document.getElementById("similarity-searcher").style.display = "none";
        }

        // load last text query to searcher
        if (config.showLastQuery) {
            document.getElementById("search-text").value = mainWindow.lastQuery;
        }

        // set sending query on enter press
        document.getElementById("search-text").addEventListener("keyup", ({key}) => {
            if (key === "Enter") {
                mainWindow.searching();
            }
        });

        // allow closing popup windows with escape
        document.addEventListener("keydown", e => {
            if (e.key === "Escape" || e.key === "Esc") {
                mainWindow.closeWindow();
                mainWindow.closeHelpWindow();
            }
            if (config.similaritySearchEnabled) {
                if (e.ctrlKey && e.key === 's') {
                    mainWindow.simSearch();
                }
            }
        });
    },

    createImageTable: function () {
        const tb = document.getElementsByClassName('div-table')[0];
        if (tb) {
            for (let i = 0; i < config.lines; i++) {
                const tr = document.createElement('tr');
                tr.id = i.toString() + 'tr';
                tb.appendChild(tr);
            }
        }
    },

    createImageBlock: function (id, values, num) {
        let div = createMainWindow.createImage(id, num);
        const buttonsDiv = document.createElement('div');
        buttonsDiv.className = "image-buttons";
        div.appendChild(buttonsDiv);
        createMainWindow.createButtons(buttonsDiv, values, id);
    },

    createImage: function (id, num) {
        const div = document.createElement('td');
        div.className = 'img-div';
        document.getElementById(Math.floor(num / config.photosOnLine) + 'tr').appendChild(div);
        const image = utils.createImage(id, id.toString(), null);
        div.appendChild(image);
        image.addEventListener("click", function (e) {
            if (e.ctrlKey) {
                mainWindow.controlAndSend(image.id);
            } else {
                mainWindow.select(image.id);
            }
        });
        return div;
    },

    createButtons: function (buttonsDiv, values, id) {
        // create buttons with labels/classes
        let i = 1;
        for (let e in values) {
            const but = utils.createButton(classes[values[e]], (i > config.displayed_classes) ? "more-b hidden" : null, "b" + id);
            buttonsDiv.appendChild(but);
            but.style.background = utils.percToColor(percentClass[values[e]]);
            but.addEventListener("click", function () {
                mainWindow.addText(but.textContent, but.id.slice(1));
            });
            i++;
        }
        const but = utils.createButton('+', "plus-but");
        but.addEventListener("click", function () {
            createMainWindow.showMoreClasses(buttonsDiv, but);
        });
        buttonsDiv.appendChild(but);
    },

    showMoreClasses: function (buttonsDiv, button) {
        // create button for showing more labels
        const butt = buttonsDiv.getElementsByClassName("more-b");
        for (let b of butt) {
            b.classList.toggle("hidden");
        }
        if (button.textContent === "+") {
            button.textContent = "-";
        } else {
            button.textContent = "+";
        }
    },

    createTopClasses: function (topClasses) {
        // create buttons of most common classes in currently shown result
        for (let c in topClasses) {
            const button = utils.createButton(classes[parseInt(topClasses[c])]);
            button.addEventListener("click", function () {
                mainWindow.addText(button.textContent);
            });
            document.getElementById("search-text").after(button);
        }
        document.getElementById("search-text").after(document.createElement('br'));
    },

    createContext: function () {
        // create buttons for shifting context of image
        const buttPrev = utils.createButton('<', "previous cont-butt");
        buttPrev.addEventListener("click", function () {
            mainWindow.showContext(parseInt(mainWindow.middleId) - config.contextShift);
        });
        document.getElementsByClassName("popup-window")[0].appendChild(buttPrev);

        const buttNext = utils.createButton('>', "next cont-butt");
        buttNext.addEventListener("click", function () {
            mainWindow.showContext(parseInt(mainWindow.middleId) + config.contextShift);
        });
        document.getElementsByClassName("popup-window")[0].appendChild(buttNext);
    },

    createWanted: function (fin) {
        // create image of currently search image
        const div = document.createElement("div");
        div.className = "find-img-div";
        const img = utils.createImage(fin, fin.toString() + 'r', "find-img");
        div.appendChild(img);

        // create button for skipping currently searching image
        const button = utils.createButton("Next", "bar-item", "next-button");
        button.addEventListener("click", function () {
            mainWindow.nextSearch();
        });
        div.appendChild(button)
        document.getElementsByClassName("sidebar")[0].appendChild(div);
    },

    hideBarButtons: function () {
        // hide buttons used for search
        document.getElementById('search-text').style.visibility = 'hidden';
        document.getElementById('clear').style.visibility = 'hidden';
        document.getElementById('next-button').style.visibility = 'hidden';
        document.getElementById('text-searcher').innerText = 'Next';
    },
};

document.addEventListener('DOMContentLoaded', createMainWindow.init);
