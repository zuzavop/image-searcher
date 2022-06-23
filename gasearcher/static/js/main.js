$(function() {
	const form = document.getElementById('form');
	$(form).submit(function (ev) {
		ev.preventDefault();
		$('.alert-danger').hide();
		$('#json').hide();
	});
});