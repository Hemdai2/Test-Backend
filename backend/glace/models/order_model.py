from django.db import models
from glace.models import Flavor
import uuid


class Order(models.Model):
    order_code = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    comments = models.TextField(blank=True)

    def __str__(self):
        return f"Commande {self.order_code}"

    def total_price(self):
        return sum(s.price() for s in self.scoops.all())


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="scoops")
    flavor = models.ForeignKey(Flavor, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.quantity} boules de {self.flavor.name}"

    def price(self):
        return self.quantity * self.flavor.price
