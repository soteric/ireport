from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'ireport.views.home', name='home'),
    # url(r'^ireport/', include('ireport.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
    (r'^getdefectsnumber', 'getdefects.views.GetDefectsNumber'),
    (r'^defects', 'defects.views.Defects'),
    (r'^backlogdetails', 'backlogs.views.BacklogDetails'),
    (r'^home', 'home.views.Home'),
    (r'backlogs', 'backlogs.views.Backlogs'),
    (r'^getbacklognumber', 'backlogs.views.GetBacklogNumber'),
    (r'^defectdetails', 'getdefects.views.DefectDetails'),
    ('', 'default.views.Default'),
)
