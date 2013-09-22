/**
 * Created with PyCharm.
 * User: ewang
 * Date: 9/9/13
 * Time: 10:30 PM
 * To change this template use File | Settings | File Templates.
 */
/**
 * Created with PyCharm.
 * User: ewang
 * Date: 8/7/13
 * Time: 12:57 PM
 * To change this template use File | Settings | File Templates.
 */
$(document).ready(function () {
    $('#ichart').html("<img src='/static/images/loading.gif' style='padding-top: 200px;max-height: 80px; display: block; margin-left: auto; margin-right: auto;' >");
    $.getJSON('/getbacklognumber', function(data) {
          var not_started = new Array();
          var in_progress = new Array();
          var in_testing = new Array();
          var completed = new Array();

          $.each(data, function(key, val) {
              // tgm
              if(key==='tgm_not_started'){
                  not_started[0] = val;
              }
              if(key==='tgm_in_progress'){
                  in_progress[0] = val;
              }
              if(key==='tgm_in_testing'){
                  in_testing[0] = val;
              }
              if(key==='tgm_completed'){
                  completed[0] = val;
              }

              // pmt
              if(key==='pmt_not_started'){
                  not_started[1] = val;
              }
              if(key==='pmt_in_progress'){
                  in_progress[1] = val;
              }
              if(key==='pmt_in_testing'){
                  in_testing[1] = val;
              }
              if(key==='pmt_completed'){
                  completed[1] = val;
              }

              // pmr
              if(key==='pmr_not_started'){
                  not_started[2] = val;
              }
              if(key==='pmr_in_progress'){
                  in_progress[2] = val;
              }
              if(key==='pmr_in_testing'){
                  in_testing[2] = val;
              }
              if(key==='pmr_completed'){
                  completed[2] = val;
              }

              // mtr
              if(key==='mtr_not_started'){
                  not_started[3] = val;
              }
              if(key==='mtr_in_progress'){
                  in_progress[3] = val;
              }
              if(key==='mtr_in_testing'){
                  in_testing[3] = val;
              }
              if(key==='mtr_completed'){
                  completed[3] = val;
              }

              // cal
              if(key==='cal_not_started'){
                  not_started[4] = val;
              }
              if(key==='cal_in_progress'){
                  in_progress[4] = val;
              }
              if(key==='cal_in_testing'){
                  in_testing[4] = val;
              }
              if(key==='cal_completed'){
                  completed[4] = val;
              }

              // varp
              if(key==='varp_not_started'){
                  not_started[5] = val;
              }
              if(key==='varp_in_progress'){
                  in_progress[5] = val;
              }
              if(key==='varp_in_testing'){
                  in_testing[5] = val;
              }
              if(key==='varp_completed'){
                  completed[5] = val;
              }

              // scm
              if(key==='scm_not_started'){
                  not_started[6] = val;
              }
              if(key==='scm_in_progress'){
                  in_progress[6] = val;
              }
              if(key==='scm_in_testing'){
                  in_testing[6] = val;
              }
              if(key==='scm_completed'){
                  completed[6] = val;
              }

              // cmp
              if(key==='cmp_not_started'){
                  not_started[7] = val;
              }
              if(key==='cmp_in_progress'){
                  in_progress[7] = val;
              }
              if(key==='cmp_in_testing'){
                  in_testing[7] = val;
              }
              if(key==='cmp_completed'){
                  completed[7] = val;
              }

              // pe
              if(key==='pe_not_started'){
                  not_started[8] = val;
              }
              if(key==='pe_in_progress'){
                  in_progress[8] = val;
              }
              if(key==='pe_in_testing'){
                  in_testing[8] = val;
              }
              if(key==='pe_completed'){
                  completed[8] = val;
              }
          })

        $('#ichart').highcharts({
            chart: {
                type: 'column',
                spacingTop: 20,
                marginBottom: 70,
                borderWidth: 1,
                borderRadius: 0,
                backgroundColor: '#E7FFE6'
            },
            credits: {
                enabled: false
            },
            title: {
                text: '1311 Talent V1 Backlog Status (Sprint 2)',
                style: {
                    fontWeight: 'bold',
                    fontSize: '28px'
                }
            },
            xAxis: {
                categories: ['TGM', 'PMT', 'PMR', 'MTR', 'CAL', 'VRP', 'SCM', 'CMP', 'PE' ]
            },
            yAxis: {
                min: 0,
                title: {
                    text: 'Backlog Item Number'
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
                floating: true
            },
            tooltip: {
                formatter: function () {
                    return '<b>' + this.x + '</b><br/>' +
                        this.series.name + ': ' + this.y + '<br/>' +
                        'Total: ' + this.point.stackTotal +'<br/><br/>' + '<label style="color: blue">Click bar to view detail</label>';
                }
            },
            plotOptions: {
                column: {
                    stacking: 'normal',
                    dataLabels: {
                        enabled: true,
                        color: (Highcharts.theme && Highcharts.theme.dataLabelsColor) || 'white',
                        formatter:function() {
                            if(this.y != 0) {
                              return this.y;
                        }
                      }
                    }
                }
            },
            series: [
                {
                    name: 'Not Started',
                    data: not_started,
                    color: '#FF5B79',
                    point: {
                        events: {
                            click: function() {
                                window.open('/backlogdetails?module='+ this.category + '&status=' + this.series.name);
                            }
                        }
                    }
                },
                {
                    name: 'Dev In-progress',
                    data: in_progress,
                    color: '#6C71FF',
                    point: {
                        events: {
                            click: function() {
                                window.open('/backlogdetails?module='+ this.category + '&status=' + this.series.name);
                            }
                        }
                    }
                },
                {
                    name: 'QA In-progress',
                    data: in_testing,
                    color: '#2531FF',
                    point: {
                        events: {
                            click: function() {
                                window.open('/backlogdetails?module='+ this.category + '&status=' + this.series.name);
                            }
                        }
                    }
                },
                {
                    name: 'Completed',
                    data: completed,
                    color: 'green',
                    point: {
                        events: {
                            click: function() {
                                window.open('/backlogdetails?module='+ this.category + '&status=' + this.series.name);
                            }
                        }
                    }
                }
            ]
        });

    });
});
