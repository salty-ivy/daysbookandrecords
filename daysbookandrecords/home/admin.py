# admin.py
from django.contrib import admin
from django.http import HttpResponse
from django.utils import timezone
import csv
from .models import Book, Record, NewsArticle, NewsletterSubscription, NewsletterIntegration

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


@admin.register(NewsletterSubscription)
class NewsletterSubscriptionAdmin(admin.ModelAdmin):
    list_display = ['email', 'subscribed_at', 'is_active', 'source']
    list_filter = ['is_active', 'source', 'subscribed_at']
    search_fields = ['email']
    readonly_fields = ['subscribed_at']
    date_hierarchy = 'subscribed_at'
    actions = ['export_to_csv', 'export_to_csv_all', 'deactivate_selected', 'activate_selected']
    
    fieldsets = (
        ('Subscription Information', {
            'fields': ('email', 'subscribed_at', 'is_active', 'source')
        }),
    )
    
    def export_to_csv(self, request, queryset):
        """Export selected subscriptions to CSV"""
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename="newsletter_subscriptions_{timezone.now().strftime("%Y%m%d_%H%M%S")}.csv"'
        
        writer = csv.writer(response)
        writer.writerow(['Email', 'Subscribed At', 'Status', 'Source'])
        
        for subscription in queryset:
            writer.writerow([
                subscription.email,
                subscription.subscribed_at.strftime('%Y-%m-%d %H:%M:%S'),
                'Active' if subscription.is_active else 'Inactive',
                subscription.source
            ])
        
        return response
    export_to_csv.short_description = "Export selected to CSV"
    
    def export_to_csv_all(self, request, queryset):
        """Export all active subscriptions to CSV"""
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename="newsletter_subscriptions_all_{timezone.now().strftime("%Y%m%d_%H%M%S")}.csv"'
        
        writer = csv.writer(response)
        writer.writerow(['Email', 'Subscribed At', 'Status', 'Source'])
        
        all_subscriptions = NewsletterSubscription.objects.filter(is_active=True).order_by('-subscribed_at')
        for subscription in all_subscriptions:
            writer.writerow([
                subscription.email,
                subscription.subscribed_at.strftime('%Y-%m-%d %H:%M:%S'),
                'Active' if subscription.is_active else 'Inactive',
                subscription.source
            ])
        
        return response
    export_to_csv_all.short_description = "Export all active subscriptions to CSV"
    
    def deactivate_selected(self, request, queryset):
        """Deactivate selected subscriptions"""
        updated = queryset.update(is_active=False)
        self.message_user(request, f'{updated} subscription(s) deactivated.')
    deactivate_selected.short_description = "Deactivate selected subscriptions"
    
    def activate_selected(self, request, queryset):
        """Activate selected subscriptions"""
        updated = queryset.update(is_active=True)
        self.message_user(request, f'{updated} subscription(s) activated.')
    activate_selected.short_description = "Activate selected subscriptions"


@admin.register(NewsletterIntegration)
class NewsletterIntegrationAdmin(admin.ModelAdmin):
    list_display = ['integration_type', 'is_active', 'created_at', 'updated_at']
    list_filter = ['integration_type', 'is_active']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Integration Settings', {
            'fields': ('integration_type', 'is_active')
        }),
        ('Mailchimp Configuration', {
            'fields': ('mailchimp_api_key', 'mailchimp_list_id', 'mailchimp_server_prefix'),
            'description': '''<strong>How to find your Mailchimp credentials:</strong><br>
            <strong>API Key:</strong> Go to Account > Extras > API keys in Mailchimp. Create a new key if needed.<br>
            <strong>List ID:</strong> Go to Audience > All contacts > Settings > Audience name and defaults. The List ID is shown at the bottom.<br>
            <strong>Server Prefix:</strong> This is your Mailchimp data center identifier. It's usually found at the END of your API key (e.g., if your API key ends with "-us1", then "us1" is your prefix). Common prefixes are: us1, us2, us3, us4, us5, us6, us7, us8, us9, us10, us11, us12, us13, us14, us15, us16, us17, us18, us19, us20, us21, us22, us23, us24, us25, us26, us27, us28, us29, us30, eu1, eu2, eu3, eu4, eu5, eu6, eu7, eu8, eu9, eu10, eu11, eu12, eu13, eu14, eu15, eu16, eu17, eu18, eu19, eu20, eu21, eu22, eu23, eu24, eu25, eu26, eu27, eu28, eu29, eu30, ap1, ap2, ap3, ap4, ap5, ap6, ap7, ap8, ap9, ap10, ap11, ap12, ap13, ap14, ap15, ap16, ap17, ap18, ap19, ap20, ap21, ap22, ap23, ap24, ap25, ap26, ap27, ap28, ap29, ap30, etc.<br>
            <strong>Alternative:</strong> If you're logged into Mailchimp, check the URL in your browser - it will show something like "us1.admin.mailchimp.com" or "us2.admin.mailchimp.com". The "us1" or "us2" part is your server prefix.<br>
            <strong>Note:</strong> If you leave this blank, the system will try to extract it from your API key automatically.''',
            'classes': ('collapse',)
        }),
        ('SendGrid Configuration', {
            'fields': ('sendgrid_api_key', 'sendgrid_list_id'),
            'description': 'Enter your SendGrid API credentials.',
            'classes': ('collapse',)
        }),
        ('Constant Contact Configuration', {
            'fields': ('constant_contact_api_key', 'constant_contact_access_token', 'constant_contact_list_id'),
            'description': 'Enter your Constant Contact API credentials.',
            'classes': ('collapse',)
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def has_add_permission(self, request):
        # Only allow one integration per type
        return True
    
    def has_delete_permission(self, request, obj=None):
        return True
    
    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        # Make integration_type read-only if editing existing object
        if obj:
            form.base_fields['integration_type'].disabled = True
        return form
    
    def save_model(self, request, obj, form, change):
        # Validate that only one integration of each type exists
        if not change:  # Creating new
            existing = NewsletterIntegration.objects.filter(integration_type=obj.integration_type)
            if existing.exists():
                from django.contrib import messages
                messages.error(request, f'An integration of type "{obj.get_integration_type_display()}" already exists.')
                return
        
        # If activating this integration, deactivate others of the same type
        if obj.is_active:
            NewsletterIntegration.objects.filter(
                integration_type=obj.integration_type
            ).exclude(id=obj.id if obj.id else None).update(is_active=False)
        
        super().save_model(request, obj, form, change)
