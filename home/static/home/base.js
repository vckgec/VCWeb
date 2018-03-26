$(document).ready(function () {
    $('#logout').click(function () {
        $.ajax({
            url: "/account/logout/",
            success: function (data) {
                javascript: location.reload(true);
            },
        });
    });
    $('#myNavbar,#appview').click(function () {
        $('#demo').collapse('hide');
    });
});








































