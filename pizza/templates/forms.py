from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.forms import ModelForm, ModelChoiceField
from .models import *
from django.db import transaction
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

class UserSignupForm(UserCreationForm):
  class Meta(UserCreationForm.Meta):
    model = User

  @transaction.atomic
  def save(self):
    user = super().save(commit=False)
    user.is_admin = False
    user.email = self.cleaned_data['username']
    user.save()
    return user

class UserLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(UserLoginForm, self).__init__(*args, **kwargs)


class PizzaForm(ModelForm):
  class Meta:
    model = Pizza
    fields = ["size", "sauce", "crust", "cheese",  "toppings"]



  size = forms.ModelChoiceField(queryset=Size.objects.all(), widget=forms.RadioSelect)

  sauce = forms.ModelChoiceField(queryset=Sauce.objects.all(), widget=forms.RadioSelect)

  cheese = forms.ModelChoiceField(queryset=Cheese.objects.all(), widget=forms.RadioSelect)

  crust = forms.ModelChoiceField(queryset=Crust.objects.all(), widget=forms.RadioSelect)

  toppings = forms.ModelMultipleChoiceField(queryset=Topping.objects.all(), widget=forms.CheckboxSelectMultiple)



  def save(self, user=None, commit=True):
    instance = super().save(commit=False)

    if commit:
      with transaction.atomic():
        instance.save()
        self.save_m2m()

        basket, created = Basket.objects.get_or_create(user=user, complete=False)

        basket.items.add(instance)

    return instance


class PremadePizza(forms.Form):
  class Meta:
    model = Pizza
    fields = ["size"]

  size = forms.ModelChoiceField(queryset=Size.objects.all(), empty_label="Select Size", label="Pizza Size")

  pizza_id = forms.IntegerField(widget=forms.HiddenInput())


