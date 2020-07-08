// custom javascript
$(document).ready(function () {

    $("#menu-toggle").click(function (e) {
        e.preventDefault();
        $("#wrapper").toggleClass("toggled");
    });

    $(".user_delete_button").click(function (e) {

        if (confirm('Do you want delete the user?')) {
            // Save it!
            console.log('Delete user aproved');
        } else {
            // Do nothing!
            console.log('Delete user canceled');
            e.preventDefault();
        }
    });

});