from django.shortcuts import render_to_response
from django.template.context import RequestContext

# Create your views here.
def Defects(request):
    return render_to_response('demo.html', RequestContext(request, {
    }))

