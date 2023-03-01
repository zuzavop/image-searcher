const welcome_page = {
    init: function () {
        // get help text
        utils.loadHelp('help-context');

        if (navigator.cookieEnabled) {
            // set cookies - TODO
            document.cookie = 'index=0';
            document.cookie = 'trying=-1; last_query=""; activity=""';
        } else {
            welcome_page.showCookiesWarning();
        }
    },

    showCookiesWarning: function () {
        const startButton = document.getElementById("start-button");
        if (startButton) {
            startButton.style.display = "none";
        }

        // show warning about cookies
        const warning = document.createElement("div");
        warning.id = "warning";
        warning.textContent = text.warning;

        document.body.appendChild(warning);
    },
};

document.addEventListener('DOMContentLoaded', welcome_page.init);