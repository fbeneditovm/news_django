from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import EmployeeViewSet, ClientUserViewSet 

router = DefaultRouter()
router.register(r'employees', EmployeeViewSet)
router.register(r'client-users', ClientUserViewSet)

urlpatterns = [
    path('', include(router.urls)),
]