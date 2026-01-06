from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Asset, InventoryItem, Assignment, RepairTicket
from .serializers import *
from users.permissions import IsAdmin
from .permissions import IsAdminUserRole
from rest_framework.viewsets import ModelViewSet
from .serializers import AssetSerializer


from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated

class AssetViewSet(ModelViewSet):
    serializer_class = AssetSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role == "ADMIN":
            return Asset.objects.all()
        return Asset.objects.filter(
            assignment__employee=user
        )

    @action(detail=False, methods=["get"], url_path="assigned")
    def assigned_assets(self, request):
        assets = self.get_queryset()
        serializer = self.get_serializer(assets, many=True)
        return Response(serializer.data)



class InventoryViewSet(viewsets.ModelViewSet):
    queryset = InventoryItem.objects.all()
    serializer_class = InventorySerializer
    permission_classes = [IsAdmin]


from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from .models import Assignment, Asset
from .serializers import AssignmentSerializer
from users.permissions import IsAdmin

class AssignmentViewSet(ModelViewSet):
    serializer_class = AssignmentSerializer
    permission_classes = [IsAuthenticated, IsAdmin]
    queryset = Assignment.objects.all()

    def perform_create(self, serializer):
        assignment = serializer.save()
        asset = assignment.asset
        asset.status = "ASSIGNED"
        asset.save()



class RepairTicketViewSet(viewsets.ModelViewSet):
    queryset = RepairTicket.objects.all()
    serializer_class = RepairTicketSerializer
    permission_classes = [IsAuthenticated]


from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Asset, InventoryItem, Assignment, RepairTicket
from users.models import User

class DashboardAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        role = user.role

        data = {}

        # ================= ADMIN =================
        if role == "ADMIN":
            data = {
                "total_assets": Asset.objects.count(),
                "inventory_items": InventoryItem.objects.count(),
                "assigned_assets": Assignment.objects.filter(date_returned__isnull=True).count(),
                "low_stock": InventoryItem.objects.filter(quantity__lte=5).count(),
                "open_tickets": RepairTicket.objects.exclude(status="CLOSED").count(),

                "asset_chart": {
                    "AVAILABLE": Asset.objects.filter(status="AVAILABLE").count(),
                    "ASSIGNED": Asset.objects.filter(status="ASSIGNED").count(),
                    "UNDER_REPAIR": Asset.objects.filter(status="UNDER_REPAIR").count(),
                    "RETIRED": Asset.objects.filter(status="RETIRED").count(),
                },

                "ticket_chart": {
                    "OPEN": RepairTicket.objects.filter(status="OPEN").count(),
                    "IN_PROGRESS": RepairTicket.objects.filter(status="IN_PROGRESS").count(),
                    "CLOSED": RepairTicket.objects.filter(status="CLOSED").count(),
                },
            }

        # ================= EMPLOYEE =================
        elif role == "EMPLOYEE":
            data = {
                "my_assets": Assignment.objects.filter(
                    employee=user, date_returned__isnull=True
                ).count(),
                "my_tickets": RepairTicket.objects.filter(asset__assignment__employee=user).count(),
            }

        # ================= TECHNICIAN =================
        elif role == "TECHNICIAN":
            data = {
                "assigned_tickets": RepairTicket.objects.filter(
                    assigned_technician=user
                ).count(),
                "pending_repairs": RepairTicket.objects.filter(
                    assigned_technician=user, status="OPEN"
                ).count(),
                "completed_repairs": RepairTicket.objects.filter(
                    assigned_technician=user, status="CLOSED"
                ).count(),
            }

        return Response(data)

# Ticket ViewSet with context for request user
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status

from .models import RepairTicket
from .serializers import TicketSerializer
from users.models import User
from users.permissions import IsAdmin


class TicketViewSet(ModelViewSet):
    serializer_class = TicketSerializer
    permission_classes = [IsAuthenticated]

    # 🔹 Ticket visibility
    def get_queryset(self):
        user = self.request.user

        if user.role == "ADMIN":
            return RepairTicket.objects.all()

        if user.role == "TECHNICIAN":
            return RepairTicket.objects.filter(assigned_technician=user)

        # EMPLOYEE
        return RepairTicket.objects.filter(created_by=user)

    # 🔹 Employee creates ticket → OPEN
    def perform_create(self, serializer):
        serializer.save(
            created_by=self.request.user,
            status="OPEN"
        )

    # 🔹 Admin assigns technician → IN_PROGRESS
    @action(detail=True, methods=["post"], permission_classes=[IsAdmin])
    def assign(self, request, pk=None):
        ticket = self.get_object()
        technician_id = request.data.get("technician_id")

        if not technician_id:
            return Response(
                {"error": "technician_id is required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            technician = User.objects.get(
                id=technician_id,
                role="TECHNICIAN"
            )
        except User.DoesNotExist:
            return Response(
                {"error": "Valid technician not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        ticket.assigned_technician = technician
        ticket.status = "IN_PROGRESS"          # ✅ STATUS UPDATE
        ticket.save()

        # Optional but recommended: Asset → MAINTENANCE
        ticket.asset.status = "MAINTENANCE"
        ticket.asset.save()

        return Response(
            {"message": "Technician assigned. Ticket in progress."},
            status=status.HTTP_200_OK
        )

    # 🔹 Technician resolves ticket → RESOLVED
    @action(detail=True, methods=["post"], permission_classes=[IsAuthenticated])
    def resolve(self, request, pk=None):
        ticket = self.get_object()
        user = request.user

        if user.role != "TECHNICIAN":
            return Response(
                {"error": "Only technician can resolve ticket"},
                status=status.HTTP_403_FORBIDDEN
            )

        if ticket.assigned_technician != user:
            return Response(
                {"error": "This ticket is not assigned to you"},
                status=status.HTTP_403_FORBIDDEN
            )

        ticket.status = "RESOLVED"
        ticket.save()

        return Response(
            {"message": "Ticket marked as resolved"},
            status=status.HTTP_200_OK
        )

    # 🔹 Admin verifies & closes ticket → CLOSED
    @action(detail=True, methods=["post"], permission_classes=[IsAdmin])
    def close(self, request, pk=None):
        ticket = self.get_object()

        if ticket.status != "RESOLVED":
            return Response(
                {"error": "Only resolved tickets can be closed"},
                status=status.HTTP_400_BAD_REQUEST
            )

        ticket.status = "CLOSED"
        ticket.save()

        # Asset back to ASSIGNED
        ticket.asset.status = "ASSIGNED"
        ticket.asset.save()

        return Response(
            {"message": "Ticket closed successfully"},
            status=status.HTTP_200_OK
        )
