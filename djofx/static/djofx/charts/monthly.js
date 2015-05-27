function refresh_transaction_list(data) {
    $("#transaction_list").html(data);
}

function refresh_spending_breakdown(data) {
    var options = {
        series: {
            pie: {
                show: true,
                innerRadius: 0.5,
                combine: {
                    color: '#999',
                    threshold: 0.04
                }
            }
        },
        legend: {
            show: false
        }
    };
    $.plot($("#pie_placeholder"), data, options);
}

function handle_plot_click(event, pos, item) {
    if (!item) {
        return;
    }

    var thedate = new Date(item.datapoint[0]);
    var series = item.series.label;

    // January is 0, because Javascript
    var themonth = thedate.getMonth() + 1;
    if (themonth < 10) {
        themonth = '0' + themonth;
    }
    var theyear = '' + thedate.getFullYear();
    var transactions_url = Urls.djofx_transaction_list(series, theyear, themonth)
    $.ajax({
        type: "GET",
        url: transactions_url,
        success: refresh_transaction_list
    });

    var months = [
        'January',
        'February',
        'March',
        'April',
        'May',
        'June',
        'July',
        'August',
        'September',
        'October',
        'November',
        'December'
    ]

    var pretty_date = months[thedate.getMonth()] + " " + theyear;

    $("#pie_placeholder").html("");
    $("#transaction_list_header").html("<h3>" + series + " transactions for " + pretty_date + "</h3>");

    $("#transaction_pie_header").html("<h3>" + series + " for " + pretty_date + " <small>" + format_currency_value(item.datapoint[1]) + "</small></h3>");

    if (series === "Outgoings") {
        var breakdown_url = Urls.djofx_monthly_breakdown(theyear, themonth)
        $.ajax({
            dataType: "json",
            url: breakdown_url,
            success: refresh_spending_breakdown
        });
    }
}

function plot_bar_chart() {
    var data = [
        {
            label: "Income",
            data: flotise_years_and_months(income),
            lines: {
                show: true
            },
            points: {
                show: true
            }
        },
        {
            label: "Outgoings",
            data: flotise_years_and_months(outgoings),
            bars: {
                show: true,
                barWidth: 0.5 * 1000 * 60 * 60 * 24 * 30, // milliseconds in roughly half a month
                align: "center",
                order: 1
            }
        }
    ];

    var options = {
        grid: {
	    hoverable: true,
	    clickable: true
	},
        xaxis: {
            mode: "time",
            timeformat: "%b %Y",
            tickSize: [1, "month"]
        },
        yaxis: {
            tickFormatter: format_currency_value,
        }
    };

    $.plot("#placeholder", data, options);

    $("#placeholder").bind("plotclick", handle_plot_click);
}

$(document).ready(plot_bar_chart);
