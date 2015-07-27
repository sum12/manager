from rest_framework.routers import SimpleRouter
from .views import ExpenseViewSet


router = SimpleRouter(trailing_slash=False)
router.register(r'expense', ExpenseViewSet)
router.register(r'sharedexpense', ExpenseViewSet)


