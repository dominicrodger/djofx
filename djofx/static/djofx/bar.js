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
            tickFormatter: function(val, axis) { return "&pound;" + parseFloat(val).toFixed(0); }
        }
    });
}

$(document).ready(plot_bar_chart);
