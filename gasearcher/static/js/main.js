const mainWindow = {
    selected: -1,
    middle: -1,
    found: -1, // index of currently search image
    trying: -1, // number of trying on current image
    lastQuery: "", // text of last query

    getCookie: function(name) {
        const value = `; ${document.cookie}`;
        const parts = value.split(`; ${name}=`);
        if (parts.length === 2) return parts.pop().split(';').shift();
    },

    init: function () {
        if(config.listingContext) {
            startMainWindow.createContext();
        }

        document.getElementById("search-text").addEventListener("keyup", ({key}) => {
            if (key === "Enter") {
                mainWindow.searching();
            }
        });

        // load last text query to searcher
        if (config.showLastQuery) {
            document.getElementById("search-text").value = mainWindow.lastQuery;
        }

        // close popup window with escape
        document.onkeydown = function(event) {
            event = event || window.event;
            let isEscape;
            if ("key" in event) {
                isEscape = (event.key === "Escape" || event.key === "Esc");
            } else {
                isEscape = (event.keyCode === 27);
            }
            if (isEscape) {
                mainWindow.closeWindow();
                mainWindow.closeHelpWindow();
            }
        };

        // set history
        window.onpopstate = (event) => {
            mainWindow.stepBack(event.state);
        };
        history.pushState({ index: mainWindow.getCookie("index"), trying: mainWindow.getCookie("trying"), last_query: mainWindow.getCookie("last_query")}, '');

        document.cookie = 'activity=""';
        // setting cookies and local variables about attempts
        if (mainWindow.found === -1) {
            let co = document.cookie.split(';');
            if (co.length > 1) {
                mainWindow.found = parseInt(mainWindow.getCookie("index"));
                mainWindow.trying = parseInt(mainWindow.getCookie("trying")) + 1;
                mainWindow.lastQuery = mainWindow.getCookie("last_query").slice(1, -1);
            } else {
                document.cookie = 'index=0; trying=0; last_query=""';
                mainWindow.found = 0;
                mainWindow.trying = 0;
            }
        }
    },

    searching: function() {
        // send text query
        let query = document.getElementById('search-text').value;
        if (mainWindow.trying === config.att) {
            mainWindow.found++;
            document.cookie = 'index=' + mainWindow.found + '; trying=-1; last_query=""; activity=""';
            location.href = '?s';
        } else if (query.length > 0) {
            if (mainWindow.trying === (config.att - 1)) { // display alert - last search
                if (!confirm(text.last_warning)) {
                    return;
                }
            }
            document.cookie = 'trying=' + mainWindow.trying + '; last_query="' + query + '"';
            location.href = '?query="' + query + '"';
        }
    },

    simSearch: function() {
        // send query for similarity search
        if (mainWindow.selected !== -1) {
            if (mainWindow.trying === config.att) {
                mainWindow.found++;
                document.cookie = 'index=' + mainWindow.found + '; trying=-1; last_query=""; activity=""';
                location.href = '?s';
            } else {
                if (mainWindow.trying === (config.att - 1)) { // display alert - last search
                    if (!confirm(text.last_warning)) {
                        return;
                    }
                }
                document.cookie = 'trying=' + mainWindow.trying + '; last_query=""';
                location.href = '?id=' + mainWindow.selected;
            }
        } else {
            alert(text.similarity_warning);
        }
    },

    clearSearch: function() {
        // clear text of search
        document.getElementById('search-text').value = '';
    },

    showContext: function(id) {
        // show images in context of database
        mainWindow.middle = id;
        document.getElementsByClassName("context")[0].innerHTML = '';
        let newId;
        for (let i of [-2, -1, 0, 1, 2]) {
            newId = parseInt(id) + i
            if (newId > 0 && newId < config.sizeDataset) {
                const image = document.createElement("img");
                image.id = "w" + (newId).toString();
                image.setAttribute('src', config.photosAddress + ("0000" + (newId + 1)).slice(-5) + '.jpg');
                image.addEventListener("click", function (e) {
                    if (e.ctrlKey) {
                        if (id == image.id.slice(1)) mainWindow.controlAndSend(parseInt(image.id.slice(1)));
                        else alert(text.context_warning)
                    } else {
                        mainWindow.select(image.id, false);
                    }
                });
                document.getElementsByClassName("context")[0].appendChild(image);
            }
        }
    },

    select: function(id, newContext = true) {
        // select image and show it context
        if (mainWindow.selected != -1) {
            document.getElementById(mainWindow.selected).setAttribute("class", "unselected");
        }
        if (newContext && mainWindow.selected == id) {
            let parent = document.querySelector(".modal-parent");
            parent.style.display = "block";
            if(config.listingContext) {
                document.getElementsByClassName('previous')[0].style.visibility = 'visible';
                document.getElementsByClassName('next')[0].style.visibility = 'visible';
            }
            mainWindow.showContext(id);
        }
        mainWindow.selected = id;
        document.getElementById(id).setAttribute("class", "selected");
    },

    controlAndSend: function(id) {
        // control result and if correct send query for new image
        let findId = document.getElementsByClassName("find-img")[0].id.slice(0, -1);
        if (id == findId) {
            alert(text.right_answer)
            mainWindow.found++;
            document.cookie = 'index=' + mainWindow.found + '; trying=-1; last_query=""; activity=""';
            location.href = '?answer=' + id;
        } else {
            alert(text.wrong_answer);
        }
    },

    addText: function(text, id) {
        // add text to text search and set focus to end
        const input = document.getElementById('search-text');
        let end = input.value.length;
        if (end > 0) {
            input.value += config.connection + text;
        } else {
            input.value += text;
        }
        end = input.value.length;
        input.setSelectionRange(end, end);
        input.focus();
        const last = mainWindow.getCookie("activity");
        document.cookie = 'activity=' + last.slice(0, last.length - 1) + text + ":" + id + '|"';
    },

    nextSearch: function() {
        // showing next image for search
        mainWindow.found++;
        document.cookie = 'index=' + mainWindow.found + '; trying=-1; last_query=""; activity=""';
        location.href = '?s';
    },

    closeWindow: function() {
        // closing of context window
        let parent = document.querySelector(".modal-parent");
        parent.style.display = "none";
    },

    closeHelpWindow: function() {
        // closing of context window
        let parent = document.querySelector(".help-parent");
        parent.style.display = "none";
    },

    stepBack: function(state) {
        // set cookies to last state
        document.cookie = 'activity=""';
        if (mainWindow.trying > 0){
            document.cookie = 'trying=' + (mainWindow.trying - 1);
        } else {
            document.cookie = 'index=' + (mainWindow.found - 1);
        }
    },

    showHelp: function() {
        // display text of help
        let parent = document.querySelector(".help-parent");
        parent.style.display = "block";
    },
};

document.addEventListener('DOMContentLoaded', mainWindow.init);