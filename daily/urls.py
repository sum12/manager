from rest_framework.routers import SimpleRouter
from django.conf.urls import url
from django.views.generic import TemplateView
from .views import DailyActivityViewSet, TypeViewSet


router = SimpleRouter(trailing_slash=False)
router.register(r'daily', DailyActivityViewSet, base_name='daily')
router.register(r'type', TypeViewSet, base_name='type')
#router.register(r'sharedexpense', ExpenseViewSet)

urlpatterns = [url(r'^dailyapp/$',TemplateView.as_view(template_name="daily_index.html"))]

urlpatterns += router.urls
