from django.shortcuts import render_to_response
from django.template.context import RequestContext

# Create your views here.
def Default(request):
    return render_to_response('base.html', RequestContext(request, {
        'content', "<p>Hello</p>"
    }))