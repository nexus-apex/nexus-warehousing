from django.db import models

class Zone(models.Model):
    name = models.CharField(max_length=255)
    warehouse = models.CharField(max_length=255, blank=True, default="")
    zone_type = models.CharField(max_length=50, choices=[("receiving", "Receiving"), ("storage", "Storage"), ("picking", "Picking"), ("packing", "Packing"), ("shipping", "Shipping")], default="receiving")
    capacity = models.IntegerField(default=0)
    utilization = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    temperature = models.CharField(max_length=50, choices=[("ambient", "Ambient"), ("cold", "Cold"), ("frozen", "Frozen")], default="ambient")
    active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.name

class InventoryItem(models.Model):
    name = models.CharField(max_length=255)
    sku = models.CharField(max_length=255, blank=True, default="")
    zone_name = models.CharField(max_length=255, blank=True, default="")
    quantity = models.IntegerField(default=0)
    lot_number = models.CharField(max_length=255, blank=True, default="")
    expiry_date = models.DateField(null=True, blank=True)
    last_counted = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=50, choices=[("available", "Available"), ("reserved", "Reserved"), ("damaged", "Damaged")], default="available")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.name

class PickList(models.Model):
    pick_number = models.CharField(max_length=255)
    order_ref = models.CharField(max_length=255, blank=True, default="")
    zone_name = models.CharField(max_length=255, blank=True, default="")
    items_count = models.IntegerField(default=0)
    status = models.CharField(max_length=50, choices=[("pending", "Pending"), ("in_progress", "In Progress"), ("completed", "Completed"), ("cancelled", "Cancelled")], default="pending")
    assigned_to = models.CharField(max_length=255, blank=True, default="")
    created_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.pick_number
