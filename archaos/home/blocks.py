from wagtail.blocks import (
    CharBlock,
    StreamBlock,
    StructBlock,
    RichTextBlock,
    ChoiceBlock,
    URLBlock
)
from wagtail.embeds.blocks import EmbedBlock
from wagtail.images.blocks import ImageChooserBlock
from wagtail.documents.blocks import DocumentChooserBlock


class ImageBlock(StructBlock):
    """
    Custom `StructBlock` for utilizing images with associated caption and
    attribution data
    """

    image = ImageChooserBlock(required=True)
    title = CharBlock(required=False)
    caption = CharBlock(required=False)
    attribution = CharBlock(required=False)

    class Meta:
        icon = "image"
        template = "home/image_block.html"


class HeadingBlock(StructBlock):
    """
    Custom `StructBlock` that allows the user to select h2 - h4 sizes for headers
    """

    heading_text = CharBlock(classname="title", required=False)

    class Meta:
        icon = "title"
        template = "home/heading_block.html"


class BaseStreamBlock(StreamBlock):
    """
    Define the custom blocks that `StreamField` will utilize
    """
    image_block = ImageBlock()
    embed_block = EmbedBlock(
        help_text="Insert an embed URL e.g https://www.youtube.com/watch?v=SGJFWirQ3ks",
        icon="media",
        template="home/embed_block.html",
    )


class HomeStreamBlock(StreamBlock):
    """
    Define the custom blocks that `StreamField` will utilize
    """
    paragraph_block = RichTextBlock()
    image_block = ImageBlock()
    embed_block = EmbedBlock(
        help_text="Insert an embed URL e.g https://www.youtube.com/watch?v=SGJFWirQ3ks",
        icon="media",
        template="home/embed_block.html",
    )


class StoriesMediaStreamBlock(BaseStreamBlock):
    """
    Stream block that allows image or embeds min = 0 max = 1
    """
    pass


class MapBlock(StructBlock):
    """
    Custom `StructBlock` for utilizing Google Maps embeds along with
    other relevant details
    """
    url = URLBlock(required=False)
    link_text_block = CharBlock(required=False)
    text_block = RichTextBlock(required=False)
    multi_embed_block = BaseStreamBlock(required=False)


class BodyStreamBlock(StreamBlock):
    """
    Define the custom blocks that `StreamField` will utilize
    """
    heading_block = HeadingBlock()
    sub_description = CharBlock()
    map_block = MapBlock()


class ImageOrEmbedStructureBlock(StructBlock):
    """
    Custom `StructBlock` that allows the user to select an image or embed URL
    """
    image_block = ImageBlock()
    embed_block = EmbedBlock(
        help_text="Insert an embed URL e.g https://www.youtube.com/watch?v=SGJFWirQ3ks",
        icon="media",
        template="home/embed_block.html",
    )


class StoryItem(StructBlock):
    story_item_title = CharBlock()
    story_item_description = RichTextBlock(required=False)
    multi_embed_block = StoriesMediaStreamBlock(required=False)


class StoryItemStreamBlock(StreamBlock):
    story_item = StoryItem()


class StoryStructBlock(StructBlock):
    story_heading = HeadingBlock(required=False)
    story_description = CharBlock(required=False)
    story_item = StoryItemStreamBlock(required=False)


class EmbedWithCaptionBlock(StructBlock):
    """
    Custom `StructBlock` that allows the user to select an image or embed URL
    """
    embed_block = EmbedBlock(
        help_text="Insert an embed URL, this could be direct URL or share video URL",
    )

    caption = CharBlock(required=False)

    class Meta:
        icon = "media"
        template = "home/embed_caption_block.html"


class MultiMediaStreamBlock(StreamBlock):
    """
    Define the custom blocks that `StreamField` will utilize
    """
    image_block = ImageBlock()
    embed_block = EmbedWithCaptionBlock()
    document_block = DocumentChooserBlock()
