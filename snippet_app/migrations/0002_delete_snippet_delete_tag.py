# Generated by Django 5.0.4 on 2024-04-27 06:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("snippet_app", "0001_initial"),
    ]

    operations = [
        migrations.DeleteModel(name="Snippet",),
        migrations.DeleteModel(name="Tag",),
    ]
