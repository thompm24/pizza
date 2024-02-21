import re
from django.shortcuts import render, get_object_or_404
import random
from .models import *
from .forms import *
from django.views.generic import CreateView
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required


# Create your views here.

def index(request):
    count  = random.randint(0,100)
    countb = random.randint(100,1000)
    return render(request, 'index.html',{'count':count, 'another':countb} )

def contact(request):
    return render(request, 'contact.html')


def counter(request):
    x = [y for y in range(0,100) if y%2==0] # list of all even numbers between 0 and 100
    return render(request, 'counter.html', {'items':x})

def all_books(request):
    # select * from book
    books = Book.objects.all()
    return render(request, 'books.html', {'books':books})


def single_book(request, bookid):
    # I know i want to get the book where id = bookid
    book = get_object_or_404(Book, id=bookid) # Book.objects.get(id=bookid)
    return render(request, 'book.html', {'book':book})


def single_author(request, authorid):
    author = get_object_or_404(Author, id=authorid)
    return render(request, 'author.html', {'author':author})


@login_required
def create_book(request):
    user = request.user
    if not user.is_superuser:
        return redirect("/") # bounce the user back to the homepage

    if request.method == "POST":
        form = BookForm(request.POST)
        if form.is_valid():
            new_book = form.save()
            return render(request, 'message.html', {'message.html': f"{new_book.title} created sucessfully"})
        else:
            return render(request, 'create_book.html', {'form':form})
    else:
    #     # its a GET request
    #     # load a new instance of the BookForm 
    #     # show it to the user
        form = BookForm()
        return render(request, 'create_book.html', {'form': form})
    

def edit_book(request,bookid):
    book = get_object_or_404(Book, id=bookid)
    if request.method == "POST":
        form = BookEditForm(request.POST, instance=book)# create form with existing data from book
        if form.is_valid():
            new_book = form.save()
            return render(request, 'message.html', {'message': f"Book f{new_book.title} updated sucessfully"})
        else:
            return render(request, 'create_book.html', {'form':form})
    else:
    #     # its a GET request
    #     # load a new instance of the BookForm 
    #     # show it to the user
        form = BookEditForm(instance=book)
        return render(request, 'create_book.html', {'form': form})
    



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



@login_required
def buy_book(request, bookid):
    # get the book (or 404)
    book = get_object_or_404(Book, id=bookid)
    # get the user 
    user = request.user
    # create a new isntance of BookUser
    newBookUser = BookUser.objects.create(book=book, user=user)
    newBookUser.save()
    # show some confirmation
    return render(request, 'confirmation.html', { 
                                                 'book': book, 'bookuser': newBookUser})

@login_required
def previous_orders(request):
    user = request.user
    orders = BookUser.objects.filter(user=user)
    return render(request, 'previous_orders.html', {'orders':orders})


