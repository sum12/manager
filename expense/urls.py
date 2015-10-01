from rest_framework.routers import SimpleRouter
from django.conf.urls import patterns, include, url
from .views import ExpenseViewSet, expense_csv


router = SimpleRouter(trailing_slash=False)
router.register(r'expense', ExpenseViewSet, base_name='expense')
#router.register(r'sharedexpense', ExpenseViewSet)

urlpatterns = patterns('',
        url(r'^expense/(?P<year>[0-9]{4})/(?P<month>[0-9]{1,2})/(?P<day>[0-9]{1,2})$', ExpenseViewSet.as_view({'get':'list'})),
        url(r'^expense/(?P<year>[0-9]{4})/(?P<month>[0-9]{1,2})$', ExpenseViewSet.as_view({'get':'list'})),
        url(r'^expense/(?P<year>[0-9]{4})$', ExpenseViewSet.as_view({'get':'list'})),
        
        url(r'^expensecsv/(?P<year>[0-9]{4})/(?P<month>[0-9]{2})/(?P<day>[0-9]{2})$', expense_csv),
        url(r'^expensecsv/(?P<year>[0-9]{4})/(?P<month>[0-9]{2})$', expense_csv),
        url(r'^expensecsv/(?P<year>[0-9]{4})$', expense_csv),
        url(r'^expensecsv$', expense_csv),
        )

urlpatterns += router.urls
