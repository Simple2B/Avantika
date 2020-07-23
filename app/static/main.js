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

    $("#code").keydown(e => {
        function insertAtCaret(text, textarea) {
            var scrollPos = textarea.scrollTop;
            var caretPos = textarea.selectionStart;

            var front = (textarea.value).substring(0, caretPos);
            var back = (textarea.value).substring(textarea.selectionEnd, textarea.value.length);
            textarea.value = front + text + back;
            caretPos = caretPos + text.length;
            textarea.selectionStart = caretPos;
            textarea.selectionEnd = caretPos;
            textarea.focus();
            textarea.scrollTop = scrollPos;

        }
        if (e.keyCode === 9) {
            e.preventDefault();
            insertAtCaret('\t', e.currentTarget);
        }
    });

});