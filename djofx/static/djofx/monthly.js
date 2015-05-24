function plot_bar_chart() {
    $.plot(
        "#placeholder", [
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
        ], {
        xaxis: {
            mode: "time",
            timeformat: "%b %Y",
            tickSize: [1, "month"]
        },
        yaxis: {
            tickFormatter: function(val, axis) { return "&pound;" + parseFloat(val).toFixed(0); },
        }
    });
}

$(document).ready(plot_bar_chart);
