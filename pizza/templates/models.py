from django.db import models


class Size(models.Model):
  id=models.SmallAutoField(primary_key=True)
  name = models.CharField(max_length=10)
  price_multiplier = models.DecimalField(max_digits=3, decimal_places=2, default=1)

class Pizza(models.Model):
  id=models.SmallAutoField(primary_key=True)
  name = models.CharField(max_length=30)
  price = models.DecimalField(max_digits=4, decimal_places=2, default=12)
  image = models.ImageField(upload_to='images/')
