const utils = {
    /**
     * load help text
     */
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

    /**
     * set used cookies if cookies are enable
     * @param {number} index
     * @param {number} trying
     * @param {string} last_query
     * @param {string} [activity]
     */
    setCookies: function (index, trying, last_query, activity) {
        if (navigator.cookieEnabled) {
            document.cookie = 'index=' + index.toString();
            document.cookie = 'trying=' + trying.toString();
            if (last_query || last_query === "") document.cookie = 'last_query="' + last_query + '"';
            if (activity || activity === "") document.cookie = 'activity="' + activity + '"';
        } else {
            if (confirm(text.cookies_warning)) {
                location.reload();
            }
        }
    },

    /**
     * try to get cookies with given name
     * @param {string} name
     * @returns {null|string}
     */
    getCookie: function (name) {
        const value = `; ${document.cookie}`;
        const parts = value.split(`; ${name}=`);
        if (parts.length === 2) return parts.pop().split(';').shift();
        else return null;
    },

    /**
     * open or close window of given class
     * @param {string} className
     * @param {boolean} open
     */
    openOrCloseWindow: function (className, open) {
        let parent = document.querySelector(className);
        if (parent) {
            parent.style.display = open ? "block" : "none";
        }
    },

    /**
     * create image with given parameters
     * @param {number} id
     * @param {string} idName
     * @param {string} [className]
     * @returns {HTMLImageElement}
     */
    createImage: function (id, idName, className) {
        const img = document.createElement("img");
        img.id = idName;
        img.src = config.photosAddress + ("0000" + (id + 1)).slice(-5) + '.jpg';
        if (className) img.className = className;
        return img;
    },

    /**
     * create button with given parameters
     * @param {string} textContent
     * @param {string} [className]
     * @param {string} [idName]
     * @returns {HTMLButtonElement}
     */
    createButton: function (textContent, className, idName) {
        const button = document.createElement("button");
        button.textContent = textContent;
        if (className) button.className = className;
        if (idName) button.id = idName;
        return button;
    },

    /**
     * generate color according to given percentage
     * @param {number} per
     * @returns {string}
     */
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
