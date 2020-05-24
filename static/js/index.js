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

    setInterval(function () {
        $.ajax({
            url: "/data",
            type: "get",
            data: {},
            success: function(response) {
                data_packets = JSON.parse(response);
                $('#data_packets').empty();
                data_packets.forEach((packet, index) => {
                    url = Flask.url_for( 'more_info',  {curr_data_id: packet.data_index});
                     td_elem =  "<tr onclick=\"window.location.href='" + url + "';\"\>\n" +
                        "<td class=\"small\">" + (index + 1) + ".</td>\n" +
                        "<td class=\"small\">" + packet.time + "</td>\n" +
                        "<td class=\"big\">"+ '0x' + packet.complete_data +"</td>\n" +
                        "</tr>";
                    $('#data_packets').append(td_elem);
                })
            },
            error: function(xhr) {
                //Do Something to handle error
            }
        });
    }, 2000);
});