const utils = {
    loadHelp: function () {
        fetch('templates/help.html')
            .then(response => response.text())
            .then(data => {
                document.getElementById('help-context').innerHTML = data;
            });
    },

    getCookie: function (name) {
        const value = `; ${document.cookie}`;
        const parts = value.split(`; ${name}=`);
        if (parts.length === 2) return parts.pop().split(';').shift();
    },

    openOrCloseWindow: function(className, open) {
        let parent = document.querySelector(className);
        if(parent) {
            parent.style.display = open ? "block" : "none";
        }
    }
};
