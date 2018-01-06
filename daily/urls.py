from rest_framework.routers import SimpleRouter
from django.conf.urls import url
from django.views.generic import TemplateView

from manager import settings

from .views import DailyActivityViewSet, TypeViewSet


router = SimpleRouter(trailing_slash=False)
router.register(r'daily', DailyActivityViewSet, base_name='daily')
router.register(r'type', TypeViewSet, base_name='type')
#router.register(r'sharedexpense', ExpenseViewSet)

params = {'template_name': 'daily_index.html',
          'extra_context': {'STATIC_URL': settings.STATIC_URL}}

templateview = TemplateView.as_view(**params)

urlpatterns = [url(r'^dailyapp/$', templateview)]

urlpatterns += router.urls
