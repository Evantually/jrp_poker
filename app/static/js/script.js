$(document).ready(function() {
    const sio = io();

    sio.on('connect', function() {
        sio.send({data: `${sio.id} connected!`});
    });

    sio.on('message', function(msg,cb) {
        $('#log').append('<br>' + $('<div/>').text('Received #' + msg.count + ': ' + msg.data).html());
        if (cb) {
            cb();
        }
    });

    sio.on('set_player_name', function(msg) {
        sio.id = msg.id;
        player = msg.player;
    });

    $('form#requestCards').submit(function(event) {
        sio.emit('player_poker_start', {
            sid: sio.id
        });
        return false;
    })

    $('form#setName').submit(function(event) {
        sio.emit('set_player_name', {
            sid: sio.id,
            username: $('#setNameData').val()
        });
        return false;
    })

    $('form#messages').submit(function(event) {
        sio.emit('message', {data: $('#message_data').val()});
        return false;
    });
});