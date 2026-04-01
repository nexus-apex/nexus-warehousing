from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from core.models import Zone, InventoryItem, PickList
from datetime import date, timedelta
import random


class Command(BaseCommand):
    help = 'Seed NexusWarehousing with demo data'

    def handle(self, *args, **kwargs):
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser('admin', 'admin@nexuswarehousing.com', 'Admin@2024')
            self.stdout.write(self.style.SUCCESS('Admin user created'))

        if Zone.objects.count() == 0:
            for i in range(10):
                Zone.objects.create(
                    name=f"Sample Zone {i+1}",
                    warehouse=f"Sample {i+1}",
                    zone_type=random.choice(["receiving", "storage", "picking", "packing", "shipping"]),
                    capacity=random.randint(1, 100),
                    utilization=round(random.uniform(1000, 50000), 2),
                    temperature=random.choice(["ambient", "cold", "frozen"]),
                    active=random.choice([True, False]),
                )
            self.stdout.write(self.style.SUCCESS('10 Zone records created'))

        if InventoryItem.objects.count() == 0:
            for i in range(10):
                InventoryItem.objects.create(
                    name=f"Sample InventoryItem {i+1}",
                    sku=f"Sample {i+1}",
                    zone_name=f"Sample InventoryItem {i+1}",
                    quantity=random.randint(1, 100),
                    lot_number=f"Sample {i+1}",
                    expiry_date=date.today() - timedelta(days=random.randint(0, 90)),
                    last_counted=date.today() - timedelta(days=random.randint(0, 90)),
                    status=random.choice(["available", "reserved", "damaged"]),
                )
            self.stdout.write(self.style.SUCCESS('10 InventoryItem records created'))

        if PickList.objects.count() == 0:
            for i in range(10):
                PickList.objects.create(
                    pick_number=f"Sample {i+1}",
                    order_ref=f"Sample {i+1}",
                    zone_name=f"Sample PickList {i+1}",
                    items_count=random.randint(1, 100),
                    status=random.choice(["pending", "in_progress", "completed", "cancelled"]),
                    assigned_to=f"Sample {i+1}",
                    created_date=date.today() - timedelta(days=random.randint(0, 90)),
                )
            self.stdout.write(self.style.SUCCESS('10 PickList records created'))
