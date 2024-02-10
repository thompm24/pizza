from django.contrib import admin
from .models import *
# Register your models here.

class PizzaAdmin(admin.ModelAdmin):
  readlony_fields = ('id',)

admin.site.register(Pizza, PizzaAdmin)
admin.site.register(Size)
