from django.db import models


class Flavor(models.Model):
    name = models.CharField(max_length=100, unique=True)
    price = models.DecimalField(max_digits=6, decimal_places=2, default=2.00)

    def __str__(self):
        return self.name
