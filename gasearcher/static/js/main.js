$(function () {
    const form = document.getElementById('form');
    $(form).submit(function (ev) {
        ev.preventDefault();
        $('.alert-danger').hide();
        $('#json').hide();
    });
});

function searching() {
    $.ajax({
        type: "POST",
        url: "~/../../clip_searcher.py",
        data: {param: document.getElementById('search_text').innerText}
    }).done(function (o) {
        // do something
    });
}