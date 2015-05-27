function refresh_transaction_list(data) {
    $("#transaction_list").html(data);
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

    $("#placeholder").bind("plotclick", function (event, pos, item) {
	if (item) {
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
	}
    });
}

$(document).ready(plot_bar_chart);
