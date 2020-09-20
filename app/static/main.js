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
        const html_levels = [
            "HTML, CSS, JS reg",
            "HTML, CSS, JS prem"
        ];
        const java_levels = [
            "Java Basics reg",
            "Java Basics prem"
        ]
        const python_levels = [
            "Python Basics reg",
            "Python Basics prem",
            "Python Inter",
            "Python Basics prem",
            "Python adv",
            "Python adv prem"
        ];
        let selected_value = $("#exam_level").val();
        switch($("#lang").val()) {
            case "html":
                $("#exam_level").empty();
                html_levels.forEach(element => {
                    if(selected_value === element) {
                        $('#exam_level').append(`<option selected value="${element}">${element}</option>`);
                    } else {
                        $('#exam_level').append(`<option value="${element}">${element}</option>`);
                    }
                });
                break;
            case "java":
                $("#exam_level").empty();
                java_levels.forEach(element => {
                    if(selected_value === element) {
                        $('#exam_level').append(`<option selected value="${element}">${element}</option>`);
                    } else {
                        $('#exam_level').append(`<option value="${element}">${element}</option>`);
                    }
                });
                break;
            case "py":
                $("#exam_level").empty();
                python_levels.forEach(element => {
                    if(selected_value === element) {
                        $('#exam_level').append(`<option selected value="${element}">${element}</option>`);
                    } else {
                        $('#exam_level').append(`<option value="${element}">${element}</option>`);
                    }
                });
                break;
        }
    };


    $("#lang").change(e => {
        update_exam_level();
    });
    update_exam_level();

});
