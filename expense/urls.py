from rest_framework.routers import SimpleRouter
from django.conf.urls import url
from .views import ExpenseViewSet


router = SimpleRouter(trailing_slash=False)
router.register(r'expense', ExpenseViewSet, base_name='expense')
#router.register(r'sharedexpense', ExpenseViewSet)

urlpatterns =[
        url(r'^expenses/(?P<year>[0-9]{4})/(?P<month>[0-9]{1,2})/(?P<day>[0-9]{1,2})$', ExpenseViewSet.as_view({'get':'list'})),
        url(r'^expenses/(?P<year>[0-9]{4})/(?P<month>[0-9]{1,2})$', ExpenseViewSet.as_view({'get':'list'})),
        url(r'^expenses/(?P<year>[0-9]{4})$', ExpenseViewSet.as_view({'get':'list'})),

        ]

urlpatterns += router.urls
