
from django.urls import path
from book_management.views import *


urlpatterns = [
    path('add_books/', add_books, name="add_books"),
    path('add_members/', add_members, name="add_members"),
    path('checkout_book/', checkout_book, name="checkout_book"),
    path('return_book/', return_book, name="return_book"),
]
