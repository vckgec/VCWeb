$(function () {
    if (screen.availWidth > 767) {
        position.style.marginLeft = (screen.availWidth / 2 - $('#position').width() / 2) + "px";
        position.style.marginTop = (screen.availHeight / 2 - $('nav').height() - $('footer').height() - $('#position').height() / 2) + "px";
    }
});