function get_date(year, month) {
    return new Date(year, month - 1, 1).getTime();
}

$(document).ready(function() {
    $.plot(
        $("#placeholder"), [
            {
                data: data,
            }
        ],
        {
            lines: {
                show: true
            },
            points: {
                show: true
            },
            xaxis: {
                mode: "time",
                timeformat: "%b-%Y",
                tickSize: [1, "month"],
                axisLabel: 'Month',
            },
            yaxis: {
                tickFormatter: function(val, axis) { return "&pound;" + parseFloat(val).toFixed(0); }
            }
        }
    );
});
