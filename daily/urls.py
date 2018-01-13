from django.conf.urls import url
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required
from rest_framework.routers import SimpleRouter

from manager import settings

from .views import DailyActivityViewSet, TypeViewSet


router = SimpleRouter(trailing_slash=False)
router.register(r'daily', login_required(DailyActivityViewSet), base_name='daily')
router.register(r'type', login_required(TypeViewSet), base_name='type')
#router.register(r'sharedexpense', ExpenseViewSet)

params = {'template_name': 'daily_index.html',
          'extra_context': {'STATIC_URL': settings.STATIC_URL}}

templateView = TemplateView.as_view(**params)

loggedinView = login_required(templateView)
dailyappView = loggedinView

urls = [url(r'^dailyapp/$', dailyappView)]

urls += router.urls
urlpatterns = urls
