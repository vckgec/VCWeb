$(document).ready(function () {
    var ws_scheme = window.location.protocol == "https:" ? "wss" : "ws";
    socket_mess = new WebSocket(ws_scheme + '://' + window.location.host + "/mess/");
    socket_mess.onmessage = function (e) {
        if (JSON.parse(e.data)[0].id.id_date) {
            $('#id').html('<label>ID will be held on ' + JSON.parse(e.data)[0].id.id_date + ' at ' + JSON.parse(e.data)[0].id.id_half +'</label>')
        }
        else {
            $('#id').html('')
        }
        var extra_details = ""
        if (JSON.parse(e.data)[0].extra_meals != 0) {
            extra_details += "Extra meals: " + JSON.parse(e.data)[0].extra_meals + "<br>"
        }
        if (JSON.parse(e.data)[0].non_count != '') {
            for (i in JSON.parse(e.data)[0].non_count) {
                extra_details += JSON.parse(e.data)[0].non_count[i] + '<br>'
            }
        }
        $('#' + JSON.parse(e.data)[0].meal_half + '_details').html(
            '<div class="panel panel-primary" style="padding-top:0px">'+
            '<div class="panel-heading" style="height:50px;padding-top:1px">' +
            '<h4><b style="color:whitesmoke">' + JSON.parse(e.data)[0].meal_half + '</b></h4>' +
            '</div>' +
            '<div class="panel-body text-left">'+
            "<b>Meal: " + JSON.parse(e.data)[0].meal_dishes + "</b><br>" +
            "Boarder count: " + JSON.parse(e.data)[0].boarder_count + "<br>" +
            extra_details +
            "<b>Total Meals: " + JSON.parse(e.data)[0].total_count + "</b><br>" +
            '</div >'+
            '</div >'
        );
    }
    if (socket_mess.readyState == 0) {
        socket_mess.addEventListener('open', function (event) {
            socket_mess.send(JSON.stringify({
                'half': 'MO'
            }));
        });
    }
    else {
        if (socket_mess.readyState != 3) {
            socket_mess.send(JSON.stringify({
                'half': 'MO'
            }));
        }
        else {
            alert("WebSocket DISCONNECT");
        }
    }
    if (socket_mess.readyState == 0) {
        socket_mess.addEventListener('open', function (event) {
            socket_mess.send(JSON.stringify({
                'half': 'EV'
            }));
        });
    }
    else {
        if (socket_mess.readyState != 3) {
            socket_mess.send(JSON.stringify({
                'half': 'EV'
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
        status = "True";
        }
        else
        {
        status = "False";
        /*$("#panelchange").attr("disabled","disabled")*/
        };
        $.ajax({
            type: "POST",
            url:"/mess/change/",
            data:{
            username:$(e.target).attr("data-catid"),
                status:status,
                half:$(e.target).attr("id"),
                csrfmiddlewaretoken:document.getElementsByName('csrfmiddlewaretoken')[0].value,
            },
            success: function(data) {
                    if (data.length==2){
                        socket_mess.send(JSON.stringify({
                            'half': data
                        }));
                    }
                    else{                        
                        $(e.target).prop("checked", status == 'True' ? false : true);
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
    $.ajax({
        type: "POST",
        url:"/mess/future/",
        data: {
            csrfmiddlewaretoken: document.getElementsByName('csrfmiddlewaretoken')[0].value,
            date: $(this).serializeArray()[1].value,
            half: $(this).serializeArray()[2].value,
            status:$(this).serializeArray()[3].value,
        },
        success: function (data) {
            /*$("#paneloff").removeAttr("disabled");*/
            /*alert(new Date(data.date) + " --" + new Date(new Date().getFullYear() + " " + (new Date().getMonth() + 1) + " " + new Date().getDate() + " 05:30:00"));*/
            if (typeof data.status === 'undefined'){
                alert(data);
            }
            else{
                if (new Date(data.date).toLocaleDateString() == new Date().toLocaleDateString())
                {
                    if (data.status == "unchecked") {
                        $('input[id=' + data.half + ']').prop('checked', false);
                    }
                    else {
                        $('input[id=' + data.half + ']').prop('checked', data.status);
                    }

                    $('input[id=' + data.half + ']').change();
                }
                else{
                    alert("Succecss");
                }
            }
            $(e.target).parents('.panel-collapse').collapse('hide');
            /*$('#panelon').click();*/
            /*$('.panel-collapse').slideUp("slow");*/
        },
        /*complete: function (data) {
            alert("Sucecss");
        }*/
    });
  
});

$(document).on('submit', '#mealform', function (e) {
    e.preventDefault();
    $.ajax({
        type: "POST",
        url: "/mess/mealdish/",
        data: {
            csrfmiddlewaretoken: document.getElementsByName('csrfmiddlewaretoken')[0].value,
            meal: $(this).serializeArray()[1].value,
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