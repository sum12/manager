from rest_framework.routers import SimpleRouter
from django.conf.urls import patterns, include, url
from .views import DailyActivityViewSet, getGraph


router = SimpleRouter(trailing_slash=False)
router.register(r'daily', DailyActivityViewSet, base_name='daily')
#router.register(r'sharedexpense', ExpenseViewSet)

urlpatterns = patterns('daily',
        url('(?P<activity_type>\w*)/$', getGraph)
        )

urlpatterns += router.urls
