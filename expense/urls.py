from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'manager.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^save/$','expense.views.save',name='expense.save'),
    url(r'^add/$','expense.views.add', name='expense.add'),
    url(r'^shared/(\d*)/$', 'expense.views.shared', name='expense.shared'),
    url(r'^$', 'expense.views.simple', name='expense.simple')
)
