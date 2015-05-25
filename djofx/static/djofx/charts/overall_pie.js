$(document).ready(function() {
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

    $.plot($("#placeholder"), data, options);
});
