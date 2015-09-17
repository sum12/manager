from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.views.generic import TemplateView
from django.template.response import SimpleTemplateResponse
from user_management import urls as user_urls
from expense import urls as expense_urls

urlpatterns = patterns('',
        url(r'^$',TemplateView.as_view(template_name="index.html")))

urlpatterns += user_urls.router.urls + expense_urls.urlpatterns
