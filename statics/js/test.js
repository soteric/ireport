function go() {
    res_data = [0, 4, 6, 17];
    var unres_data = [17, 24, 8, 19];
    $('#ichart').highcharts({
        chart: {
            type: 'column'
        },
        credits: {
            enabled: false
        },
        title: {
            text: 'B1308 PMR Sprint Defects',
            style: {
                fontWeight: 'bold',
                fontSize: '20px'
            }
        },
        xAxis: {
            categories: ['P2', 'P3/P4 Regression', 'P3 Universal', 'Others']
        },
        yAxis: {
            min: 0,
            title: {
                text: 'Defects Number'
            },
            stackLabels: {
                enabled: true,
                style: {
                    fontWeight: 'bold',
                    color: (Highcharts.theme && Highcharts.theme.textColor) || 'gray'
                }
            }
        },
        legend: {
            align: 'right',
            x: -100,
            verticalAlign: 'top',
            y: 20,
            floating: true,
            backgroundColor: (Highcharts.theme && Highcharts.theme.legendBackgroundColorSolid) || 'white',
            borderColor: '#CCC',
            borderWidth: 1,
            shadow: false
        },
        tooltip: {
            formatter: function() {
                return '<b>' + this.x + '</b><br/>' +
                    this.series.name + ': ' + this.y + '<br/>' +
                    'Total: ' + this.point.stackTotal;
            }
        },
        plotOptions: {
            column: {
                stacking: 'normal',
                dataLabels: {
                    enabled: true,
                    color: (Highcharts.theme && Highcharts.theme.dataLabelsColor) || 'white'
                }
            }
        },
        series: [{
            name: 'Unresolved',
            data: res_data,
            color: 'red'
        }, {
            name: 'Resolved',
            data: unres_data,
            color: 'green'
        }]
    });
}