from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import *
from django.views.generic import CreateView
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from .forms import *
from datetime import *
from django.db.models import Sum
from django.views.decorators.http import require_POST

# Create your views here.
def index(request):
  baskets = []
  print("Hello")
  if request.user.is_authenticated:

    baskets = Basket.objects.filter(user = request.user, complete=True)



  print(baskets)
  return render(request, 'index.html', {'baskets' : baskets})




def pizza(request, pizza_id):
  pizza =Pizza.objects.get(pk=pizza_id)
  if pizza is not None:
    return render(request, 'pizza.html', {'pizza': pizza})
  else:
    return Http404('Pizza does not exist')


def basket(request):
    user = request.user
    basket = get_object_or_404(Basket, user=user, complete=False)
    total_price = basket.get_total()

    if request.method == 'POST':
        form = PizzaUserForm(request.POST)
        if form.is_valid():
            pizza_user = form.save(commit=False)
            pizza_user.basket = basket
            pizza_user.user = user
            pizza_user.save()

            basket.complete = True
            basket.save()

            # Prepare delivery context
            delivery_time = pizza_user.date_ordered + timedelta(minutes=30)
            context = {'delivery_time': delivery_time, 'basket': basket}
            return render(request, 'delivery.html', context)
        else:
            print("Form not valid")
            print(form.errors)
    else:
        form = PizzaUserForm()


    context = {'basket': basket, 'form' : form}
    return render(request, 'basket.html', context)




def create_pizza(request):
  form = PizzaForm()
  if request.method == 'POST':
    form = PizzaForm(request.POST)
    if form.is_valid():
      pizza_instance=form.save(commit=False)
      pizza_instance.name = "CYO Pizza"

      pizza_instance.save()

      price = pizza_instance.size.price + pizza_instance.cheese.price + pizza_instance.crust.price + pizza_instance.sauce.price
      toppings = form.cleaned_data['toppings']
      for topping in toppings:
        pizza_instance.toppings.add(topping)
        price += topping.price

      pizza_instance.price = price
      pizza_instance.save()

      basket, created = Basket.objects.get_or_create(user = request.user, complete=False)

      basket.items.add(pizza_instance)

      return redirect('all_pizzas')

  context = {'form' : form}
  return render(request, 'create_pizza.html', context)




@login_required
def all_pizzas(request):
  all_pizzas = Pizza.objects.order_by('id')[:6]
  form = PremadePizza()

  if request.method == "POST":
    form = PremadePizza(request.POST)
    print("FORM POSTED")


    if form.is_valid():
      print("Yippe yipee")
      pizza_id = form.cleaned_data['pizza_id']

      premade_pizza = get_object_or_404(Pizza, pk=pizza_id)

      pizza = premade_pizza
      pizza.pk = None
      pizza.save()

      pizza.size = form.cleaned_data['size']

      pizza.price = pizza.size.price


      basket, created = Basket.objects.get_or_create(user=request.user, complete=False)

      basket.items.add(pizza)

      return redirect(request.path)
    else:
      print(form.errors)

  return render(request, 'all_pizzas.html', {'pizzas':all_pizzas, 'form':form})


@login_required
def toggle_delivery(request):
  basket, create = Basket.objects.get_or_create(user=request.user, complete=False)

  if basket.delivery:
    basket.delivery = False
  else:
    basket.delivery = True


class UserSignupView(CreateView):
  model = User
  form_class = UserSignupForm
  template_name = 'user_signup.html'

  def get_context_data(self, **kwargs):
    return super().get_context_data(**kwargs)

  def form_valid(self, form):
    user = form.save()
    login(self.request, user)
    return redirect('index')


class UserLoginView(LoginView):
  template_name='login.html'

  def form_valid(self, form):
    super().form_valid(form)
    return redirect('index')

def logout_user(request):
  logout(request)
  return redirect("/")

