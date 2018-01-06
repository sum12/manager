from django.conf.urls import url
from django.views.generic import TemplateView
from manager import settings
from user_management import urls as user_urls
from expense import urls as expense_urls
from daily import urls as daily_urls

params = {'template_name': 'index.html',
          'extra_context': {'STATIC_URL': settings.STATIC_URL}}

templateview = TemplateView.as_view(**params)

urlparams = dict(year='(?P<year>[0-9]{4})',
                 month='(?P<month>[0-9]{1,2})',
                 day='(?P<day>[0-9]{1,2})'
                 )

urlpatterns = [url(r'^{year}/{month}/{day}$'.format(**urlparams), templateview),
               url(r'^{year}/{month}$'.format(**urlparams), templateview),
               url(r'^{year}$'.format(**urlparams), templateview),
               url(r'^$', templateview)]

urlpatterns += user_urls.router.urls
urlpatterns += expense_urls.urlpatterns
urlpatterns += daily_urls.urlpatterns
