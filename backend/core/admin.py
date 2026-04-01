from django.contrib import admin
from .models import Zone, InventoryItem, PickList

@admin.register(Zone)
class ZoneAdmin(admin.ModelAdmin):
    list_display = ["name", "warehouse", "zone_type", "capacity", "utilization", "created_at"]
    list_filter = ["zone_type", "temperature"]
    search_fields = ["name", "warehouse"]

@admin.register(InventoryItem)
class InventoryItemAdmin(admin.ModelAdmin):
    list_display = ["name", "sku", "zone_name", "quantity", "lot_number", "created_at"]
    list_filter = ["status"]
    search_fields = ["name", "sku", "zone_name"]

@admin.register(PickList)
class PickListAdmin(admin.ModelAdmin):
    list_display = ["pick_number", "order_ref", "zone_name", "items_count", "status", "created_at"]
    list_filter = ["status"]
    search_fields = ["pick_number", "order_ref", "zone_name"]
