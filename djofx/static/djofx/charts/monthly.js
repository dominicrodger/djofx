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
}

$(document).ready(plot_bar_chart);
