# Generated by Django 5.0.4 on 2024-06-18 18:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0007_rename_standardpage_homstandardpage'),
        ('wagtailcore', '0091_remove_revision_submitted_for_moderation'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='HomStandardPage',
            new_name='StandardPage',
        ),
    ]
