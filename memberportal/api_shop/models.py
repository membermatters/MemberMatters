from django.core.exceptions import ValidationError
from django.db import models
from django.conf import settings


class Category(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return f"{{ self.name }} - {{ self.description }}"


class Supplier(models.Model):
    name = models.CharField(max_length=255)
    website = models.URLField(max_length=255)

    def __str__(self):
        f"{{ self.name }} - {{ self.website }}"


class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    buy_price = models.DecimalField(max_digits=6, decimal_places=2)
    sell_price = models.DecimalField(max_digits=6, decimal_places=2)
    memberbucks_only = models.BooleanField(default=True)

    def __str__(self):
        return f"{{ self.name }} - {{ self.description }} - {{ self.sell_price }}"


class Transaction(models.Model):
    pass
