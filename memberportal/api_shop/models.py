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

    def __str__(self):
        return f"{{ self.name }} - {{ self.description }}"


class Transaction(models.Model):
    pass
