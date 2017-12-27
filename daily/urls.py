from rest_framework.routers import SimpleRouter
from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView
from .views import DailyActivityViewSet, getGraph


router = SimpleRouter(trailing_slash=False)
router.register(r'daily', DailyActivityViewSet, base_name='daily')
#router.register(r'sharedexpense', ExpenseViewSet)

urlpatterns = patterns('', url(r'^dailyapp/$',TemplateView.as_view(template_name="daily_index.html")))

urlpatterns += router.urls
