# Generated by Django 5.0.4 on 2024-08-15 17:48

import wagtail.blocks
import wagtail.embeds.blocks
import wagtail.fields
import wagtail.images.blocks
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0027_alter_gallerypage_carousel'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='homepage',
            name='body',
        ),
        migrations.RemoveField(
            model_name='homepage',
            name='extra_embed',
        ),
        migrations.AddField(
            model_name='homepage',
            name='page_body',
            field=wagtail.fields.StreamField([('paragraph_block', wagtail.blocks.RichTextBlock()), ('image_block', wagtail.blocks.StructBlock([('image', wagtail.images.blocks.ImageChooserBlock(required=True)), ('title', wagtail.blocks.CharBlock(required=False)), ('caption', wagtail.blocks.CharBlock(required=False)), ('attribution', wagtail.blocks.CharBlock(required=False))])), ('embed_block', wagtail.embeds.blocks.EmbedBlock(help_text='Insert an embed URL e.g https://www.youtube.com/watch?v=SGJFWirQ3ks', icon='media', template='home/embed_block.html'))], blank=True, verbose_name='body'),
        ),
    ]
