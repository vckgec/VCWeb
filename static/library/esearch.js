$(function () {
    document.getElementById("loader").style.marginLeft = ($('#results').width() / 2 - $('#loader').width() / 2) + "px";
    document.getElementById("loader").style.marginTop = $('nav').height() + "px";
    $('#results').load("/library/libgen/ #myDiv", function () {
        document.getElementById("myDiv").style.display = "block";
        document.getElementById("loader").style.display = "none";
    });
});