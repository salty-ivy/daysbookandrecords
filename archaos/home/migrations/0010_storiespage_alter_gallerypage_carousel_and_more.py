# Generated by Django 5.0.4 on 2024-06-20 10:36

import django.db.models.deletion
import wagtail.blocks
import wagtail.embeds.blocks
import wagtail.fields
import wagtail.images.blocks
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0009_rename_storypage_articlepage'),
        ('wagtailcore', '0091_remove_revision_submitted_for_moderation'),
    ]

    operations = [
        migrations.CreateModel(
            name='StoriesPage',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.page')),
                ('description', models.TextField(blank=True, help_text='Text to describe the page')),
                ('body', wagtail.fields.StreamField([('stories', wagtail.blocks.StructBlock([('Story_heading', wagtail.blocks.StructBlock([('heading_text', wagtail.blocks.CharBlock(form_classname='title', required=True)), ('size', wagtail.blocks.ChoiceBlock(blank=True, choices=[('', 'Select a header size'), ('h1', 'H1'), ('h2', 'H2'), ('h3', 'H3'), ('h4', 'H4')], required=False))])), ('story_description', wagtail.blocks.CharBlock()), ('story_item', wagtail.blocks.StreamBlock([('story_item', wagtail.blocks.StructBlock([('story_item_title', wagtail.blocks.CharBlock()), ('story_item_description', wagtail.blocks.RichTextBlock()), ('multi_embed_block', wagtail.blocks.StructBlock([('image_block', wagtail.blocks.StructBlock([('image', wagtail.images.blocks.ImageChooserBlock(required=True)), ('title', wagtail.blocks.CharBlock(required=False)), ('caption', wagtail.blocks.CharBlock(required=False)), ('attribution', wagtail.blocks.CharBlock(required=False))])), ('embed_block', wagtail.embeds.blocks.EmbedBlock(help_text='Insert an embed URL e.g https://www.youtube.com/watch?v=SGJFWirQ3ks', icon='media', template='home/embed_block.html'))]))]))]))]))])),
            ],
            options={
                'abstract': False,
            },
            bases=('wagtailcore.page',),
        ),
        migrations.AlterField(
            model_name='gallerypage',
            name='carousel',
            field=wagtail.fields.StreamField([('image_block', wagtail.blocks.StructBlock([('image', wagtail.images.blocks.ImageChooserBlock(required=True)), ('title', wagtail.blocks.CharBlock(required=False)), ('caption', wagtail.blocks.CharBlock(required=False)), ('attribution', wagtail.blocks.CharBlock(required=False))])), ('embed_block', wagtail.embeds.blocks.EmbedBlock(help_text='Insert an embed URL e.g https://www.youtube.com/watch?v=SGJFWirQ3ks', icon='media', template='home/embed_block.html'))], blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='homepage',
            name='extra_embed',
            field=wagtail.fields.StreamField([('image_block', wagtail.blocks.StructBlock([('image', wagtail.images.blocks.ImageChooserBlock(required=True)), ('title', wagtail.blocks.CharBlock(required=False)), ('caption', wagtail.blocks.CharBlock(required=False)), ('attribution', wagtail.blocks.CharBlock(required=False))])), ('embed_block', wagtail.embeds.blocks.EmbedBlock(help_text='Insert an embed URL e.g https://www.youtube.com/watch?v=SGJFWirQ3ks', icon='media', template='home/embed_block.html'))], blank=True, verbose_name='Page embed'),
        ),
        migrations.AlterField(
            model_name='mappage',
            name='body',
            field=wagtail.fields.StreamField([('heading_block', wagtail.blocks.StructBlock([('heading_text', wagtail.blocks.CharBlock(form_classname='title', required=True)), ('size', wagtail.blocks.ChoiceBlock(blank=True, choices=[('', 'Select a header size'), ('h1', 'H1'), ('h2', 'H2'), ('h3', 'H3'), ('h4', 'H4')], required=False))])), ('sub_description', wagtail.blocks.CharBlock()), ('map_block', wagtail.blocks.StructBlock([('url', wagtail.blocks.URLBlock(required=False)), ('link_text_block', wagtail.blocks.CharBlock(required=False)), ('text_block', wagtail.blocks.RichTextBlock(required=False)), ('multi_embed_block', wagtail.blocks.StreamBlock([('image_block', wagtail.blocks.StructBlock([('image', wagtail.images.blocks.ImageChooserBlock(required=True)), ('title', wagtail.blocks.CharBlock(required=False)), ('caption', wagtail.blocks.CharBlock(required=False)), ('attribution', wagtail.blocks.CharBlock(required=False))])), ('embed_block', wagtail.embeds.blocks.EmbedBlock(help_text='Insert an embed URL e.g https://www.youtube.com/watch?v=SGJFWirQ3ks', icon='media', template='home/embed_block.html'))], required=False))]))], blank=True, null=True),
        ),
    ]
