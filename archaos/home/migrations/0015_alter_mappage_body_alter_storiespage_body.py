# Generated by Django 5.0.4 on 2024-07-10 19:26

import wagtail.blocks
import wagtail.embeds.blocks
import wagtail.fields
import wagtail.images.blocks
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0014_alter_gallerypage_carousel'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mappage',
            name='body',
            field=wagtail.fields.StreamField([('heading_block', wagtail.blocks.StructBlock([('heading_text', wagtail.blocks.CharBlock(form_classname='title', required=True)), ('size', wagtail.blocks.ChoiceBlock(blank=True, choices=[('', 'Select a header size'), ('h2', 'H2'), ('h3', 'H3'), ('h4', 'H4')], required=False))])), ('sub_description', wagtail.blocks.CharBlock()), ('map_block', wagtail.blocks.StructBlock([('url', wagtail.blocks.URLBlock(required=False)), ('link_text_block', wagtail.blocks.CharBlock(required=False)), ('text_block', wagtail.blocks.RichTextBlock(required=False)), ('multi_embed_block', wagtail.blocks.StreamBlock([('image_block', wagtail.blocks.StructBlock([('image', wagtail.images.blocks.ImageChooserBlock(required=True)), ('title', wagtail.blocks.CharBlock(required=False)), ('caption', wagtail.blocks.CharBlock(required=False)), ('attribution', wagtail.blocks.CharBlock(required=False))])), ('embed_block', wagtail.embeds.blocks.EmbedBlock(help_text='Insert an embed URL e.g https://www.youtube.com/watch?v=SGJFWirQ3ks', icon='media', template='home/embed_block.html'))], required=False))]))], blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='storiespage',
            name='body',
            field=wagtail.fields.StreamField([('stories', wagtail.blocks.StructBlock([('story_heading', wagtail.blocks.StructBlock([('heading_text', wagtail.blocks.CharBlock(form_classname='title', required=True)), ('size', wagtail.blocks.ChoiceBlock(blank=True, choices=[('', 'Select a header size'), ('h2', 'H2'), ('h3', 'H3'), ('h4', 'H4')], required=False))])), ('story_description', wagtail.blocks.CharBlock(required=False)), ('story_item', wagtail.blocks.StreamBlock([('story_item', wagtail.blocks.StructBlock([('story_item_title', wagtail.blocks.CharBlock()), ('story_item_description', wagtail.blocks.RichTextBlock(required=False)), ('multi_embed_block', wagtail.blocks.StreamBlock([('image_block', wagtail.blocks.StructBlock([('image', wagtail.images.blocks.ImageChooserBlock(required=True)), ('title', wagtail.blocks.CharBlock(required=False)), ('caption', wagtail.blocks.CharBlock(required=False)), ('attribution', wagtail.blocks.CharBlock(required=False))])), ('embed_block', wagtail.embeds.blocks.EmbedBlock(help_text='Insert an embed URL e.g https://www.youtube.com/watch?v=SGJFWirQ3ks', icon='media', template='home/embed_block.html'))], required=False))]))], required=False))]))]),
        ),
    ]
