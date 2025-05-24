from django.db import models
from glace.models import Flavor


class Tub(models.Model):
    flavor = models.OneToOneField(Flavor, on_delete=models.CASCADE, related_name="tub")
    scoops_left = models.PositiveIntegerField(default=40)
    capacity = models.PositiveIntegerField(default=40)

    def is_empty(self):
        return self.scoops_left == 0

    def consume_scoops(self, amount):
        if self.scoops_left < amount:
            self.notify_admin_due_to_low_scoops(amount=amount)
            raise ValueError(
                f"Il ne reste plus assez de boules pour {self.flavor.name}. Il ne reste que {self.scoops_left}."
            )
        self.scoops_left -= amount
        self.save()

    def refill(self, qty=None):
        if qty:
            self.scoops_left += qty
        else:
            self.scoops_left = self.capacity
        self.save()

    def notify_admin_of_low_scoops(self):
        print(f"⚠️ Le pot de glace '{self.flavor.name}' est vide! Veuillez le remplir.")

    def notify_admin_due_to_low_scoops(self, amount):
        print(
            f"⚠️ Le pot de glace {self.flavor.name}  ne contient plus que {self.scoops_left} boules. il ne peut pas en servir {amount} boules."
        )

    def __str__(self):
        return f"{self.flavor.name} pot – {self.scoops_left} restants"
