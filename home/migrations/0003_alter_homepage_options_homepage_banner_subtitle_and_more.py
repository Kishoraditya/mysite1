# Generated by Django 4.2.16 on 2025-04-26 11:09

from django.db import migrations, models
import wagtail.fields


class Migration(migrations.Migration):

    dependencies = [
        ("home", "0002_create_homepage"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="homepage",
            options={"verbose_name": "Home Page", "verbose_name_plural": "Home Pages"},
        ),
        migrations.AddField(
            model_name="homepage",
            name="banner_subtitle",
            field=models.CharField(blank=True, max_length=250),
        ),
        migrations.AddField(
            model_name="homepage",
            name="banner_title",
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AddField(
            model_name="homepage",
            name="body",
            field=wagtail.fields.RichTextField(blank=True),
        ),
    ]
