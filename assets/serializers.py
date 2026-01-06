from rest_framework import serializers
from .models import Asset, InventoryItem, Assignment, RepairTicket


class AssetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Asset
        fields = "__all__"


class InventorySerializer(serializers.ModelSerializer):
    class Meta:
        model = InventoryItem
        fields = "__all__"


class AssignmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Assignment
        fields = "__all__"


from rest_framework import serializers
from .models import RepairTicket

class RepairTicketSerializer(serializers.ModelSerializer):
    asset_name = serializers.CharField(source="asset.name", read_only=True)
    technician_email = serializers.EmailField(
        source="assigned_technician.email",
        read_only=True
    )

    class Meta:
        model = RepairTicket
        fields = "__all__"



# Ticket Serializer

from rest_framework import serializers
from .models import RepairTicket
from users.models import User

class TechnicianSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "email"]



from rest_framework import serializers
from .models import RepairTicket

class TicketSerializer(serializers.ModelSerializer):
    asset_name = serializers.CharField(source="asset.name", read_only=True)
    technician_email = serializers.EmailField(
        source="assigned_technician.email",
        read_only=True
    )

    class Meta:
        model = RepairTicket
        fields = [
            "id",
            "issue",
            "status",
            "asset",
            "asset_name",
            "technician_email",
            "created_at",
        ]
