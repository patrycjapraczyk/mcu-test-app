$("#search_form_input").keyup(function(){
    var text = $(this).val();

    $.ajax({
      url: "/suggestions",
      type: "get",
      data: {jsdata: text},
      success: function(response) {
        $("#place_for_suggestions").html(response);
      },
      error: function(xhr) {
        //Do Something to handle error
      }
    });
});