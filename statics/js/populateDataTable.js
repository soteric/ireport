/**
 * Created with PyCharm.
 * User: ewang
 * Date: 9/20/13
 * Time: 9:47 AM
 * To change this template use File | Settings | File Templates.
 */
$(document).ready(function () {
    table = $('#datatable').dataTable({
        'bProcessing': true,
        "bJQueryUI": true,
        "iDisplayLength": 10,
        "aLengthMenu": [[10, 25, 50, -1], [10, 25, 50, "All"]],
        "oLanguage": {
        "sSearch": '',
        "sPageButton": "dataTables_paginate paging_",
        "sLengthMenu": '_MENU_',
        "sInfo": '_START_ to _END_ of _TOTAL_'
        }
    });
})