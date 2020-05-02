$(document).ready(function () {
    $('#settings-button').bind('click', function () {
        $('#settings').removeClass('hidden');
        $('#control-panel').addClass('hidden');
    });

    $("#close-settings, #button-ok").bind('click', function() {
        console.log('click')
        $('#settings').addClass('hidden');
        $('#control-panel').removeClass('hidden');
    });
})