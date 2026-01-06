from django.db import models
from users.models import User


# ======================
# Asset Model
# ======================
class Asset(models.Model):

    STATUS_CHOICES = (
        ('AVAILABLE', 'Available'),
        ('ASSIGNED', 'Assigned'),
        ('UNDER_REPAIR', 'Under Repair'),
    )

    name = models.CharField(max_length=100)
    type = models.CharField(max_length=100)
    serial_number = models.CharField(max_length=100, unique=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='AVAILABLE')
    purchase_date = models.DateField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.serial_number})"


# ======================
# Inventory Item Model
# ======================
class InventoryItem(models.Model):

    item_name = models.CharField(max_length=100)
    quantity = models.PositiveIntegerField()
    threshold = models.PositiveIntegerField(help_text="Minimum stock alert level")

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.item_name


# ======================
# Asset Assignment Model
# ======================
class Assignment(models.Model):

    asset = models.ForeignKey(Asset, on_delete=models.CASCADE)
    employee = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        limit_choices_to={'role': 'EMPLOYEE'}
    )
    date_assigned = models.DateField(auto_now_add=True)
    date_returned = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.asset.name} → {self.employee.email}"

class RepairTicket(models.Model):

    STATUS_CHOICES = (
        ("OPEN", "Open"),
        ("IN_PROGRESS", "In Progress"),
        ("RESOLVED", "Resolved"),
        ("CLOSED", "Closed"),
    )

    asset = models.ForeignKey(Asset, on_delete=models.CASCADE)
    issue = models.TextField()

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="OPEN"
    )

    created_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="created_repair_tickets"
    )

    assigned_technician = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="assigned_repair_tickets"
    )

    created_at = models.DateTimeField(auto_now_add=True)
