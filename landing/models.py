from django.db import models
from django.utils.translation import gettext_lazy as _

from modelcluster.fields import ParentalKey
from modelcluster.contrib.taggit import ClusterTaggableManager
from taggit.models import TaggedItemBase

from wagtail.models import Page, Orderable
from wagtail.fields import RichTextField, StreamField
from wagtail.admin.panels import (
    FieldPanel, InlinePanel, MultiFieldPanel, FieldRowPanel
)
from wagtail.images.blocks import ImageChooserBlock
from wagtail.images.models import Image
from wagtail.snippets.models import register_snippet
from wagtail.search import index
from wagtail import blocks
from wagtail.contrib.settings.models import BaseSiteSetting, register_setting

from wagtail.models import Page
from wagtail.admin.panels import FieldPanel
from wagtail.fields import StreamField, RichTextField

# Hero Section Block
class HeroBlock(blocks.StructBlock):
    """Hero section with title, subtitle, and background image."""
    title = blocks.CharBlock(required=True, help_text=_("Title for the hero section"))
    subtitle = blocks.TextBlock(required=False, help_text=_("Subtitle for the hero section"))
    cta_text = blocks.CharBlock(required=False, help_text=_("Call to action button text"))
    cta_link = blocks.URLBlock(required=False, help_text=_("Call to action button link"))
    background_image = ImageChooserBlock(required=False, help_text=_("Background image for the hero section"))
    
    class Meta:
        template = 'landing/blocks/hero_block.html'
        icon = 'image'
        label = _("Hero Section")


# Feature Block
class FeatureBlock(blocks.StructBlock):
    """Feature with icon, title, and description."""
    icon = blocks.CharBlock(required=False, help_text=_("Font Awesome icon class"))
    title = blocks.CharBlock(required=True, help_text=_("Feature title"))
    description = blocks.TextBlock(required=True, help_text=_("Feature description"))
    
    class Meta:
        template = 'landing/blocks/feature_block.html'
        icon = 'placeholder'
        label = _("Feature")


# Features Section Block
class FeaturesBlock(blocks.StructBlock):
    """Section with multiple features."""
    title = blocks.CharBlock(required=False, help_text=_("Section title"))
    features = blocks.ListBlock(FeatureBlock())
    
    class Meta:
        template = 'landing/blocks/features_block.html'
        icon = 'list-ul'
        label = _("Features Section")


# Testimonial Block
class TestimonialBlock(blocks.StructBlock):
    """Testimonial with quote, author, and optional image."""
    quote = blocks.TextBlock(required=True, help_text=_("Testimonial quote"))
    author = blocks.CharBlock(required=True, help_text=_("Author name"))
    role = blocks.CharBlock(required=False, help_text=_("Author role or company"))
    image = ImageChooserBlock(required=False, help_text=_("Author image"))
    
    class Meta:
        template = 'landing/blocks/testimonial_block.html'
        icon = 'openquote'
        label = _("Testimonial")


# Testimonials Section Block
class TestimonialsBlock(blocks.StructBlock):
    """Section with multiple testimonials."""
    title = blocks.CharBlock(required=False, help_text=_("Section title"))
    testimonials = blocks.ListBlock(TestimonialBlock())
    
    class Meta:
        template = 'landing/blocks/testimonials_block.html'
        icon = 'openquote'
        label = _("Testimonials Section")


# Call to Action Block
class CTABlock(blocks.StructBlock):
    """Call to action section with title, text, and button."""
    title = blocks.CharBlock(required=True, help_text=_("CTA title"))
    text = blocks.TextBlock(required=False, help_text=_("CTA text"))
    button_text = blocks.CharBlock(required=True, help_text=_("Button text"))
    button_link = blocks.URLBlock(required=True, help_text=_("Button link"))
    background_color = blocks.CharBlock(required=False, help_text=_("Background color (hex code)"))
    
    class Meta:
        template = 'landing/blocks/cta_block.html'
        icon = 'success'
        label = _("Call to Action")


