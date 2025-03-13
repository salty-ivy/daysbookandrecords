from django import template
from wagtail.models import Page

register = template.Library()
# https://docs.djangoproject.com/en/3.2/howto/custom-template-tags/


@register.simple_tag()
def get_navbar_pages():
    return Page.objects.live().public().in_menu().filter(depth__gte=2)
