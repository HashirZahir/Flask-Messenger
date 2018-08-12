$(document).ready(function(){
    // The connection URL has the following format:
    //     http[s]://<domain>:<port>[/<namespace>]
    var socket = io.connect('http://' + document.domain + ':' + location.port);
    socket.on('connect', function() {
        socket.emit('joined', {data: 'I\'m connected!'});
    });

    // send message from chat form to server
    function updateThread() {
        var message_text = $('#message_text').val();
        if ($.trim(message_text) == '') {
            return false;
        }
        var url = $(location).attr('href'),
        parts = url.split("/"),
        thread_id = parts[parts.length-1];

        var data = {
            message_text: message_text,
            room: thread_id,
            thread_id: thread_id
        };
        socket.emit('server-message', data);
    }

    $('#send').click(function () {
        updateThread();
    });

    $('#message_text').keypress(function(e) {
        var code = e.keyCode || e.which;
        if (code == 13) {
            updateThread();
        }
    });

    // message received from server, append <p> message to div
    socket.on('server-to-client', function(data) {
        $('#message_text').val(null);
        $('<p>' + data['author_id'] + ': ' + data['message_text'] + '</p>').appendTo($('.DivWithScroll'));
        //$('#chat').scrollTop($('#chat')[0].scrollHeight);
    });
    
    

    function leave_room() {
        socket.disconnect();
    }
});