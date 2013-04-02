from django.conf.urls import patterns, url

urlpatterns = patterns('handlecmd.views',
    url(r'^web/', 'recvcmdFromWeb'),
    url(r'^app/', 'recvcmdFromApp'),
    url(r'^getcmd/', 'getcmd'),
)
