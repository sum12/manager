from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('user_management.views',
    # Examples:
    # url(r'^$', 'manager.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^(\d+)/friends$','get_friends',name='user.friends'),
    url(r'^$','index',name='user.index')
)
