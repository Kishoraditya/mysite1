
from django.db import models

from wagtail.models import Page
from wagtail.fields import RichTextField
from wagtail.admin.panels import FieldPanel


class HomePage(Page):
    """Home page model."""
    
    # Database fields
    body = RichTextField(blank=True)
    banner_title = models.CharField(max_length=100, blank=True)
    banner_subtitle = models.CharField(max_length=250, blank=True)
    
    # Editor panels configuration
    content_panels = Page.content_panels + [
        FieldPanel('banner_title'),
        FieldPanel('banner_subtitle'),
        FieldPanel('body'),
    ]
    
    class Meta:
        verbose_name = "Home Page"
        verbose_name_plural = "Home Pages"