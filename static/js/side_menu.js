$(document).ready( function() {
    console.log("here")

    $('#reset').bind('click', function () {
        console.log('click');
        window.location.href = '/reset';
    });
});