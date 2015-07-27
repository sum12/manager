from django.conf.urls import patterns, include, url
from django.contrib import admin
from user_management import urls as user_urls
from expense import urls as expense_urls

urlpatterns = user_urls.router.urls + expense_urls.router.urls
