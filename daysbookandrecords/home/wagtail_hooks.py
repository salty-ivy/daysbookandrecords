# wagtail_hooks.py

from wagtail_modeladmin.options import (
    ModelAdmin,
    ModelAdminGroup,
    modeladmin_register
)
from django.http import HttpResponse
from django.utils import timezone
from django.shortcuts import redirect
from django.utils.html import format_html
import csv

from .models import Book, Record, NewsArticle, NewsletterSubscription, NewsletterIntegration


class BookAdmin(ModelAdmin):
    model = Book
    menu_label = "Books"
    menu_icon = "pick"
    menu_order = 200
    add_to_settings_menu = False
    exclude_from_explorer = False
    list_display = ['title', 'author', 'genre', 'price', 'status', 'created_at', 'featured']
    list_filter = ['genre', 'condition', 'status', 'created_at']
    search_fields = ['title', 'author', 'isbn']
    readonly_fields = ['created_at', 'updated_at']

class RecordAdmin(ModelAdmin):
    model = Record
    menu_label = "Records"
    menu_icon = "pick"
    menu_order = 200
    add_to_settings_menu = False
    exclude_from_explorer = False
    list_display = ['title', 'artist', 'genre', 'condition', 'format', 'price', 'status', 'created_at', 'featured']
    list_filter = ['genre', 'condition', 'format', 'status', 'created_at']
    search_fields = ['title', 'artist', 'cat_number']
    readonly_fields = ['created_at', 'updated_at']


modeladmin_register(BookAdmin)
modeladmin_register(RecordAdmin)

class NewsArticleAdmin(ModelAdmin):
    model = NewsArticle
    menu_label = "News Articles"
    menu_icon = "doc-full"
    menu_order = 301
    add_to_settings_menu = False
    exclude_from_explorer = False
    list_display = ['title', 'author', 'publish_date', 'status', 'featured', 'created_at']
    list_filter = ['status', 'featured', 'publish_date', 'created_at']
    search_fields = ['title', 'author', 'content', 'excerpt']
    exclude = ['slug']

modeladmin_register(NewsArticleAdmin)


class NewsletterSubscriptionAdmin(ModelAdmin):
    model = NewsletterSubscription
    menu_label = "Newsletter Emails"
    menu_icon = "mail"
    menu_order = 400
    add_to_settings_menu = False
    exclude_from_explorer = False
    list_display = ['email', 'subscribed_at', 'is_active', 'source']
    list_filter = ['is_active', 'source', 'subscribed_at']
    search_fields = ['email']
    readonly_fields = ['subscribed_at']
    index_template_name = 'modeladmin/home/newslettersubscription/index.html'
    
    def get_button_helper_class(self):
        """Override to customize button text"""
        from wagtail_modeladmin.helpers import ButtonHelper
        
        class CustomButtonHelper(ButtonHelper):
            def add_button(self, classnames_add=None, classnames_exclude=None):
                """Override add button to change text to 'Add New'"""
                # Call parent method to get the button structure
                button = super().add_button(classnames_add, classnames_exclude)
                # Only modify the label
                if button:
                    button['label'] = 'Add New'
                return button
        
        return CustomButtonHelper
    
    def get_queryset(self, request):
        return super().get_queryset(request).order_by('-subscribed_at')
    
    def index_view(self, request, *args, **kwargs):
        """Override index view to handle export requests and add export buttons"""
        # Check if this is an export request
        if 'export_all' in request.GET:
            return self.export_all(request)
        elif 'export_selected' in request.GET:
            return self.export_selected(request)
        
        # Call parent index view
        response = super().index_view(request, *args, **kwargs)
        
        # Add export URLs to context if it's a TemplateResponse
        if hasattr(response, 'context_data'):
            # Get the base URL for this modeladmin
            base_url = self.url_helper.get_action_url('index')
            response.context_data['export_all_url'] = f"{base_url}?export_all=1"
            response.context_data['export_selected_url'] = f"{base_url}?export_selected=1"
        
        return response
    
    def export_all(self, request):
        """Export all active subscriptions to CSV"""
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename="newsletter_subscriptions_all_{timezone.now().strftime("%Y%m%d_%H%M%S")}.csv"'
        
        writer = csv.writer(response)
        writer.writerow(['Email', 'Subscribed At', 'Status', 'Source'])
        
        subscriptions = NewsletterSubscription.objects.filter(is_active=True).order_by('-subscribed_at')
        for subscription in subscriptions:
            writer.writerow([
                subscription.email,
                subscription.subscribed_at.strftime('%Y-%m-%d %H:%M:%S'),
                'Active' if subscription.is_active else 'Inactive',
                subscription.source
            ])
        
        return response
    
    def export_selected(self, request):
        """Export selected subscriptions to CSV"""
        # Get selected IDs from GET parameters
        selected_ids = request.GET.getlist('selected')
        
        if not selected_ids:
            from django.contrib import messages
            messages.warning(request, 'No subscriptions selected for export.')
            return redirect(self.url_helper.get_action_url('index'))
        
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename="newsletter_subscriptions_selected_{timezone.now().strftime("%Y%m%d_%H%M%S")}.csv"'
        
        writer = csv.writer(response)
        writer.writerow(['Email', 'Subscribed At', 'Status', 'Source'])
        
        subscriptions = NewsletterSubscription.objects.filter(id__in=selected_ids).order_by('-subscribed_at')
        for subscription in subscriptions:
            writer.writerow([
                subscription.email,
                subscription.subscribed_at.strftime('%Y-%m-%d %H:%M:%S'),
                'Active' if subscription.is_active else 'Inactive',
                subscription.source
            ])
        
        return response

