function displaytips() {
    tipbutt = document.getElementsByClassName("tipsbutton")[0];
    tips = document.getElementById("tips");
    if (tipbutt.innerHTML == "Tips") {
        tips.style.display = "block";
        tipbutt.innerHTML = "Hide"
    }
    else {
        tips.style.display = "none";
        tipbutt.innerHTML = "Tips"
    }
}
$(function () {
    position.style.marginLeft = (screen.availWidth / 2 - $('#position').width() / 2) + "px";
    position.style.marginTop = (screen.availHeight / 2 - $('nav').height() - $('footer').height() - $('#position').height() / 2) + "px";
});