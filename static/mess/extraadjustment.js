$(function () {
    if (screen.availWidth > 767) {
        extra.style.marginLeft = ($('#position1').width() / 2 - $('#extra').width() / 2) + "px";
        extra.style.marginTop = (screen.availHeight / 2 - $('nav').height() - $('footer').height() - $('#extra').height() / 2 - 30) + "px";
        adjust.style.marginLeft = ($('#position2').width() / 2 - $('#adjust').width() / 2) + "px";
        adjust.style.marginTop = (screen.availHeight / 2 - $('nav').height() - $('footer').height() - $('#adjust').height() / 2 - 30) + "px";
    }
});