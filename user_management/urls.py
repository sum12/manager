from django.conf.urls import patterns, include, url
from django.contrib import admin

from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter(trailing_slash=False)
router.register(r'api', views.PersonViewSet)
urlpatterns = patterns('user_management.views',
    # Examples:
    # url(r'^$', 'manager.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^(\d+)/friends$','get_friends',name='user.friends'),
#    url(r'^$','index',name='user.index')
) +  router.urls
