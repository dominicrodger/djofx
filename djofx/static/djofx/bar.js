function plot_bar_chart() {
    $.plot("#placeholder", [ flotise_years_and_months(data) ], {
        series: {
            bars: {
                show: true,
                barWidth: 0.5 * 1000 * 60 * 60 * 24 * 30, // milliseconds in roughly half a month
                align: "center"
            }
        },
        xaxis: {
            mode: "time",
            timeformat: "%b %Y",
            tickSize: [1, "month"]
        },
        yaxis: {
            tickFormatter: function(val, axis) { return "&pound;" + parseFloat(val).toFixed(0); },
            transform: function (v) { return -v; },
            inverseTransform: function (v) { return -v; }
        }
    });
}

$(document).ready(plot_bar_chart);
