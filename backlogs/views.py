from django.shortcuts import render_to_response
from django.shortcuts import RequestContext
from backlogs.v1story import V1Story
from getdefects.v1_meta import V1Meta
from datetime import datetime
from django.shortcuts import render
import xml.etree.cElementTree as ET
from django.http import HttpResponse
import simplejson
import logging

# Create your views here.
def Backlogs(request):
    return render_to_response('backlog.html', RequestContext(request, {
    }))


def GetBacklogNumber(request):
    t1 = datetime.now()

    modules = {'pmr': '454039', 'pmt': '567434', 'mtr': '567436', 'scm': '611410', 'varp': '611415', 'cal': '805607',
               'tgm': '567435', 'cmp': '551644', 'pe': '294215'}
    status = ['_not_started', '_in_progress', '_in_testing', '_completed']
    fields = ['SecurityScope.Name', 'SecurityScope', 'Status.Name', 'Timebox.Name']
    attr_type = {'status': 0, 'project': 0, 'sprint': 0}
    not_started = ['None', 'No Requirements', 'Requirements Done', 'Planned']
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
    doc = ET.fromstring(dom)
    root = doc

    for ne in range(0, 4, 1):
        if root[0][ne].attrib['name'] == 'Status.Name':
            attr_type['status'] = ne
        if root[0][ne].attrib['name'] == 'SecurityScope':
            attr_type['project'] = ne
        if root[0][ne].attrib['name'] == 'Timebox.Name':
            attr_type['sprint'] = ne
    for ns in root:
        for module in modules.iteritems():
            if ns[attr_type['sprint']].text == 'Sprint 2':
                if ns[attr_type['project']][0].attrib['idref'].split(':')[1] == module[1]:
                    module_key = module[0]
                    if ns[attr_type['status']].text in not_started:
                        statistic_data[module_key + '_not_started'] += 1
                    elif ns[attr_type['status']].text in in_progress:
                        statistic_data[module_key + '_in_progress'] += 1
                    elif ns[attr_type['status']].text in completed:
                        statistic_data[module_key + '_completed'] += 1
                    if ns[attr_type['status']].text in in_testing:
                        statistic_data[module_key + '_in_testing'] += 1

    t2 = datetime.now()
    logging.info("Timer for backlog report function\nTotal time spent: ", (t2 - t1).seconds, "seconds.")
    data = simplejson.dumps(statistic_data)
    return HttpResponse(data, mimetype='application/json')


def BacklogDetails(request):
    parameters = {}
    for para in request.GET.iteritems():
        parameters[para[0].encode('utf-8')] = para[1].encode('utf-8')
    print parameters
    modules = {'pmr': '454039', 'pmt': '567434', 'mtr': '567436', 'scm': '611410', 'varp': '611415', 'cal': '805607',
               'tgm': '567435', 'cmp': '551644', 'pe': '294215'}
    status = ['_not_started', '_in_progress', '_in_testing', '_completed']
    fields = ['ID.Name', 'ID.Number', 'SecurityScope.Name', 'Status.Name', 'Timebox.Name', 'SecurityScope']
    # attr_type = {'status': 0, 'project': 0, 'sprint': 0}
    status_mapping = {
        'Not Started': ['None', 'No Requirements', 'Requirements Done', 'Planned'],
        'Dev In-progress': ['In Progress', 'Awaiting Clarification', 'Awaiting Code Fix', 'Blocked', 'Reopened'],
        'QA In-progress': ['In Testing', 'Dev Complete'],
        'Completed': ['Done']
    }

    statistic_data = {}
    scope = ''
    sel = ''
    backlogItems = {}
    story_list = []
    v1_id = ''

    for each_module in modules.iterkeys():
        for module in status:
            statistic_data[each_module + module] = 0

    # setup scope for all modules
    # for scope_id in modules.itervalues():
    #     if scope == '':
    #         scope = "SecurityScope='Scope:" + scope_id + "'"
    #     else:
    #         scope = scope + '|' + "SecurityScope='Scope:" + scope_id + "'"

    # single scope from request
    scope = "SecurityScope='Scope:" + modules[str(parameters['module']).lower()] + "'"

    for field in fields:
        if sel == '':
            sel = field
        else:
            sel = sel + ',' + field

    v1 = V1Meta()
    query = v1.url + "/rest-1.v1/Data/Story?Sel=" + sel + "&Where=" + scope
    print query
    dom = v1.get_xml(query)
    doc = ET.fromstring(dom)
    root = doc

    for node_asset in root:
        id = node_asset.attrib['id'].split(':')[1]
        backlogItems[id] = {}
        for node_attribute in node_asset:
            for attr in fields:
                if node_attribute.attrib['name'] == attr:
                    backlogItems[id][attr] = node_attribute.text
        backlogItems[id]['oid'] = node_asset.attrib['id']

    for item in backlogItems.iteritems():
        for i in item[1].iteritems():
            if i[0] == 'ID.Number':
                v1_id = str(i[1])
            elif i[0] == 'ID.Name':
                try:
                    title = str(i[1])
                except Exception:
                    title = "=== ASCII character detected, please modify the title!!! ==="
            elif i[0] == 'Timebox.Name':
                sprint = str(i[1]).replace(' ', '')
            elif i[0] == 'Status.Name':
                status = str(i[1])
            elif i[0] == 'oid':
                oid = str(i[1])
            elif i[0] == 'SecurityScope.Name':
                start = str(i[1]).find('(')+1
                end = str(i[1]).find(')')
                module = str(i[1])[start:end]
        if status in status_mapping[parameters['status']]:
            custom_status = parameters['status']
            v1_tmp = V1Story(v1_id=v1_id, oid=oid, title=title, custom_status=custom_status, module=module, sprint=sprint, status=status)
            story_list.append(v1_tmp)

    return render(request, 'backlogdetails.html', {'items': story_list})
