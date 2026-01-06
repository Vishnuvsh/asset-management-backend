from rest_framework.routers import DefaultRouter
from .views import EmployeeViewSet,TechnicianListView,UserProfileAPIView

router = DefaultRouter()
router.register('employees', EmployeeViewSet, basename='employees')

urlpatterns = router.urls

# view for user profile

from django.urls import path

urlpatterns += [
    path("profile/", UserProfileAPIView.as_view()),
    path("technicians/", TechnicianListView.as_view()),
]
