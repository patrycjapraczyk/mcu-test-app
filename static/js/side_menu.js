$(document).ready( function() {
    $('#reset').bind('click', function () {
        $.ajax({
            url: "/reset",
            type: "get",
            data: {},
            success: function(response) {
                alert('Sent reset!')
            },
            error: function(xhr) {
                //Do Something to handle error
            }
        });
    });
});