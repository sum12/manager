from django.conf.urls import url
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required
from manager import settings
from user_management import urls as user_urls
from expense import urls as expense_urls
from daily import urls as daily_urls

params = {'template_name': 'index.html',
          'extra_context': {'STATIC_URL': settings.STATIC_URL}}

templateView = TemplateView.as_view(**params)
loggedinView = login_required(templateView)

expenseView = loggedinView


urlparams = dict(year='(?P<year>[0-9]{4})',
                 month='(?P<month>[0-9]{1,2})',
                 day='(?P<day>[0-9]{1,2})'
                 )

urls = [url(r'^{year}?/?{month}?/?{day}?$'.format(**urlparams), expenseView)]

urls += user_urls.urlpatterns
urls += expense_urls.urlpatterns
urls += daily_urls.urlpatterns
urlpatterns = urls
