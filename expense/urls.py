from rest_framework.routers import SimpleRouter
from django.conf.urls import patterns, include, url
from .views import ExpenseViewSet, expense_csv


router = SimpleRouter(trailing_slash=False)
router.register(r'expense', ExpenseViewSet)
router.register(r'sharedexpense', ExpenseViewSet)

urlpatterns = patterns('',
        url(r'^expensecsv$', expense_csv))
