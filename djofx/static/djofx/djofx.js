function refresh_table_contents() {
    $.ajax({
        type: "GET",
        url: window.location.href,
        success: function(data) {
            $("#transaction_list").html(data);
            bind_form_handlers();
        }
    });
}

function handle_form_submission() {
    var theform = $(this);
    theform.find("button").prop("disabled", true);
    $.ajax({
        type: "POST",
        url: $(this).attr('action'),
        data: $(this).serialize(),
        success: function(data) {
            refresh_table_contents();
        }
    });

    return false;
}

function bind_form_handlers() {
    $("form.update_row").submit(handle_form_submission);
}

$(document).ready(bind_form_handlers);
