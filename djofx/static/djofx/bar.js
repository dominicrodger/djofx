function plot_bar_chart() {
    $.plot("#placeholder", [ data ], {
	series: {
	    bars: {
		show: true,
		barWidth: 0.6,
		align: "center"
	    }
	},
	xaxis: {
	    mode: "categories",
	    tickLength: 0
	},
        yaxis: {
            tickFormatter: function(val, axis) { return "&pound;" + parseFloat(val).toFixed(0); }
        }
    });
}

$(document).ready(plot_bar_chart);
