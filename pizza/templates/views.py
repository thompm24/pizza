from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import *
from django.views.generic import CreateView
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from .forms import * 


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



class UserSignupView(CreateView):
    model = User
    form_class = UserSignupForm
    template_name = 'user_signup.html'

    def get_context_data(self, **kwargs):
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('/')


class UserLoginView(LoginView):
    template_name='login.html'


def logout_user(request):
    logout(request)
    return redirect("/")
