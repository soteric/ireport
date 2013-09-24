from django.http import HttpResponse
import simplejson
import logging
from v1_meta import V1Meta
from datetime import datetime
import xml.etree.cElementTree as ET
from defects.v1defect import V1Defect
from django.shortcuts import render

# Create your views here.
def GetDefectsNumber(request):
    t1 = datetime.now()

    modules = {'pmr': '454039', 'pmt': '567434', 'mtr': '567436', 'scm': '611410', 'vrp': '611415', 'cal': '805607',
               'tgm': '567435', 'cmp': '551644', 'pe': '294215'}
    status = ['_unres', '_in_testing', '_res']
    fields = ['SecurityScope', 'Custom_SLA2.Name', 'Type.Name', 'Custom_ConfigurationType.Name', 'Status.Name']
    p1p2 = ['P1', 'P2']
    cfg_type = ['Universal (Universal features require 30 days pre-notice.)', 'Admin Opt-out', 'Provisioning Opt-out']
    in_testing = ['Dev Complete', 'In Testing']
    attr_type = {'type': 0, 'config': 0, 'sla': 0, 'status': 0, 'project': 0, 'project.name': 0 }

    some_data = {}
    scope = ''
    sel = ''
    for each_module in modules.iterkeys():
        for module in status:
            some_data[each_module + module] = 0

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
    query = v1.url + "/rest-1.v1/Data/Defect?Sel=" + sel + "&Where=" + scope
    dom = v1.get_xml(query)
    doc = ET.fromstring(dom)
    root = doc

    for node_attribute in range(0, 6, 1):
        if root[0][node_attribute].attrib['name'] == 'Type.Name':
            attr_type['type'] = node_attribute
        if root[0][node_attribute].attrib['name'] == 'Custom_ConfigurationType.Name':
            attr_type['config'] = node_attribute
        if root[0][node_attribute].attrib['name'] == 'Custom_SLA2.Name':
            attr_type['sla'] = node_attribute
        if root[0][node_attribute].attrib['name'] == 'Status.Name':
            attr_type['status'] = node_attribute
        if root[0][node_attribute].attrib['name'] == 'SecurityScope':
            attr_type['project'] = node_attribute
        if root[0][node_attribute].attrib['name'] == 'SecurityScope.Name':
            attr_type['project.name'] = node_attribute

    for node_asset in root:
        for module in modules.iteritems():
            if node_asset[attr_type['project']][0].attrib['idref'].split(':')[1] == module[1]:
                module_key = module[0]
                if node_asset[attr_type['sla']].text in p1p2 \
                    or node_asset[attr_type['type']].text == 'Regression' \
                    or (node_asset[attr_type['sla']].text == 'P3' and node_asset[attr_type['type']].text == 'New' and node_asset[
                            attr_type['config']].text in cfg_type):
                    if node_asset[attr_type['status']].text == 'Done':
                        some_data[module_key + '_res'] += 1
                    elif node_asset[attr_type['status']].text in in_testing:
                        some_data[module_key + '_in_testing'] += 1
                    else:
                        some_data[module_key + '_unres'] += 1

    t2 = datetime.now()
    logging.error("Timer for defect report function\nTotal time spent: " + str((t2 - t1).seconds) + " seconds.")
    data = simplejson.dumps(some_data)
    return HttpResponse(data, mimetype='application/json')


def DefectDetails(request):
    parameters = {}
    for para in request.GET.iteritems():
        parameters[para[0].encode('utf-8')] = para[1].encode('utf-8')
    print parameters
    modules = {'pmr': '454039', 'pmt': '567434', 'mtr': '567436', 'scm': '611410', 'vrp': '611415', 'cal': '805607',
               'tgm': '567435', 'cmp': '551644', 'pe': '294215'}
    status_list = ['_unres', '_in_testing', '_res']
    fields = ['ID.Name', 'ID.Number', 'SecurityScope.Name', 'Status.Name', 'Timebox.Name', 'SecurityScope', 'Custom_SLA2.Name', 'Type.Name', 'Custom_ConfigurationType.Name', 'Owners.Name']
    # attr_type = {'status': 0, 'project': 0, 'sprint': 0}
    status_mapping = {
        'Unresolved': ['None', 'No Requirements', 'Requirements Done', 'Planned', 'In Progress', 'Awaiting Clarification', 'Awaiting Code Fix', 'Blocked', 'Reopened'],
        'In Testing': ['Dev Complete', 'In Testing'],
        'Closed': ['Done']
    }
    p1p2 = ['P1', 'P2']
    cfg_type = ['Universal (Universal features require 30 days pre-notice.)', 'Admin Opt-out', 'Provisioning Opt-out']

    scope = ''
    sel = ''
    backlogItems = {}
    defect_list = []
    v1_id = ''

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
    query = v1.url + "/rest-1.v1/Data/Defect?Sel=" + sel + "&Where=" + scope
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
                    node_value = node_attribute.find('Value')
                    if node_value != None:
                        backlogItems[id][attr] = node_value.text.split(" ")[0]
                    else:
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
            elif i[0] == 'Custom_SLA2.Name':
                sla = str(i[1])
            elif i[0] == 'Type.Name':
                type = str(i[1])
            elif i[0] == 'Custom_ConfigurationType.Name':
                configType = str(i[1])
            elif i[0] == 'Owners.Name':
                owner = str(i[1])
        if status in status_mapping[parameters['status']]:
            if sla in p1p2 \
                    or type == 'Regression' \
                    or (sla == 'P3' and type == 'New' and configType in cfg_type):
                custom_status = parameters['status']
                if configType == cfg_type[0]:
                    configType = configType.split(" ")[0]
                v1_tmp = V1Defect(v1_id=v1_id, oid=oid, title=title, custom_status=custom_status, module=module, sprint=sprint, status=status, sla=sla, type=type, configType=configType, owner=owner)
                defect_list.append(v1_tmp)

    return render(request, 'defectdetails.html', {'items': defect_list})
