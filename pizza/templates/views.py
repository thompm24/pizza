from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import *

# Create your views here.
def index(request):
	return render(request, 'index.html')

def pizza(request, pizza_id):
	pizza =Pizza.objects.get(pk=pizza_id)
	if pizza is not None:
		return render(request, 'pizza.html', {'pizza': pizza})
	else:
		return Http404('Pizza does not exist')

def all_pizzas(request):
	all_pizzas = Pizza.objects.all()
	return render(request, 'all_pizzas.html', {'pizzas':all_pizzas})
