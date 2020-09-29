from django.urls import re_path
from django.contrib.auth import views as authViews

viewParams = {'template_name': 'user_management/login.html'}

urls = [
        re_path('^login', authViews.LoginView.as_view(**viewParams),name='login'),
        re_path('^logout', authViews.LogoutView.as_view())
        ]
urlpatterns = urls
