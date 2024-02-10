from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.forms import ModelForm, ModelChoiceField
from .models import User
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
