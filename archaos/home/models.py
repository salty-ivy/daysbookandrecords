from django.db import models
from django.utils.text import slugify
from django.conf import settings

from wagtail.models import Page
from wagtail.fields import RichTextField
from wagtail.admin.panels import FieldPanel, InlinePanel, MultiFieldPanel, FieldRowPanel
from .blocks import BaseStreamBlock, BodyStreamBlock, MultiMediaStreamBlock, StoryStructBlock, HomeStreamBlock
from wagtail.fields import StreamField
from modelcluster.fields import ParentalKey
from wagtail.contrib.forms.models import AbstractEmailForm, AbstractFormField
from wagtail.blocks import RichTextBlock


class HomePage(Page):
    # body = RichTextField(blank=True)
    page_body = StreamField(
        HomeStreamBlock(), verbose_name="body", blank=True, use_json_field=True
    )

    content_panels = Page.content_panels + [
        # FieldPanel("body"),
        FieldPanel("page_body"),
        # FieldPanel("extra_embed"),
    ]


class StandardPage(Page):
    body = StreamField(
        [("paragraph", RichTextBlock())],
    )

    content_panels = Page.content_panels + [
        FieldPanel("body"),
    ]

    parent_page_types = ["HomePage"]


class GalleryIndexPage(Page):
    description = models.TextField(help_text="Text to describe the page", blank=True)

    content_panels = Page.content_panels + [
        FieldPanel("description"),
    ]

    subpage_types = ["GalleryPage"]

    def get_gallery_items(self):
        return (
            GalleryPage.objects.live()
            .descendant_of(self)
        )

    def get_context(self, request, *args, **kwargs):
        context = super(GalleryIndexPage, self).get_context(request)
        context["gallery_items"] = self.get_gallery_items()
        return context


class GalleryPage(Page):
    description = models.TextField(help_text="Text to describe the page", blank=True)
    index_image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        help_text="Landscape mode only; horizontal width between 1000px and " "3000px.",
    )
    carousel = StreamField(MultiMediaStreamBlock(), blank=True, null=True)

    content_panels = Page.content_panels + [
        FieldPanel("description"),
        FieldPanel("index_image"),
        FieldPanel("carousel"),
    ]

    parent_page_types = ["GalleryIndexPage"]


class MapPage(Page):
    description = models.TextField(help_text="Text to describe the page", blank=True)
    body = StreamField(
        BodyStreamBlock(),
        blank=True,
        null=True
    )

    content_panels = Page.content_panels + [
        FieldPanel("description"),
        FieldPanel("body"),
    ]


class StoriesPage(Page):
    description = models.TextField(help_text="Text to describe the page", blank=True)
    body = StreamField([
        ("story", StoryStructBlock()),
    ])

    content_panels = Page.content_panels + [
        FieldPanel("description"),
        FieldPanel("body"),
    ]

    def get_story_titles(self):
        titles = []
        for block in self.body:
            if block.block_type == 'story':
                heading_text = block.value['story_heading']['heading_text']
                slugified_heading = slugify(heading_text)
                titles.append({
                    'original': heading_text,
                    'slug': slugified_heading,
                })
        return titles

    def is_dropdown_enabled(self):
        titles = []
        for block in self.body:
            if block.block_type == "story":
                heading = block.value.get('story_heading').get('heading_text')
                if heading:
                    titles.append(heading)

        return len(titles) > 0


# class ArticlePage(HomePage):
#     pass


class NewArticlePage(Page):
    body = RichTextField(blank=True)
    extra_embed = StreamField(
        BaseStreamBlock(), verbose_name="Page embed", blank=True, use_json_field=True
    )

    content_panels = Page.content_panels + [
        FieldPanel("body"),
        FieldPanel("extra_embed"),
    ]


class FormField(AbstractFormField):
    page = ParentalKey('FormPage', on_delete=models.CASCADE, related_name='form_fields')


class FormPage(AbstractEmailForm):
    description = RichTextField(blank=True)
    heading = models.CharField(max_length=255, blank=True, null=True)

    thank_you_text = RichTextField(blank=True)

    content_panels = AbstractEmailForm.content_panels + [
        FieldPanel('description'),
        FieldPanel('heading'),
        InlinePanel('form_fields', heading="Form fields", label="Field"),
        FieldPanel('thank_you_text'),
        MultiFieldPanel(
            [
                FieldRowPanel(
                    [
                        FieldPanel("from_address"),
                        FieldPanel("to_address"),
                    ]
                ),
                FieldPanel("subject"),
            ],
            "Email",
        ),
    ]

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request)
        context["captcha_key"] = settings.CAPTCHA_KEY
        return context
