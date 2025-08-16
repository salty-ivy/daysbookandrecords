from django.urls import path
from . import views

app_name = 'home'

urlpatterns = [
    path('books/<str:book_slug>/', views.book_detail, name='book_detail'),
    path('records/<str:record_slug>/', views.record_detail, name='record_detail'),
    path('used-books/', views.used_books, name='used_books'),
    path('new-books/', views.new_books, name='new_books'),
]
