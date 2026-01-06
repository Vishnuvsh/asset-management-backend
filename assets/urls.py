from rest_framework.routers import DefaultRouter
from django.urls import path
from .views import (
    AssetViewSet,
    InventoryViewSet,
    AssignmentViewSet,
    TicketViewSet,
    DashboardAPIView,
)

router = DefaultRouter()

router.register("assets", AssetViewSet, basename="assets")
router.register("inventory", InventoryViewSet, basename="inventory")
router.register("assignments", AssignmentViewSet, basename="assignments")
router.register("tickets", TicketViewSet, basename="tickets")


urlpatterns = [
    *router.urls,
    path("dashboard/", DashboardAPIView.as_view(), name="dashboard"),
]