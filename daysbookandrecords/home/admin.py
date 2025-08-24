# admin.py
from django.contrib import admin
from .models import Book, Record, NewsArticle

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'genre', 'condition', 'price', 'status', 'created_at']
    list_filter = ['genre', 'condition', 'status', 'created_at']
    search_fields = ['title', 'author', 'isbn']
    readonly_fields = ['created_at', 'updated_at']

    def save_model(self, request, obj, form, change):
        if not change:  # Creating new object
            obj.added_by = request.user
        obj.updated_by = request.user
        super().save_model(request, obj, form, change)

@admin.register(Record)
class RecordAdmin(admin.ModelAdmin):
    list_display = ['title', 'artist', 'genre', 'condition', 'format', 'price', 'status', 'created_at']
    list_filter = ['genre', 'condition', 'format', 'status', 'created_at']
    search_fields = ['title', 'artist', 'cat_number']
    readonly_fields = ['created_at', 'updated_at']

    def save_model(self, request, obj, form, change):
        if not change:  # Creating new object
            obj.added_by = request.user
        obj.updated_by = request.user
        super().save_model(request, obj, form, change)

@admin.register(NewsArticle)
class NewsArticleAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'publish_date', 'status', 'featured', 'created_at']
    list_filter = ['status', 'featured', 'publish_date', 'created_at']
    search_fields = ['title', 'author', 'content', 'excerpt']
    readonly_fields = ['created_at', 'updated_at']
    date_hierarchy = 'publish_date'
    exclude = ['slug']
    
    fieldsets = (
        ('Content', {
            'fields': ('title', 'author', 'content', 'excerpt')
        }),
        ('Media', {
            'fields': ('featured_image',)
        }),
        ('Publishing', {
            'fields': ('publish_date', 'status', 'featured')
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def save_model(self, request, obj, form, change):
        """Auto-generate slug from title if not provided or if title changed"""
        if not obj.slug or (change and 'title' in form.changed_data):
            # Import here to avoid circular imports
            from django.utils.text import slugify
            from django.db import IntegrityError
            
            base_slug = slugify(obj.title)
            obj.slug = base_slug
            
            # Ensure slug uniqueness
            counter = 1
            while True:
                try:
                    # Check if slug exists (excluding current object if editing)
                    if change:
                        existing = NewsArticle.objects.filter(slug=obj.slug).exclude(id=obj.id)
                    else:
                        existing = NewsArticle.objects.filter(slug=obj.slug)
                    
                    if not existing.exists():
                        break
                    
                    obj.slug = f"{base_slug}-{counter}"
                    counter += 1
                except IntegrityError:
                    obj.slug = f"{base_slug}-{counter}"
                    counter += 1
        
        super().save_model(request, obj, form, change)
