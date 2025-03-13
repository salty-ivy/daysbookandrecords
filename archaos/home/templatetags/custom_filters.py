from django import template
from django.utils.text import slugify
from wagtail.rich_text import RichText
import re


register = template.Library()

@register.filter(name='add_class')
def add_class(field, css_class):
    return field.as_widget(attrs={"class": css_class})

@register.filter(name='slugify_heading')
def slugify_heading(value):
    return slugify(value)

@register.filter(name='truncate_words')
def truncate_words(value, num_words):
    if isinstance(value, RichText):
        value = str(value)
    words = re.split(r'\s+', value)
    if len(words) > num_words:
        return ' '.join(words[:num_words]) + '...'
    return value