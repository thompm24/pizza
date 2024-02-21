from .models import *
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.forms import ModelForm, ModelChoiceField
from django.db import transaction

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = [ 'title', 'author', 'genre', 'price']

    def clean(self):
        data = self.cleaned_data
        title = data['title']
        author = data['author']
        book_exists = Book.objects.filter(title=title).exists()
        if book_exists:
            raise forms.ValidationError(f"The book {title} already exists in the database")
        return data
    
class BookEditForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = [ 'title', 'author', 'genre', 'price']

    def clean(self):
        data = self.cleaned_data
        title = data['title']
        author = data['author']
        return data
        


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
    