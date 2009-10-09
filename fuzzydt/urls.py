from django.conf.urls.defaults import *

urlpatterns = patterns('fuzzydt.views',
    url(r'^', 'fuzzydtparse', name='fuzzydtparse'),
)
