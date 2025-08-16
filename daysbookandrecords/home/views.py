from django.shortcuts import render, get_object_or_404
from django.http import Http404
from django.core.paginator import Paginator
from django.db import models
from .models import Book, Record

def book_detail(request, book_slug):
    """View for individual book detail page"""
    try:
        # Find book by slug
        book = None
        for book_obj in Book.objects.filter(status='available'):
            if book_obj.get_slug() == book_slug:
                book = book_obj
                break
        
        if not book:
            raise Http404("Book not found")
            
        context = {
            'book': book,
        }
        return render(request, 'home/book_detail.html', context)
    except Http404:
        # Handle case where book doesn't exist or is not available
        return render(request, 'home/book_detail.html', {'book': None})

def record_detail(request, record_slug):
    """View for individual record detail page"""
    try:
        # Find record by slug
        record = None
        for record_obj in Record.objects.filter(status='available'):
            if record_obj.get_slug() == record_slug:
                record = record_obj
                break
        
        if not record:
            raise Http404("Record not found")
            
        context = {
            'record': record,
        }
        return render(request, 'home/record_detail.html', context)
    except Http404:
        # Handle case where record doesn't exist or is not available
        return render(request, 'home/record_detail.html', {'record': None})

def used_books(request):
    """View for used books page"""
    # Get search and genre filters
    search_query = request.GET.get('search', '')
    genre_filter = request.GET.get('genre', '')
    
    # Filter books by condition (used) and status
    books = Book.objects.filter(condition='used', status='available')
    
    # Apply search filter
    if search_query:
        books = books.filter(title__icontains=search_query)
    
    # Apply genre filter
    if genre_filter:
        books = books.filter(genre=genre_filter)
    
    # Get unique genres for sidebar
    genres = Book.objects.filter(condition='used', status='available').values_list('genre', flat=True).distinct()
    
    # Pagination
    paginator = Paginator(books, 18)  # 18 books per page (6 rows of 3)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'books': page_obj,
        'genres': genres,
        'search_query': search_query,
        'genre_filter': genre_filter,
    }
    
    return render(request, 'home/used_books_page.html', context)

def new_books(request):
    """View for new books page"""
    # Get search and genre filters
    search_query = request.GET.get('search', '')
    genre_filter = request.GET.get('genre', '')
    
    # Filter books by condition (new) and status
    books = Book.objects.filter(condition='new', status='available')
    
    # Apply search filter
    if search_query:
        books = books.filter(title__icontains=search_query)
    
    # Apply genre filter
    if genre_filter:
        books = books.filter(genre=genre_filter)
    
    # Get unique genres for sidebar
    genres = Book.objects.filter(condition='new', status='available').values_list('genre', flat=True).distinct()
    
    # Pagination
    paginator = Paginator(books, 18)  # 18 books per page (6 rows of 3)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'books': page_obj,
        'genres': genres,
        'search_query': search_query,
        'genre_filter': genre_filter,
    }
    
    return render(request, 'home/new_books_page.html', context)

def records_view(request):
    """View for records page"""
    # Get search and genre filters
    search_query = request.GET.get('search', '')
    genre_filter = request.GET.get('genre', '')
    condition_filter = request.GET.get('condition', '')
    
    # Filter records by status
    records = Record.objects.filter(status='available')
    
    # Apply condition filter
    if condition_filter:
        records = records.filter(condition=condition_filter)
    
    # Apply search filter
    if search_query:
        records = records.filter(
            models.Q(title__icontains=search_query) |
            models.Q(artist__icontains=search_query) |
            models.Q(description__icontains=search_query)
        )
    
    # Apply genre filter
    if genre_filter:
        records = records.filter(genre=genre_filter)
    
    # Get unique genres for sidebar
    genres = Record.objects.filter(status='available').values_list('genre', flat=True).distinct()
    
    # Pagination
    paginator = Paginator(records, 18)  # 18 records per page (6 rows of 3)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'records': page_obj,
        'genres': genres,
        'search_query': search_query,
        'genre_filter': genre_filter,
        'condition_filter': condition_filter,
    }
    
    return render(request, 'home/records_page.html', context)

def cart_view(request):
    """View for cart page"""
    return render(request, 'home/cart_page.html')
