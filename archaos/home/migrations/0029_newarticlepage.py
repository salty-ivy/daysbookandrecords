# Generated by Django 5.0.4 on 2024-09-03 17:47

import django.db.models.deletion
import wagtail.blocks
import wagtail.embeds.blocks
import wagtail.fields
import wagtail.images.blocks
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0028_remove_homepage_body_remove_homepage_extra_embed_and_more'),
        ('wagtailcore', '0091_remove_revision_submitted_for_moderation'),
    ]

    operations = [
        migrations.CreateModel(
            name='NewArticlePage',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.page')),
                ('body', wagtail.fields.RichTextField(blank=True)),
                ('extra_embed', wagtail.fields.StreamField([('image_block', wagtail.blocks.StructBlock([('image', wagtail.images.blocks.ImageChooserBlock(required=True)), ('title', wagtail.blocks.CharBlock(required=False)), ('caption', wagtail.blocks.CharBlock(required=False)), ('attribution', wagtail.blocks.CharBlock(required=False))])), ('embed_block', wagtail.embeds.blocks.EmbedBlock(help_text='Insert an embed URL e.g https://www.youtube.com/watch?v=SGJFWirQ3ks', icon='media', template='home/embed_block.html'))], blank=True, verbose_name='Page embed')),
            ],
            options={
                'abstract': False,
            },
            bases=('wagtailcore.page',),
        ),
    ]
