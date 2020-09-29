from django.urls import re_path
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required
from rest_framework.routers import SimpleRouter

from manager import settings

from .views import DailyActivityViewSet, TypeViewSet


router = SimpleRouter(trailing_slash=False)
router.register(r'daily', DailyActivityViewSet, basename='daily')
router.register(r'type', TypeViewSet, basename='type')
#router.register(r'sharedexpense', ExpenseViewSet)

params = {'template_name': 'daily_index.html',
          'extra_context': {'STATIC_URL': settings.STATIC_URL}}

templateView = TemplateView.as_view(**params)

loggedinView = login_required(templateView)
dailyappView = loggedinView

urls = [re_path(r'^dailyapp/$', dailyappView)]

urls += router.urls
urlpatterns = urls
