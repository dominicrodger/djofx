function refresh_table_contents() {
    $.ajax({
        type: "GET",
        url: window.location.href,
        success: function(data) {
            $("#transaction_list").html(data);
            bind_handlers_in_transaction_list();
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

function prepare_categorise_modal() {
    var btn = $(this);
    $("#transaction_inline_form").attr(
        "action", btn.attr("data-url")
    );
    $("#payee_label").html(btn.attr("data-payee"));
    $("#id_category").val(btn.attr("data-category"));
}

function bind_handlers_in_transaction_list() {
    $("form.update_row").submit(
        handle_form_submission
    );
    $(".payment-categorise-modal-btn").click(
        prepare_categorise_modal
    );
}

function handle_modal_submission() {
    var theform = $(this);
    theform.find("button").prop("disabled", true);
    $.ajax({
        type: "POST",
        url: $(this).attr('action'),
        data: $(this).serialize(),
        success: function(data) {
            refresh_table_contents();
            $(".modal").modal("hide");
            theform.find("button").prop("disabled", false);
        }
    });

    return false;
}

function get_date(year, month) {
    return new Date(year, month - 1, 1).getTime();
}

function flotise_years_and_months(data) {
    var rval = []

    for (var i = 0; i < data.length; i += 1) {
        var year_and_month = data[i][0];
        var value = data[i][1];

        rval.push(
            [
                get_date(year_and_month[0], year_and_month[1]),
                value
            ]
        );
    }

    return rval;
}

function format_currency_value(val, axis) {
    return "&pound;" + parseFloat(val).toLocaleString();
}

$(document).ready(function() {
    bind_handlers_in_transaction_list();
    $("#transaction_inline_form").submit(handle_modal_submission);

    $('.modal').on('shown.bs.modal', function (e) {
        $("#transaction_inline_form select").focus();
    })
});
