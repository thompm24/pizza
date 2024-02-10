from django.urls import path
from . import views
from .views import *



urlpatterns = [
	path('', views.index, name="index"),
	path('pizzas', views.all_pizzas, name='all_pizzas'),
        path('pizza/<int:pizza_id>', views.pizza)
]
