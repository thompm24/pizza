from django.contrib import admin
from .models import *
# Register your models here.

class PizzaAdmin(admin.ModelAdmin):
  readlony_fields = ('id',)

admin.site.register(Pizza, PizzaAdmin)
admin.site.register(Size)
admin.site.register(Sauce)
admin.site.register(Crust)
admin.site.register(Cheese)
admin.site.register(Topping)
admin.site.register(Basket)
