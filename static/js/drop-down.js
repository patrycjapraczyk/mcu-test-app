$(document).ready( function() {
    $('.drop-down-select').each(function () {
            $(this).append("<div class='select-selected'>"
                + $(this).find('select option:selected').text()
                + "</div>")
        }
    );

    $('.drop-down-select').append(
        "<div class='select-items select-hide'></div>"
    );

    $('option').each(
        (i, option) => {
            $(option).closest('.drop-down-select').find('.select-items').append('<div>' + option.innerHTML + '</div>');
        });


    $('.select-items').remove('option');

    var closeAllSelect = function () {
        $('.select-selected').removeClass('open');
        $('.select-selected').removeClass('select-arrow-active');
        $('.select-items').addClass('select-hide');
    };

    $('.select-items').children('div').on("click", function (e) {
        $(this).closest('.drop-down-select').find('.select-selected').text(this.innerHTML);
        $(this).closest('.drop-down-select').find('select').find("option[value='"+this.innerHTML+"']").attr('selected', 'selected')
        closeAllSelect();
    });

    $('.select-selected').on("click", function (e) {
        e.stopPropagation();
        $(this).toggleClass('select-arrow-active');
        $(this).toggleClass('open');
        $(this).closest('.drop-down-select').find('.select-items').toggleClass('select-hide');
    });

    $(document).on("click", closeAllSelect);
});