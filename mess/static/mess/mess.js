$(document).ready(function () {
    var ws_scheme = window.location.protocol == "https:" ? "wss" : "ws";
    socket_mess = new WebSocket(ws_scheme + '://' + window.location.host + "/mess/");
    socket_mess.onmessage = function (e) {
        if (JSON.parse(e.data).id.id_date) {
            $('#id').html('<label>ID will be held on ' + JSON.parse(e.data).id.id_date + ' at ' + JSON.parse(e.data).id.id_half +'</label>')
        }
        else {
            $('#id').html('')
        }
        var extra_details = ""
        if (JSON.parse(e.data).extra_meals != 0) {
            extra_details += "Extra meals: " + JSON.parse(e.data).extra_meals + "<br>"
        }
        if (JSON.parse(e.data).non_count != '') {
            for (i in JSON.parse(e.data).non_count) {
                extra_details += JSON.parse(e.data).non_count[i] + '<br>'
            }
        }
        $('#' + JSON.parse(e.data).half + '_details').html(
            '<div class="panel panel-primary" style="padding-top:0px">'+
            '<div class="panel-heading" style="height:50px;padding-top:1px">' +
            '<h4><b style="color:whitesmoke">' + JSON.parse(e.data).half + '</b></h4>' +
            '</div>' +
            '<div class="panel-body text-left">'+
            "<b>Meal: " + JSON.parse(e.data).dish + "</b><br>" +
            "Boarder count: " + JSON.parse(e.data).presence_count + "<br>" +
            extra_details +
            "<b>Total Meals: " + JSON.parse(e.data).total_count + "</b><br>" +
            '</div >'+
            '</div >'
        );
    }
    if (socket_mess.readyState == 0) {
        socket_mess.addEventListener('open', function (event) {
            socket_mess.send(JSON.stringify({
                'half': '1MO'
            }));
        });
    }
    else {
        if (socket_mess.readyState != 3) {
            socket_mess.send(JSON.stringify({
                'half': '1MO'
            }));
        }
        else {
            alert("WebSocket DISCONNECT");
        }
    }
    if (socket_mess.readyState == 0) {
        socket_mess.addEventListener('open', function (event) {
            socket_mess.send(JSON.stringify({
                'half': '2EV'
            }));
        });
    }
    else {
        if (socket_mess.readyState != 3) {
            socket_mess.send(JSON.stringify({
                'half': '2EV'
            }));
        }
        else {
            alert("WebSocket DISCONNECT");
        }
    }
    if (new Date().getHours() > 15)
    {
        /*$('#morning').prop('disabled', true);*/
        /*date=new Date(new Date().getFullYear()+"-"+(new Date().getMonth()+1)+"-"+(new Date().getDate()+1)).toLocaleDateString();*/
        /*exit();*/
    };
    $('.switch').change(function (e) {
        var status="";
        if($(e.target).prop("checked") == true){
        status = "on";
        }
        else
        {
        status = "off";
        /*$("#panelchange").attr("disabled","disabled")*/
        };
        $.ajax({
            type: "POST",
            url:"/mess/change/",
            data:{
                status:status,
                half:$(e.target).attr("id"),
                csrfmiddlewaretoken:document.getElementsByName('csrfmiddlewaretoken')[0].value,
            },
            success: function(data) {
                    if (data.length==3){
                        socket_mess.send(JSON.stringify({
                            'half': data
                        }));
                        if (data == '1MO' && status=='on') {
                            if ($('input[id="2EV"]').prop('checked')==false){
                                $('input[id="2EV"]').prop('checked',true)
                                $('input[id="2EV"]').change(); 
                            }
                        }
                    }
                    else{                        
                        $(e.target).prop("checked", status == 'on' ? false : true);
                        alert(data);
                    }
            },
            error: function(xhr, textStatus, errorThrown){
                alert("Please report this error: " + errorThrown + xhr.status + xhr.responseText);
            }
        });
    });
});

$(document).ready(function () {
    mysidenav.style.width = "0px";
    $('#open').click(function () {
        $(this).css("visibility", "hidden");
        if (window.screen.width < 350)
        {
            mysidenav.style.width = screen.width + "px";
        }
        else
        {
            mysidenav.style.width = "350px";
        }
    });
    $('#close').click(function () {
        mysidenav.style.width = "0px"; 
        $('#open').css("visibility", "visible");
    });
    /*$('a[data-toggle="tab"]').click(function(event) {
    // only do this if navigation is visible, otherwise you see jump in navigation while collapse() is called 
        if ($(".navbar-collapse").is(":visible") && $(".navbar-toggle").is(":visible") ) {
            $('.navbar-collapse').collapse('toggle');
        }
    });*/
});

$(document).on('submit', '#changeform', function (e) {
    e.preventDefault();
    if (new Date($(this).serializeArray()[1].value).toLocaleDateString() == new Date().toLocaleDateString()) {
        if($('input[id=' + $(this).serializeArray()[2].value + ']').prop('checked') != ($(this).serializeArray()[3].value == 'off' ? false : true)){
            $('input[id=' + $(this).serializeArray()[2].value + ']').prop('checked', $(this).serializeArray()[3].value == 'off' ? false : true)
            $('input[id=' + $(this).serializeArray()[2].value + ']').change();
        }        
    }
    else{
        $.ajax({
            type: "POST",
            url:"/mess/change/",
            data: {
                csrfmiddlewaretoken: document.getElementsByName('csrfmiddlewaretoken')[0].value,
                date: $(this).serializeArray()[1].value,
                half: $(this).serializeArray()[2].value,
                status:$(this).serializeArray()[3].value,
            },
            success: function (data) {
                alert(data);
            },
            /*complete: function (data) {
                $("#paneloff").removeAttr("disabled");
                alert(new Date(data.date) + " --" + new Date(new Date().getFullYear() + " " + (new Date().getMonth() + 1) + " " + new Date().getDate() + " 05:30:00"));
                $('#panelon').click();
                $('.panel-collapse').slideUp("slow");
            }*/
        });
    }
    $(e.target).parents('.panel-collapse').collapse('hide');
});

$(document).on('submit', '#mealform', function (e) {
    e.preventDefault();
    $.ajax({
        type: "POST",
        url: "/mess/mealdish/",
        data: {
            csrfmiddlewaretoken: document.getElementsByName('csrfmiddlewaretoken')[0].value,
            dish: $(this).serializeArray()[1].value,
            half: $(this).serializeArray()[2].value,
            date: $(this).serializeArray()[3].value
        },
        success: function (data) {
            socket_mess.send(JSON.stringify({
                'half': data
            }));
            $(e.target).parents('.panel-collapse').collapse('hide');
        },
    });
});