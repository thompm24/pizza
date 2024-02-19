from django.urls import path
from . import views
from .views import *
from .forms import *


urlpatterns = [
	path('', views.index, name="index"),
  path('create_pizza', views.create_pizza, name='create_pizza'),
  path('basket', views.basket, name='basket'),
	path('pizzas', views.all_pizzas, name='all_pizzas'),
  path('pizza/<int:pizza_id>', views.pizza),
  path('register/', views.UserSignupView.as_view(), name="register"),
  path('login/',views.LoginView.as_view(template_name="login.html", authentication_form=UserLoginForm), name='login'),
 path('logout/', views.logout_user, name="logout"),
]
