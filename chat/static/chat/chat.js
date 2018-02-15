$(document).ready(function () {
    var scrolling = false;
    var chatlist = document.getElementById('box1');
    var ws_scheme = window.location.protocol == "https:" ? "wss" : "ws";
    socket_chat = new WebSocket(ws_scheme + '://' + window.location.host + "/chat/");
    socket_chat.onmessage = function (e) {
        if (chatlist.scrollTop + $("#box1").height() == chatlist.scrollHeight) {
            scrolling = false;
        }
        else {
            scrolling = true;
        }
        if (JSON.parse(e.data)[0].chat_datetime) {
            $('#box').append(
                '<label style="background-color:black;color:white;margin-top:10px;padding-left:5px;padding-right:5px">' + JSON.parse(e.data)[0].chat_datetime +'</label>'
            )
        }
        if (JSON.parse(e.data)[0].username == $('#chatbox').attr('username')) 
        {
            $('#box').append(
                '<div style="margin-right:-20px">' +
                '<div>' +
                '<span class="ms" ></span>' +
                '<div class="mac" style="word-wrap:break-word">' +
                '<div style="height:50px">' +
                '<img src="' + JSON.parse(e.data)[0].dp + '" style="width:50px;height:50px;margin-top:0px;right:5px;position:absolute" class="img-circle" alt="vc">' +
                '</div>' +
                '<small style="position:absolute; top:0px;right:55px">' + JSON.parse(e.data)[0].name + '</small>' +
                '<small  style="position:absolute;bottom:0px;right:55px">' + JSON.parse(e.data)[0].time + '</small>' +
                '<label style="margin-top:9px;margin-bottom:9px;position:relative;width:230px;text-align:left;margin-left:5px">' + JSON.parse(e.data)[0].message + '</label>' +
                '</div>' +
                '</div>' +
                '</div>'
            );
            chatlist.scrollTop = chatlist.scrollHeight;
        }
        else {
            $('#box').append(
                '<div style="margin-left:-20px">' +
                '<div><span class="msj"></span>' +
                '<div class="macro" style="word-wrap:break-word">' +
                '<small style="float:right;position:absolute;top:0px;right:5px">' + JSON.parse(e.data)[0].name + '</small>' +
                '<small style="float:right;position:absolute;bottom:0px;right:5px">' + JSON.parse(e.data)[0].time + '</small>' +
                '<img src="' + JSON.parse(e.data)[0].dp + '" style="width:50px;height:50px;margin-top:0px;position:relative" class="img-circle" alt="vc">' +
                '<label style="margin-top:9px;margin-bottom:9px;position:relative;width:230px;text-align:left;margin-left:5px">' + JSON.parse(e.data)[0].message + '</label>' +
                '</div>' +
                '</div>' +
                '</div>'
            );
            if (!scrolling) {
                chatlist.scrollTop = chatlist.scrollHeight;
            }
        }

    }

    $('#box1').load("/chat/index/" + ' #box', function () {
        chatlist.scrollTop = chatlist.scrollHeight;
    });

    $('#open').click(function () {
        chatlist.scrollTop = chatlist.scrollHeight;
    });

    $(document).on('submit', '#chatform', function (e) {
        e.preventDefault();
        if ($('#chatbox').attr('username')) {

            if ($('#chatbox').val().trim() != '') {
                if (socket_chat.readyState == 0) {
                    socket_chat.addEventListener('open', function (event) {
                        socket_chat.send(JSON.stringify({
                            'username': $('#chatbox').attr('username'),
                            'message': $('#chatbox').val()
                        }));
                    });
                }
                else {
                    if (socket_chat.readyState != 3) {
                        socket_chat.send(JSON.stringify({
                            'username': $('#chatbox').attr('username'),
                            'message': $('#chatbox').val()
                        }));
                        $('#chatbox').val('');
                    }
                    else {
                        alert("WebSocket DISCONNECT");
                    }
                }
            }
        }
        else {
            alert("Login required");
        }
    });
});