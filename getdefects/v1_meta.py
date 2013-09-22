import logging
import urllib2
import re
from urllib2 import Request, HTTPBasicAuthHandler, HTTPCookieProcessor


class V1Meta():
    def __init__(self):
        self.username = 'ah_nt_domain\ewang'
        self.password = 'Welcomeew@'

        self.AUTH_HANDLERS = [HTTPBasicAuthHandler]

        try:
            from ntlm.HTTPNtlmAuthHandler import HTTPNtlmAuthHandler
        except ImportError:
            logging.warn("Windows integrated authentication module (ntlm) not found.")
        else:
            class CustomHTTPNtlmAuthHandler(HTTPNtlmAuthHandler):
                """ A version of HTTPNtlmAuthHandler that handles errors (better).

                    The default version doesn't use `self.parent.open` in it's
                    error handler, and completely bypasses the normal `OpenerDirector`
                    call chain, most importantly `HTTPErrorProcessor.http_response`,
                    which normally raises an error for 'bad' http status codes..
                """
                def http_error_401(self, req, fp, code, msg, hdrs):
                    response = HTTPNtlmAuthHandler.http_error_401(self, req, fp, code, msg, hdrs)
                    if not (200 <= response.code < 300):
                        response = self.parent.error(
                                'http', req, response, response.code, response.msg,
                                response.info)
                    return response

            self.AUTH_HANDLERS.append(CustomHTTPNtlmAuthHandler)
        self.url = 'http://versionone.successfactors.com/vone'

        base_url = self.url
        password_manager = urllib2.HTTPPasswordMgrWithDefaultRealm()
        password_manager.add_password(None, base_url, self.username, self.password)
        handlers = [HandlerClass(password_manager) for HandlerClass in self.AUTH_HANDLERS]
        self.opener = urllib2.build_opener(*handlers)
        self.opener.add_handler(HTTPCookieProcessor())
        self.request = Request(base_url)
        self.request.add_header("Content-Type", "text/xml;charset=UTF-8")
        self.module = {
            'pmr'   : '454039',
            'pmt'   : '567434',
            'mtr'   : '567436',
            'scm'   : '611410',
            'varp'  : '611415',
            'cal'   : '805607',
            'tgm'   : '567435'
        }
        # if self.module.has_key(sf_module):
        #     print sf_module, self.module[sf_module]
        #     self.v1_get(self.module[sf_module])
        # else:
        #     print "Your module is not configured in the system, please contact adminstrator to add your module.\nContact: Eric (Wei) Wang: ewang@successfactors.com"

    def v1_get(self, mod, id):
        print "fetching data for ", mod, ' ...'
        queue = {'total':
        "http://versionone.successfactors.com/vone/rest-1.v1/Data/Scope/"+id+"/Workitems:Defect.@Count",
        'unresolved_p1p2+p3reg' :"http://versionone.successfactors.com/vone/rest-1.v1/Data/Scope/"+id+"/Workitems:Defect[(Custom_SLA2.Name='P1'%7CCustom_SLA2.Name='P2')%7C(Custom_SLA2.Name='P3';Type.Name='Regression')].@Count",
        'resolved_p1p2+p3reg' :"http://versionone.successfactors.com/vone/rest-1.v1/Data/Scope/"+id+"/Workitems:Defect[(Custom_SLA2.Name='P1'%7CCustom_SLA2.Name='P2')%7C(Custom_SLA2.Name='P3';Type.Name='Regression');Status.Name='Done'].@Count",
        'unresolved_p3+out' :"http://versionone.successfactors.com/vone/rest-1.v1/Data/Scope/"+id+"/Workitems:Defect[Custom_SLA2.Name='P3';Type.Name='New';(Custom_ConfigurationType.Name='Provisioning%20Opt-out'%7CCustom_ConfigurationType.Name='Admin%20Opt-out')].@Count",
        'resolved_p3+out' :"http://versionone.successfactors.com/vone/rest-1.v1/Data/Scope/"+id+"/Workitems:Defect[Custom_SLA2.Name='P3';Type.Name='New';(Custom_ConfigurationType.Name='Provisioning%20Opt-out'%7CCustom_ConfigurationType.Name='Admin%20Opt-out');Status.Name='Done'].@Count",
        'unresolved_p3+universal' :"http://versionone.successfactors.com/vone/rest-1.v1/Data/Scope/"+id+"/Workitems:Defect[Custom_ConfigurationType.Name='Universal%20(Universal%20features%20require%2030%20days%20pre-notice.)'].@Count",
        'resolved_p3+universal' :"http://versionone.successfactors.com/vone/rest-1.v1/Data/Scope/"+id+"/Workitems:Defect[Custom_ConfigurationType.Name='Universal%20(Universal%20features%20require%2030%20days%20pre-notice.)';Status.Name='Done'].@Count"
        }
        result = {}
        for i in queue.iterkeys():
            key, number = self.send_request(i, queue[i])
            result[key] = number

        total_unresolved = result['unresolved_p3+out'] + result['unresolved_p1p2+p3reg'] + result['unresolved_p3+universal']
        total_resolved = result['resolved_p3+out'] + result['resolved_p1p2+p3reg'] + result['resolved_p3+universal']
        print mod
        print 'total_unresolved', total_unresolved
        print 'total_resolved', total_resolved
        return total_unresolved, total_resolved

    def send_request(self, key, req):
        response = self.opener.open(req)
        html = response.read()
        pattern = re.compile('>\d+<')
        match = re.search(pattern, html)
        number = int(match.group(0)[1:-1])
        return key, number

    def get_xml(self, query):
        response = self.opener.open(query)
        html = response.read()
        return html

# v1 = V1Meta()
# m = {
#             'pmr'   : '454039',
#             'pmt'   : '567434',
#             'mtr'   : '567436',
#             'scm'   : '611410',
#             'varp'  : '611415',
#             'cal'   : '805607',
#             'tgm'   : '567435'
#         }
# for i in m.iterkeys():
#     unres, res = v1.v1_get(i, m[i])
