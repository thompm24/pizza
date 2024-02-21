from django.urls import path, include
from . import views
from .forms import * # add o imports at the top of the file

urlpatterns = [
    path('',views.index, name="index"),# mywebsite.com 
    path('contactus', views.contact, name="contact"), # mywebsite.com/contact 
    path('counter', views.counter, name="counter"),
    path('books', views.all_books, name="all_books"),
    path('books/<int:bookid>', views.single_book, name="single_book"),
    path('books/<int:bookid>/edit', views.edit_book, name="edit_book"),
    path('author/<int:authorid>', views.single_author, name="single_author"),
    path('books/create', views.create_book, name="create_book"),
    path('register/', views.UserSignupView.as_view(), name="register"),
    path('login/',views.LoginView.as_view(template_name="login.html", authentication_form=UserLoginForm)),
    path('logout/', views.logout_user, name="logout"),
    path('buy/<int:bookid>', views.buy_book, name="buy_book"),
    path('orders', views.previous_orders, name="previous_orders")

]