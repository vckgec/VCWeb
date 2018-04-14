$(document).ready(function () {
    $('#logout').click(function () {
        $.ajax({
            url: "/account/logout/",
            success: function (data) {
                javascript: location.reload(true);
            },
        });
    });
    $('#myNavbar,#myBody').click(function () {
        $('#demo').collapse('hide');
    });
});








































