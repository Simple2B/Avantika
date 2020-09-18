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

    $(".exam_delete_button").click(function (e) {

        if (confirm('Do you want delete the exam?')) {
            // Save it!
            console.log('Delete exam aproved');
        } else {
            // Do nothing!
            console.log('Delete exam canceled');
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

    function update_exam_level(){
        switch($("#lang").val()) {
            case "html":
                $("#exam_level").empty();
                $('#exam_level').append('<option value="HTML, CSS, JS reg">HTML, CSS, JS reg</option>');
                $('#exam_level').append('<option value="HTML, CSS, JS prem">HTML, CSS, JS prem</option>');
                break;
            case "java":
                $("#exam_level").empty();
                $('#exam_level').append('<option value="Java Basics reg">Java Basics reg</option>');
                $('#exam_level').append('<option value="Java Basics prem">Java Basics prem</option>');
                break;
            case "py":
                $("#exam_level").empty();
                $('#exam_level').append('<option value="Python Basics reg">Python Basics reg</option>');
                $('#exam_level').append('<option value="Python Basics prem">Python Basics prem</option>');
                $('#exam_level').append('<option value="Python Inter Prem">Python Inter Prem</option>');
                $('#exam_level').append('<option value="Python Basics prem">Python Basics prem</option>');
                $('#exam_level').append('<option value="Python adv">Python adv</option>');
                $('#exam_level').append('<option value="Python adv prem">Python adv prem</option>');
                break;
        }
    };


    $("#lang").change(e => {
        update_exam_level();
    });
    update_exam_level();

});