# Content Section Block
class ContentBlock(blocks.StructBlock):
    """Rich text content section with optional image."""
    title = blocks.CharBlock(required=False, help_text=_("Section title"))
    content = blocks.RichTextBlock(required=True, help_text=_("Section content"))
    image = ImageChooserBlock(required=False, help_text=_("Section image"))
    image_position = blocks.ChoiceBlock(
        choices=[
            ('left', _("Left")),
            ('right', _("Right")),
        ],
        default='right',
        help_text=_("Position of the image")
    )
    
    class Meta:
        template = 'landing/blocks/content_block.html'
        icon = 'doc-full'
        label = _("Content Section")


# Landing Page Tag
class LandingPageTag(TaggedItemBase):
    """Tags for landing pages."""
    content_object = ParentalKey(
        'LandingPage',
        related_name='tagged_items',
        on_delete=models.CASCADE
    )


# Landing Page Model
class LandingPage(Page):
    """Modular landing page model."""
    
    # Database fields
    description = models.CharField(max_length=255, blank=True, help_text=_("Page description for SEO"))
    body = StreamField([
        ('hero', HeroBlock()),
        ('features', FeaturesBlock()),
        ('testimonials', TestimonialsBlock()),
        ('content', ContentBlock()),
        ('cta', CTABlock()),
    ], use_json_field=True, null=True, blank=True)
    # Define what page types can be created as children
    #subpage_types = ['blog.BlogPage', 'about.AboutPage']
    # Define what page types can be parent pages
    parent_page_types = ['wagtailcore.Page', 'home.HomePage']
    # SEO fields
    og_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        help_text=_("Open Graph image (1200x630px recommended)")
    )
    tags = ClusterTaggableManager(through=LandingPageTag, blank=True)
    
    # Search index configuration
    search_fields = Page.search_fields + [
        index.SearchField('description'),
        index.SearchField('body'),
        index.RelatedFields('tags', [
            index.SearchField('name'),
        ]),
    ]
    
    # Editor panels configuration
    content_panels = Page.content_panels + [
        FieldPanel('description'),
        FieldPanel('body'),
        FieldPanel('tags'),
    ]
    
    promote_panels = Page.promote_panels + [
        FieldPanel('og_image'),
    ]
    
    # Meta class
    class Meta:
        verbose_name = _("Landing Page")
        verbose_name_plural = _("Landing Pages")


# SEO Settings
@register_setting
class SEOSettings(BaseSiteSetting):
    """Site-wide SEO settings."""
    google_analytics_id = models.CharField(
        max_length=50,
        blank=True,
        help_text=_("Google Analytics tracking ID (e.g., UA-XXXXXXXX-X)")
    )
    google_site_verification = models.CharField(
        max_length=255,
        blank=True,
        help_text=_("Google Search Console verification code")
    )
    bing_site_verification = models.CharField(
        max_length=255,
        blank=True,
        help_text=_("Bing Webmaster Tools verification code")
    )
    default_og_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        help_text=_("Default Open Graph image (1200x630px recommended)")
    )
    site_description = models.TextField(
        blank=True,
        help_text=_("Default site description for SEO")
    )
    twitter_site = models.CharField(
        max_length=50,
        blank=True,
        help_text=_("Twitter site username (e.g., @site)")
    )
    facebook_app_id = models.CharField(
        max_length=50,
        blank=True,
        help_text=_("Facebook App ID")
    )
    
    panels = [
        MultiFieldPanel([
            FieldPanel('google_analytics_id'),
            FieldPanel('google_site_verification'),
            FieldPanel('bing_site_verification'),
        ], heading=_("Analytics & Verification")),
        MultiFieldPanel([
            FieldPanel('default_og_image'),
            FieldPanel('site_description'),
            FieldPanel('twitter_site'),
            FieldPanel('facebook_app_id'),
        ], heading=_("Social Media")),
    ]
