$(function () {
    document.getElementById("loader").style.marginLeft = ($('#results').width() / 2 - $('#loader').width() / 2) + "px";
    document.getElementById("loader").style.marginTop = $('nav').height() + "px";
});
$(document).ready(function () {
    var ws_scheme = window.location.protocol == "https:" ? "wss" : "ws";
    ws = new WebSocket(ws_scheme +"://socketvc.herokuapp.com");
    var i;
    var row;
    ws.onopen = function (e) {
        i=0;
        row = ['row1', 'row2'];
        console.log(e)
        ws.send(JSON.stringify({ 'type': 'library', 'message': $('#query').val()}));
    };    
    ws.onmessage = function (e) {
        var ebooksdata = JSON.parse(e.data);
        ebookshtml = '<a href=' + ebooksdata.booklink + '>' +
            '<div class="container-fluid '+row[i%2]+'">' +
            '<div class="col-sm-3">' + ebooksdata.author + '</div>' +
            '<div class="col-sm-7">' + ebooksdata.title + '</div>' +
            '<div class="col-sm-2"><i>' + ebooksdata.type + ';' + ebooksdata.size + '</i></div>' +
            '</div>' +
            '</a>';
        i+=1;
        if (i>1){
            $('#ebookscount').html(i+' ebooks found.');
        }
        else{
            $('#ebookscount').html(i + ' ebook found.');
        }        
        document.getElementById("ebooksdata").style.display = "block";
        document.getElementById("loader").style.display = "none";
        $('#ebooksdata').append(ebookshtml);
    };
    ws.onclose = function (e) {
        if (i < 1) {
            setTimeout(function () {

                document.getElementById("loader").style.display = "none";
                $('#ebookscount').html('No ebook found.');
            }, 3000);
        }      
        console.log(e)
    };
    ws.onerror = function (e) {
        if (i < 1) {
            setTimeout(function () {

                document.getElementById("loader").style.display = "none";
                $('#ebookscount').html('No ebook found.');
            }, 3000);
        }
        console.log(e)
    };
});