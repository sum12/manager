from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    url(r'^question/(\d+)/$', 'expense.views.question', name='expense.question'),
    url(r'^question/(\d+)/(\d+)/$', 'expense.views.question', name='expense.question'),
    url(r'^answers/(\d+)/(\d+)/$', 'expense.views.answers', name='expense.answers'),
)
