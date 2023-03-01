const mainWindow = {
    selectedId: -1, // index of currently selected
    middleId: -1, // index of middle image in context
    found: -1, // index of currently search image
    trying: -1, // number of trying on current image
    lastQuery: "", // text of last query

    init: function () {
        // set history
        window.onpopstate = (event) => {
            mainWindow.stepBack(event.state);
        };
        history.pushState({
            index: utils.getCookie("index"),
            trying: utils.getCookie("trying"),
            last_query: utils.getCookie("last_query")
        }, '');

        // setting cookies and local variables about attempts
        document.cookie = 'activity=""';
        if (mainWindow.found === -1) {
            if (utils.getCookie("index") && utils.getCookie("trying")) {
                mainWindow.found = parseInt(utils.getCookie("index"));
                mainWindow.trying = parseInt(utils.getCookie("trying"));
                if (utils.getCookie("last_query")) {
                    mainWindow.lastQuery = utils.getCookie("last_query").slice(1, -1);
                } else {
                    document.cookie = 'last_query=""';
                    mainWindow.lastQuery = "";
                }
            } else {
                utils.setCookies(0, 0, "");
                mainWindow.found = 0;
                mainWindow.trying = 0;
            }
        }
    },

    searching: function () {
        // send text query
        let query = document.getElementById('search-text').value;
        if (mainWindow.trying === config.att) {
            utils.setCookies(mainWindow.found + 1, 0, "", "");
            location.href = '?s';
        } else if (query.length > 0) {
            if (mainWindow.trying === (config.att - 1)) { // display alert - last search
                if (!confirm(text.last_warning)) {
                    return;
                }
            }
            utils.setCookies(mainWindow.found, mainWindow.trying + 1, query);
            location.href = '?query="' + query + '"';
        }
    },

    simSearch: function () {
        // send query for similarity search
        if (mainWindow.selectedId !== -1) {
            if (mainWindow.trying === config.att) {
                utils.setCookies(mainWindow.found + 1, 0, "", "");
                location.href = '?s';
            } else {
                if (mainWindow.trying === (config.att - 1)) { // display alert - last search
                    if (!confirm(text.last_warning)) {
                        return;
                    }
                }
                utils.setCookies(mainWindow.found, mainWindow.trying + 1, "");
                location.href = '?id=' + mainWindow.selectedId;
            }
        } else {
            alert(text.similarity_warning);
        }
    },

    clearSearch: function () {
        // clear text of search
        document.getElementById('search-text').value = '';
    },

    showContext: function (id) {
        // show images in context of database
        mainWindow.middleId = id;
        document.getElementsByClassName("context")[0].innerHTML = '';
        let newId;
        for (let i of config.contextIds) {
            newId = parseInt(id) + i
            if (newId > 0 && newId < config.sizeDataset) {
                const image = utils.createImage(newId, "w" + (newId).toString(), null);
                image.addEventListener("click", function (e) {
                    if (e.ctrlKey) {
                        if (parseInt(id) === parseInt(image.id.slice(1))) mainWindow.controlAndSend(parseInt(image.id.slice(1)));
                        else alert(text.context_warning)
                    } else {
                        mainWindow.select(image.id, false);
                    }
                });
                document.getElementsByClassName("context")[0].appendChild(image);
            }
        }
    },

    select: function (id, newContext = true) {
        // select image and show it context
        if (mainWindow.selectedId !== -1) {
            document.getElementById(mainWindow.selectedId).setAttribute("class", "unselected");
        }

        if (newContext && mainWindow.selectedId === parseInt(id)) {
            let parent = document.querySelector(".modal-parent");
            if (parent) {
                parent.style.display = "block";
            }

            if (config.shiftInContextEnabled) {
                document.getElementsByClassName('previous')[0].style.visibility = 'visible';
                document.getElementsByClassName('next')[0].style.visibility = 'visible';
            }
            mainWindow.showContext(id);
        }

        mainWindow.selectedId = parseInt(id);
        document.getElementById(id).setAttribute("class", "selected");
    },

    controlAndSend: function (id) {
        // control result and if correct send query for new image
        let findId = parseInt(document.getElementsByClassName("find-img")[0].id.slice(0, -1));
        if (parseInt(id) === findId) {
            alert(text.right_answer)
            utils.setCookies(mainWindow.found + 1, 0, "", "");
            location.href = '?answer=' + id;
        } else {
            alert(text.wrong_answer);
        }
    },

    addText: function (text, id) {
        // add text to text search and set focus to end
        const input = document.getElementById('search-text');
        if (input) {
            let end = input.value.length;
            if (end > 0) {
                input.value += config.connection + text;
            } else {
                input.value += text;
            }
            end = input.value.length;
            input.setSelectionRange(end, end);
            input.focus();
            if (id) {
                const last = utils.getCookie("activity");
                document.cookie = 'activity=' + last.slice(0, -1) + text + ":" + id + '|"';
            }
        }
    },

    nextSearch: function () {
        // showing next image for search
        utils.setCookies(mainWindow.found + 1, 0, "", "");
        location.href = '?s';
    },

    closeWindow: function () {
        // closing of context window
        utils.openOrCloseWindow(".help-modal-parent", false);
    },

    closeHelpWindow: function () {
        // closing of context window
        utils.openOrCloseWindow(".help-parent", false);
    },

    stepBack: function (state) {
        console.log(state); //TODO
        // set cookies to last state
        document.cookie = 'activity=""';
        if (mainWindow.trying > 0) {
            document.cookie = 'trying=' + (mainWindow.trying - 1);
        } else {
            document.cookie = 'index=' + (mainWindow.found - 1);
        }
    },

    showHelp: function () {
        // display text of help
        utils.openOrCloseWindow(".help-parent", true);
    },
};

document.addEventListener('DOMContentLoaded', mainWindow.init);