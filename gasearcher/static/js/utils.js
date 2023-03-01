const utils = {
    // load help text
    loadHelp: function (containerName) {
        fetch('templates/help.html')
            .then(response => response.text())
            .then(data => {
                const container = document.getElementById(containerName);
                if (container) {
                    container.innerHTML = data;
                }
            });
    },

    setCookies: function (index, trying, last_query, activity) {
        if (navigator.cookieEnabled) {
            document.cookie = 'index=' + index;
            document.cookie = 'trying=' + trying;
            if (last_query || last_query === "") document.cookie = 'last_query="' + last_query + '"';
            if (activity || activity === "") document.cookie = 'activity="' + activity + '"';
        } else {
            if(confirm(text.cookies_warning)) {
                location.reload();
            }
        }
    },

    getCookie: function (name) {
        const value = `; ${document.cookie}`;
        const parts = value.split(`; ${name}=`);
        if (parts.length === 2) return parts.pop().split(';').shift();
        else return null;
    },

    openOrCloseWindow: function (className, open) {
        let parent = document.querySelector(className);
        if (parent) {
            parent.style.display = open ? "block" : "none";
        }
    },

    createImage: function (id, idName, className) {
        const img = document.createElement("img");
        img.id = idName;
        img.src = config.photosAddress + ("0000" + (parseInt(id) + 1)).slice(-5) + '.jpg';
        if (className) img.className = className;
        return img;
    },

    createButton: function (textContent, className, idName) {
        const button = document.createElement("button");
        button.textContent = textContent;
        if (className) button.className = className;
        if (idName) button.id = idName;
        return button;
    },

    percToColor: function (per) {
        per = 100 - (per * config.percGrow)
        let r, g;
        if (per < 99) {
            r = 255;
            g = Math.round((255 / 99) * per);
        } else {
            g = 255;
            r = Math.round((25500 / 99) - (255 / 99) * per);
        }
        let h = r * 0x10000 + g * 0x100;
        return '#' + ('000000' + h.toString(16)).slice(-6);
    },
};
