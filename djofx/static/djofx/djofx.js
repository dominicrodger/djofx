function handle_form_submission() {
    var theform = $(this);
    theform.find("button").prop("disabled", true);
    $.ajax({
        type: "POST",
        url: $(this).attr('action'),
        data: $(this).serialize(),
        success: function(data) {
            var therow = theform.closest("tr");
            $(therow).html(data);
            theform.find("button").prop("disabled", false);
            bind_form_handlers();
        }
    });

    return false;
}

function bind_form_handlers() {
    $("form.update_row").submit(handle_form_submission);
}

$(document).ready(bind_form_handlers);
