from django.conf.urls import url
from django.contrib.auth import views as authViews

viewParams = {'template_name': 'user_management/login.html'}

urls = [
        url('^login', authViews.login, viewParams, name='login'),
        url('^logout', authViews.logout)
        ]
urlpatterns = urls
