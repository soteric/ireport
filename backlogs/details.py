from django.shortcuts import render_to_response
from django.template.context import RequestContext
from getdefects.v1_meta import V1Meta
from datetime import datetime
import xml.etree.cElementTree as ET
from django.http import HttpResponse
import simplejson
import logging
# Create your views here.
def BacklogDetails(request):
    t1 = datetime.now()

    modules = {'pmr': '454039', 'pmt': '567434', 'mtr': '567436', 'scm': '611410', 'varp': '611415', 'cal': '805607',
               'tgm': '567435', 'cmp': '551644', 'pe': '294215'}
    status = ['_not_started', '_in_progress', '_in_testing', '_completed']
    fields = ['SecurityScope', 'Status.Name', 'Timebox.Name']
    attr_type = {'status': 0, 'project': 0, 'sprint': 0}
    not_started = [None, 'No Requirements', 'Requirements Done', 'Planned']
    in_progress = ['In Progress', 'Awaiting Clarification', 'Awaiting Code Fix', 'Blocked', 'Reopened']
    in_testing = ['In Testing', 'Dev Complete']
    completed = ['Done']

    statistic_data = {}
    scope = ''
    sel = ''

    for each_module in modules.iterkeys():
        for module in status:
            statistic_data[each_module + module] = 0

    for scope_id in modules.itervalues():
        if scope == '':
            scope = "SecurityScope='Scope:" + scope_id + "'"
        else:
            scope = scope + '|' + "SecurityScope='Scope:" + scope_id + "'"

    for field in fields:
        if sel == '':
            sel = field
        else:
            sel = sel + ',' + field

    v1 = V1Meta()
    query = v1.url + "/rest-1.v1/Data/Story?Sel=" + sel + "&Where=" + scope
    dom = v1.get_xml(query)
    print query
    doc = ET.fromstring(dom)
    root = doc

    for node_element in range(0, 4, 1):
        if root[0][node_element].attrib['name'] == 'Status.Name':
            attr_type['status'] = node_element
        if root[0][node_element].attrib['name'] == 'SecurityScope':
            attr_type['project'] = node_element
        if root[0][node_element].attrib['name'] == 'Timebox.Name':
            attr_type['sprint'] = node_element

    for node_asset in root:
        for module in modules.iteritems():
            if node_asset[attr_type['sprint']].text == 'Sprint 2':
                if node_asset[attr_type['project']][0].attrib['idref'].split(':')[1] == module[1]:
                    module_key = module[0]
                    if node_asset[attr_type['status']].text in not_started:
                        statistic_data[module_key + '_not_started'] += 1
                    elif node_asset[attr_type['status']].text in in_progress:
                        statistic_data[module_key + '_in_progress'] += 1
                    elif node_asset[attr_type['status']].text in completed:
                        statistic_data[module_key + '_completed'] += 1
                    if node_asset[attr_type['status']].text in in_testing:
                        statistic_data[module_key + '_in_testing'] += 1


    return render_to_response('backlogdetails.html', RequestContext(request, {
    }))

from django.shortcuts import render_to_response
from django.template.context import RequestContext
