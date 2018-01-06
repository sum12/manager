from django.conf.urls import url
from django.contrib import admin
from django.views.generic import TemplateView
from django.template.response import SimpleTemplateResponse
from user_management import urls as user_urls
from expense import urls as expense_urls
from daily import urls as daily_urls
urlpatterns =[
        url(r'^(?P<year>[0-9]{4})/(?P<month>[0-9]{1,2})/(?P<day>[0-9]{1,2})$',TemplateView.as_view(template_name="index.html")),
        url(r'^(?P<year>[0-9]{4})/(?P<month>[0-9]{1,2})$',TemplateView.as_view(template_name="index.html")),
        url(r'^(?P<year>[0-9]{4})$',TemplateView.as_view(template_name="index.html")),
        url(r'^$',TemplateView.as_view(template_name="index.html"))
        ]

urlpatterns += user_urls.router.urls 
urlpatterns += expense_urls.urlpatterns 
urlpatterns += daily_urls.urlpatterns 
