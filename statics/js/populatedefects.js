/**
 * Created with PyCharm.
 * User: ewang
 * Date: 8/7/13
 * Time: 12:57 PM
 * To change this template use File | Settings | File Templates.
 */
$(document).ready(function () {
    $('#ichart').html("<img src='/static/images/loading.gif' style='padding-top: 200px;max-height: 80px; display: block; margin-left: auto; margin-right: auto;' >");
    $.getJSON('/getdefectsnumber', function(data) {
          var unres_data = new Array();
          var res_data = new Array();
          var in_testing_data = new Array();

          $.each(data, function(key, val) {
              // tgm
              if(key==='tgm_unres'){
                  unres_data[0] = val;
              }
              if(key==='tgm_in_testing'){
                  in_testing_data[0] = val;
              }
              if(key==='tgm_res'){
                  res_data[0] = val;
              }

              // pmt
              if(key==='pmt_unres'){
                  unres_data[1] = val;
              }
              if(key==='pmt_in_testing'){
                  in_testing_data[1] = val;
              }
              if(key==='pmt_res'){
                  res_data[1] = val;
              }

              // pmr
              if(key==='pmr_unres'){
                  unres_data[2] = val;
              }
              if(key==='pmr_in_testing'){
                  in_testing_data[2] = val;
              }
              if(key==='pmr_res'){
                  res_data[2] = val;
              }

              // mtr
              if(key==='mtr_unres'){
                  unres_data[3] = val;
              }
              if(key==='mtr_in_testing'){
                  in_testing_data[3] = val;
              }
              if(key==='mtr_res'){
                  res_data[3] = val;
              }

              // cal
              if(key==='cal_unres'){
                  unres_data[4] = val;
              }
              if(key==='cal_in_testing'){
                  in_testing_data[4] = val;
              }
              if(key==='cal_res'){
                  res_data[4] = val;
              }

              // varp
              if(key==='vrp_unres'){
                  unres_data[5] = val;
              }
              if(key==='vrp_in_testing'){
                  in_testing_data[5] = val;
              }
              if(key==='vrp_res'){
                  res_data[5] = val;
              }

              // scm
              if(key==='scm_unres'){
                  unres_data[6] = val;
              }
              if(key==='scm_in_testing'){
                  in_testing_data[6] = val;
              }
              if(key==='scm_res'){
                  res_data[6] = val;
              }

              // cmp
              if(key==='cmp_unres'){
                  unres_data[7] = val;
              }
              if(key==='cmp_in_testing'){
                  in_testing_data[7] = val;
              }
              if(key==='cmp_res'){
                  res_data[7] = val;
              }

              // scm
              if(key==='pe_unres'){
                  unres_data[8] = val;
              }
              if(key==='pe_in_testing'){
                  in_testing_data[8] = val;
              }
              if(key==='pe_res'){
                  res_data[8] = val;
              }
          })

        $('#ichart').highcharts({
            chart: {
                type: 'column',
                marginBottom: 70,
                borderWidth: 1,
                borderRadius: 0,
                backgroundColor: '#FDFFFF'
            },
            credits: {
                enabled: false
            },
            title: {
                text: '1311 Talent REM (V1 Defects)',
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
                    name: 'Unresolved',
                    data: unres_data,
                    color: '#FF5B79',
                    point: {
                        events: {
                            click: function() {
                                window.open('/defectdetails?module='+ this.category + '&status=' + this.series.name);
                            }
                        }
                    }
                },
                {
                    name: 'In Testing',
                    data: in_testing_data,
                    color: '#2531FF',
                    point: {
                        events: {
                            click: function() {
                                window.open('/defectdetails?module='+ this.category + '&status=' + this.series.name);
                            }
                        }
                    }
                },
                {
                    name: 'Closed',
                    data: res_data,
                    color: 'green',
                    point: {
                        events: {
                            click: function() {
                                window.open('/defectdetails?module='+ this.category + '&status=' + this.series.name);
                            }
                        }
                    }
                }
            ]
        });
    });
});
