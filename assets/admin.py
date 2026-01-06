from django.contrib import admin
from .models import Asset, InventoryItem, Assignment, RepairTicket


@admin.register(Asset)
class AssetAdmin(admin.ModelAdmin):
    list_display = ('name', 'type', 'serial_number', 'status')
    list_filter = ('status', 'type')
    search_fields = ('name', 'serial_number')


@admin.register(InventoryItem)
class InventoryItemAdmin(admin.ModelAdmin):
    list_display = ('item_name', 'quantity', 'threshold')
    search_fields = ('item_name',)


@admin.register(Assignment)
class AssignmentAdmin(admin.ModelAdmin):
    list_display = ('asset', 'employee', 'date_assigned', 'date_returned')
    list_filter = ('date_assigned',)


@admin.register(RepairTicket)
class RepairTicketAdmin(admin.ModelAdmin):
    list_display = ('asset', 'status', 'assigned_technician', 'created_at')
    list_filter = ('status',)
