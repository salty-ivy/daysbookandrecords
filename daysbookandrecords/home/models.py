from django.db import models
from wagtail.models import Page
from wagtail.fields import RichTextField
from wagtail.admin.panels import FieldPanel, MultiFieldPanel
from wagtail.search import index
from taggit.models import TaggedItemBase
from modelcluster.contrib.taggit import ClusterTaggableManager
from modelcluster.models import ClusterableModel
from modelcluster.fields import ParentalKey
from django.contrib.auth.models import User

# Custom tag models for genre/sub-genre
class BookGenreTag(TaggedItemBase):
    content_object = ParentalKey('Book', related_name='genre_tags', on_delete=models.CASCADE)

class BookSubGenreTag(TaggedItemBase):
    content_object = ParentalKey('Book', related_name='sub_genre_tags', on_delete=models.CASCADE)

class RecordGenreTag(TaggedItemBase):
    content_object = ParentalKey('Record', related_name='genre_tags', on_delete=models.CASCADE)

class RecordSubGenreTag(TaggedItemBase):
    content_object = ParentalKey('Record', related_name='sub_genre_tags', on_delete=models.CASCADE)

# Book model
class Book(ClusterableModel):
    STATUS_CHOICES = [
        ('available', 'Available'),
        ('sold', 'Sold'),
        ('reserved', 'Reserved'),
    ]

    CONDITION_CHOICES = [
        ('new', 'New'),
        ('used', 'Used'),
    ]

    image = models.ImageField(upload_to='books/', blank=True, null=True)
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    publisher = models.CharField(max_length=200, blank=True)
    genre = models.CharField(max_length=100)
    sub_genre = ClusterTaggableManager(through=BookSubGenreTag, blank=True)
    condition = models.CharField(max_length=10, choices=CONDITION_CHOICES, default='used')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    isbn = models.CharField(max_length=20, blank=True)
    description = RichTextField(blank=True)
    link = models.URLField(blank=True)
    featured = models.BooleanField(default=False)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='available')
    added_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='books_added')
    updated_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='books_updated', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def get_slug(self):
        """Generate a URL-friendly slug from the book title"""
        import re
        slug = re.sub(r'[^\w\s-]', '', self.title.lower())
        slug = re.sub(r'[-\s]+', '-', slug)
        return slug.strip('-')
    
    def get_absolute_url(self):
        """Get the absolute URL for the book detail page"""
        return f'/item/books/{self.get_slug()}/'

    def __str__(self):
        return f"{self.title} by {self.author}"

    class Meta:
        ordering = ['-created_at']

# Record model
class Record(ClusterableModel):
    STATUS_CHOICES = [
        ('available', 'Available'),
        ('sold', 'Sold'),
        ('reserved', 'Reserved'),
    ]

    CONDITION_CHOICES = [
        ('new', 'New'),
        ('used', 'Used'),
    ]

    FORMAT_CHOICES = [
        ('LP', 'LP'),
        ('Singles', 'Singles'),
        ('7"', '7"'),
        ('10"', '10"'),
        ('12"', '12"'),
    ]

    image = models.ImageField(upload_to='records/', blank=True, null=True)
    title = models.CharField(max_length=200)
    artist = models.CharField(max_length=200)
    label = models.CharField(max_length=200, blank=True)
    genre = models.CharField(max_length=100)
    sub_genre = ClusterTaggableManager(through=RecordSubGenreTag, blank=True)
    condition = models.CharField(max_length=10, choices=CONDITION_CHOICES, default='used')
    format = models.CharField(max_length=10, choices=FORMAT_CHOICES, default='LP')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    cat_number = models.CharField(max_length=50, blank=True, verbose_name="Catalog Number")
    description = RichTextField(blank=True)
    link = models.URLField(blank=True)
    featured = models.BooleanField(default=False)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='available')
    added_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='records_added')
    updated_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='records_updated', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def get_slug(self):
        """Generate a URL-friendly slug from the record title"""
        import re
        slug = re.sub(r'[^\w\s-]', '', self.title.lower())
        slug = re.sub(r'[-\s]+', '-', slug)
        return slug.strip('-')
    
    def get_absolute_url(self):
        """Get the absolute URL for the record detail page"""
        return f'/item/records/{self.get_slug()}/'

    def __str__(self):
        return f"{self.title} by {self.artist}"

    class Meta:
        ordering = ['-created_at']

# Wagtail Page models
class HomePage(Page):
    intro = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('intro'),
    ]

    def get_context(self, request):
        context = super().get_context(request)
        # Get recent used books and new books for display
        context['recent_used_books'] = Book.objects.filter(featured=1, condition='used')[:6]
        context['recent_new_books'] = Book.objects.filter(featured=1, condition='new')[:6]
        context['recent_records'] = Record.objects.filter(featured=1)
        return context

class BooksPage(Page):
    intro = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('intro'),
    ]

    def get_context(self, request):
        context = super().get_context(request)
        books = Book.objects.filter(status='available')

        # Filter by genre if specified
        genre = request.GET.get('genre')
        if genre:
            books = books.filter(genre__icontains=genre)

        # Search functionality
        search_query = request.GET.get('search')
        if search_query:
            books = books.filter(
                models.Q(title__icontains=search_query) |
                models.Q(author__icontains=search_query) |
                models.Q(description__icontains=search_query)
            )

        context['books'] = books
        context['genres'] = Book.objects.values_list('genre', flat=True).distinct()
        return context

class RecordsPage(Page):
    intro = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('intro'),
    ]

    def get_context(self, request):
        context = super().get_context(request)
        records = Record.objects.filter(status='available')

        # Filter by genre if specified
        genre = request.GET.get('genre')
        if genre:
            records = records.filter(genre__icontains=genre)

        # Search functionality
        search_query = request.GET.get('search')
        if search_query:
            records = records.filter(
                models.Q(title__icontains=search_query) |
                models.Q(artist__icontains=search_query) |
                models.Q(description__icontains=search_query)
            )

        context['records'] = records
        context['genres'] = Record.objects.values_list('genre', flat=True).distinct()
        return context

class AboutPage(Page):
    body = RichTextField()

    content_panels = Page.content_panels + [
        FieldPanel('body'),
    ]

class NewsPage(Page):
    body = RichTextField()

    content_panels = Page.content_panels + [
        FieldPanel('body'),
    ]

class ContactPage(Page):
    body = RichTextField()
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=20, blank=True)
    address = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('body'),
        MultiFieldPanel([
            FieldPanel('email'),
            FieldPanel('phone'),
            FieldPanel('address'),
        ], heading="Contact Information"),
    ]