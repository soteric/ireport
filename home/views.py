from django.http import HttpResponse
from django.template.loader import get_template
from django.template import Context

# Create your views here.
def Home(request):
    t = get_template('home.html')
    pages = {}
    pages['Team Overview'] = 'sf/teamoverviewpage'
    print pages
    html = t.render(Context({'pages': {('Team Overview': 'sf/teamoverviewpage'), ('Reviews':'sf/pmreviews'), ('Admin tools': 'sf/admin')},
                             'environments': {'QACAND', 'QAMIAN', 'QAPATCH', 'QAAUTOCAND', 'QAAUTOCAND2', 'QAPATCHPREM'}
                             }))
    return HttpResponse(html)