modeladmin_register(NewsletterSubscriptionAdmin)


class NewsletterIntegrationAdmin(ModelAdmin):
    model = NewsletterIntegration
    menu_label = "Newsletter Settings"
    menu_icon = "cog"
    menu_order = 401
    add_to_settings_menu = False
    exclude_from_explorer = False
    list_display = ['integration_type', 'is_active_display', 'created_at', 'updated_at']
    list_filter = ['integration_type', 'is_active']
    readonly_fields = ['created_at', 'updated_at', 'active_status_display']
    
    def is_active_display(self, obj):
        """Display active status with visual indicator"""
        if obj.is_active:
            return format_html('<span style="color: green; font-weight: bold;">✓ ACTIVE</span>')
        return format_html('<span style="color: #999;">Inactive</span>')
    is_active_display.short_description = 'Status'
    
    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        
        # Remove integration_type and is_active from the form - they'll be determined automatically
        if 'integration_type' in form.base_fields:
            del form.base_fields['integration_type']
        if 'is_active' in form.base_fields:
            del form.base_fields['is_active']
        
        return form
    
    def get_fieldsets(self, request, obj=None):
        """Show integration fieldsets - type and active status determined automatically"""
        from django.utils.html import format_html
        
        fieldsets = (
            ('Mailchimp Configuration', {
                'fields': ('mailchimp_api_key', 'mailchimp_list_id', 'mailchimp_server_prefix'),
                'description': format_html(
                    '<strong>How to find your Mailchimp credentials:</strong><br>'
                    '<strong>API Key:</strong> Go to Account > Extras > API keys in Mailchimp. Create a new key if needed.<br>'
                    '<strong>List ID:</strong> Go to Audience > All contacts > Settings > Audience name and defaults. The List ID is shown at the bottom.<br>'
                    '<strong>Server Prefix:</strong> This is your Mailchimp data center identifier. It\'s usually found at the END of your API key (e.g., if your API key ends with "-us1", then "us1" is your prefix). Common prefixes are: us1, us2, us3, etc.<br>'
                    '<strong>Alternative:</strong> If you\'re logged into Mailchimp, check the URL in your browser - it will show something like "us1.admin.mailchimp.com". The "us1" part is your server prefix.<br>'
                    '<strong>Note:</strong> If you leave this blank, the system will try to extract it from your API key automatically.<br><br>'
                    '<strong style="color: green;">Tip:</strong> Fill in all Mailchimp fields to automatically configure Mailchimp integration.'
                ),
            }),
            ('SendGrid Configuration', {
                'fields': ('sendgrid_api_key', 'sendgrid_list_id'),
                'description': format_html(
                    'Enter your SendGrid API credentials.<br><br>'
                    '<strong style="color: green;">Tip:</strong> Fill in all SendGrid fields to automatically configure SendGrid integration.'
                ),
            }),
            ('Constant Contact Configuration', {
                'fields': ('constant_contact_api_key', 'constant_contact_access_token', 'constant_contact_list_id'),
                'description': format_html(
                    'Enter your Constant Contact API credentials.<br><br>'
                    '<strong style="color: green;">Tip:</strong> Fill in all Constant Contact fields to automatically configure Constant Contact integration.'
                ),
            }),
        )
        
        if obj:
            fieldsets += (
                ('Metadata', {
                    'fields': ('created_at', 'updated_at', 'active_status_display'),
                    'classes': ('collapse',)
                }),
            )
        
        return fieldsets
    
    def save_model(self, request, obj, form, change):
        """Automatically determine integration type and active status based on filled fields"""
        # Check which integration has all required fields filled
        mailchimp_complete = (
            obj.mailchimp_api_key and 
            obj.mailchimp_list_id and 
            obj.mailchimp_server_prefix
        )
        
        sendgrid_complete = (
            obj.sendgrid_api_key and 
            obj.sendgrid_list_id
        )
        
        constant_contact_complete = (
            obj.constant_contact_api_key and 
            obj.constant_contact_access_token and 
            obj.constant_contact_list_id
        )
        
        # Determine integration type based on which fields are filled
        # Priority: Mailchimp > SendGrid > Constant Contact
        if mailchimp_complete:
            obj.integration_type = 'mailchimp'
            obj.is_active = True
        elif sendgrid_complete:
            obj.integration_type = 'sendgrid'
            obj.is_active = True
        elif constant_contact_complete:
            obj.integration_type = 'constant_contact'
            obj.is_active = True
        else:
            # No complete integration, set to none
            obj.integration_type = 'none'
            obj.is_active = False
        
        # If we're activating a new integration, deactivate others
        if obj.is_active and change:
            # Deactivate other integrations of the same type (shouldn't happen, but just in case)
            NewsletterIntegration.objects.filter(
                integration_type=obj.integration_type
            ).exclude(pk=obj.pk).update(is_active=False)
        
        super().save_model(request, obj, form, change)
    
    def active_status_display(self, obj):
        """Display current active status"""
        if obj is None:
            return "N/A (New integration - fill in all fields for an integration to activate it)"
        
        if obj.is_active:
            return format_html(
                '<div style="background-color: #d4edda; border: 1px solid #c3e6cb; padding: 10px; border-radius: 4px; margin: 10px 0;">'
                '<strong style="color: #155724;">✓ This integration is ACTIVE</strong><br>'
                'Integration Type: <strong>{}</strong><br>'
                'New newsletter subscriptions will be automatically synced to this service.'
                '</div>',
                obj.get_integration_type_display()
            )
        else:
            return format_html(
                '<div style="background-color: #f8d7da; border: 1px solid #f5c6cb; padding: 10px; border-radius: 4px; margin: 10px 0;">'
                '<strong style="color: #721c24;">This integration is INACTIVE</strong><br>'
                'Fill in all required fields for an integration (Mailchimp, SendGrid, or Constant Contact) to activate it automatically.'
                '</div>'
            )
    active_status_display.short_description = 'Current Status'

modeladmin_register(NewsletterIntegrationAdmin)