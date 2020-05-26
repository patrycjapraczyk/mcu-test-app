$(document).ready(function () {
    $('#reset').bind('click', function () {
        $.ajax({
            url: "/reset",
            type: "get",
            data: {},
            success: function (response) {
                alert('Sent reset!')
            },
            error: function (xhr) {
                //Do Something to handle error
            }
        });
    });

    let get_data
        = function() {
            $.ajax({
                url: "/data",
                type: "get",
                data: {},
                success: function (response) {
                    let data_packets = JSON.parse(response);
                    $('#data_packets').empty();
                    data_packets.forEach((packet, index) => {
                        let url_more_info = Flask.url_for('more_info', {curr_data_id: packet.data_index});
                        let td_elem = "<tr onclick=\"window.location.href='" + url_more_info + "';\"\>\n" +
                            "<td class=\"small\">" + (index + 1) + ".</td>\n" +
                            "<td class=\"small\">" + packet.time + "</td>\n" +
                            "<td class=\"big\">" + '0x' + packet.complete_data + "</td>\n" +
                            "</tr>";
                        $('#data_packets').append(td_elem);
                    })
                },
                error: function (xhr) {
                    //Do Something to handle error
                }
            });
        }

    let get_err_percentage
        =  function() {
        $.ajax({
            url: "/get_correct_percentage",
            type: "get",
            data: {},
            success: function (response) {
                let percentage = response;
                let status = 'good';
                if(percentage < 90 && percentage >= 70) {
                    status = 'warning';
                } else if(percentage < 70 && percentage >= 5) {
                    status = 'attention';
                } else if(percentage < 5) {
                    status = 'offline';
                }
                $('#pointer').removeClass();
                $('#pointer').addClass(status);
                $('#pointer #status')[0].innerHTML = status;
            },
            error: function (xhr) {
                //Do Something to handle error
            }
        });
    };

    setInterval(function () {
        get_data();
        get_err_percentage();
    }, 500);
});