from django.shortcuts import render, get_object_or_404
from django.http import Http404, JsonResponse
from django.core.paginator import Paginator
from django.db import models
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views import View
import json
import hashlib
from .models import Book, Record, NewsArticle, NewsletterSubscription, NewsletterIntegration

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
        
        # Get 5 random books from the same genre (excluding current book)
        related_books = []
        if book.genre:
            related_books = Book.objects.filter(
                genre=book.genre,
                status='available'
            ).exclude(id=book.id).order_by('?')[:5]
            
        context = {
            'book': book,
            'related_books': related_books,
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
    
    # Get unique genres for sidebar - filter out empty/null genres and get distinct values
    raw_genres = Book.objects.filter(
        condition='used', 
        status='available',
        genre__isnull=False
    ).exclude(genre='').values_list('genre', flat=True)
    
    # Convert to set to ensure uniqueness, then back to list and sort
    genres = sorted(list(set(raw_genres)))
    
    # Debug: print genres to see what we're getting
    print(f"Used Books - Raw genres: {list(raw_genres)}")
    print(f"Used Books - Unique genres: {genres}")
    
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
    
    # Get unique genres for sidebar - filter out empty/null genres and get distinct values
    raw_genres = Book.objects.filter(
        condition='new', 
        status='available',
        genre__isnull=False
    ).exclude(genre='').values_list('genre', flat=True)
    
    # Convert to set to ensure uniqueness, then back to list and sort
    genres = sorted(list(set(raw_genres)))
    
    # Debug: print genres to see what we're getting
    print(f"New Books - Raw genres: {list(raw_genres)}")
    print(f"New Books - Unique genres: {genres}")
    
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
    
    # Get unique genres for sidebar - filter out empty/null genres and get distinct values
    raw_genres = Record.objects.filter(
        status='available',
        genre__isnull=False
    ).exclude(genre='').values_list('genre', flat=True)
    
    # Convert to set to ensure uniqueness, then back to list and sort
    genres = sorted(list(set(raw_genres)))
    
    # Debug: print genres to see what we're getting
    print(f"Records - Raw genres: {list(raw_genres)}")
    print(f"Records - Unique genres: {genres}")
    
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

def news_listing(request):
    """View for news listing page"""
    # Get published news articles
    news_articles = NewsArticle.objects.filter(status='published').order_by('-publish_date')
    
    # Pagination
    paginator = Paginator(news_articles, 9)  # 9 articles per page (3 rows of 3)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'news_articles': page_obj,
    }
    
    return render(request, 'home/news_listing.html', context)

def news_detail(request, news_slug):
    """View for individual news article"""
    try:
        article = NewsArticle.objects.get(slug=news_slug, status='published')
        
        # Get 3 related articles (excluding current)
        related_articles = NewsArticle.objects.filter(
            status='published'
        ).exclude(id=article.id).order_by('-publish_date')[:3]
        
        context = {
            'article': article,
            'related_articles': related_articles,
        }
        return render(request, 'home/news_detail.html', context)
    except NewsArticle.DoesNotExist:
        raise Http404("News article not found")


@require_http_methods(["POST"])
def newsletter_subscribe(request):
    """Handle newsletter subscription via AJAX"""
    try:
        data = json.loads(request.body)
        email = data.get('email', '').strip().lower()
        
        if not email:
            return JsonResponse({'success': False, 'message': 'Email address is required.'}, status=400)
        
        # Validate email format
        from django.core.validators import validate_email
        from django.core.exceptions import ValidationError
        try:
            validate_email(email)
        except ValidationError:
            return JsonResponse({'success': False, 'message': 'Please enter a valid email address.'}, status=400)
        
        # Check if email already exists
        subscription, created = NewsletterSubscription.objects.get_or_create(
            email=email,
            defaults={'is_active': True, 'source': 'website'}
        )
        
        if not created:
            if subscription.is_active:
                return JsonResponse({'success': False, 'message': 'This email is already subscribed.'}, status=400)
            else:
                # Reactivate subscription
                subscription.is_active = True
                subscription.save()
        
        # Sync with third-party integrations if active
        sync_success = False
        sync_message = ""
        try:
            active_integration = NewsletterIntegration.objects.filter(is_active=True).first()
            if active_integration and active_integration.integration_type == 'mailchimp':
                sync_success, sync_message = sync_to_mailchimp(email, active_integration)
        except Exception as e:
            # Log error but don't fail the subscription
            print(f"Error syncing to integration: {str(e)}")
        
        return JsonResponse({
            'success': True, 
            'message': 'Thank you for subscribing! You will receive our latest updates.',
            'sync_status': sync_success,
            'sync_message': sync_message
        })
        
    except json.JSONDecodeError:
        return JsonResponse({'success': False, 'message': 'Invalid request data.'}, status=400)
    except Exception as e:
        return JsonResponse({'success': False, 'message': 'An error occurred. Please try again later.'}, status=500)


def sync_to_mailchimp(email, integration):
    """Sync email subscription to Mailchimp"""
    try:
        import requests
        
        if not integration.mailchimp_api_key or not integration.mailchimp_list_id:
            return False, "Mailchimp credentials not configured"
        
        # Extract server prefix from API key or use provided one
        server_prefix = integration.mailchimp_server_prefix
        if not server_prefix and integration.mailchimp_api_key:
            # Try to extract from API key format (key-server)
            parts = integration.mailchimp_api_key.split('-')
            if len(parts) > 1:
                server_prefix = parts[-1]
        
        if not server_prefix:
            return False, "Mailchimp server prefix not configured"
        
        mailchimp_url = f"https://{server_prefix}.api.mailchimp.com/3.0/lists/{integration.mailchimp_list_id}/members"
        
        # Check if member already exists
        subscriber_hash = hashlib.md5(email.lower().encode()).hexdigest()
        check_url = f"https://{server_prefix}.api.mailchimp.com/3.0/lists/{integration.mailchimp_list_id}/members/{subscriber_hash}"
        
        headers = {
            'Authorization': f'Bearer {integration.mailchimp_api_key}',
            'Content-Type': 'application/json'
        }
        
        # Check existing member
        response = requests.get(check_url, headers=headers)
        
        if response.status_code == 200:
            # Member exists, update status
            update_data = {
                'status': 'subscribed',
                'email_address': email
            }
            response = requests.patch(check_url, headers=headers, json=update_data)
        elif response.status_code == 404:
            # Member doesn't exist, create new
            member_data = {
                'email_address': email,
                'status': 'subscribed'
            }
            response = requests.post(mailchimp_url, headers=headers, json=member_data)
        else:
            return False, f"Mailchimp API error: {response.status_code}"
        
        if response.status_code in [200, 201]:
            return True, "Successfully synced to Mailchimp"
        else:
            error_data = response.json() if response.text else {}
            error_msg = error_data.get('detail', 'Unknown error')
            return False, f"Mailchimp sync failed: {error_msg}"
            
    except ImportError:
        return False, "Requests library not installed. Install with: pip install requests"
    except Exception as e:
        return False, f"Mailchimp sync error: {str(e)}"
