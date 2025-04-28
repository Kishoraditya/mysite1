import pytest
from django.test import Client
from django.urls import reverse
from wagtail.models import Page, Site

from landing.models import LandingPage, SEOSettings


@pytest.mark.django_db
def test_seo_settings():
    """Test that SEO settings can be created and retrieved."""
    # Get the default site
    site = Site.objects.first()
    
    # Create SEO settings
    seo_settings = SEOSettings.objects.create(
        site=site,
        google_analytics_id='UA-12345678-1',
        google_site_verification='google123',
        bing_site_verification='bing123',
        site_description='Site-wide description for SEO',
        twitter_site='@testsite',
        facebook_app_id='123456789'
    )
    
    # Retrieve the settings
    retrieved_settings = SEOSettings.objects.get(site=site)
    
    # Check that the settings were saved correctly
    assert retrieved_settings.google_analytics_id == 'UA-12345678-1'
    assert retrieved_settings.google_site_verification == 'google123'
    assert retrieved_settings.site_description == 'Site-wide description for SEO'
    assert retrieved_settings.twitter_site == '@testsite'


@pytest.mark.django_db
def test_landing_page_seo_tags():
    # Get the root page (always has ID 1)
    root_page = Page.objects.get(id=1)
    
    # Create a landing page with SEO fields
    landing_page = LandingPage(
        title="Regular Title",
        description="Regular description",
        seo_title="Custom SEO Title for Testing",
        search_description="Custom SEO description for testing",
    )
    
    # Add the page as a child of the root page
    root_page.add_child(instance=landing_page)
    
    # Publish the page
    revision = landing_page.save_revision()
    revision.publish()
    
    # Refresh the page from the database
    landing_page.refresh_from_db()
    
    # Get the site
    from wagtail.models import Site
    site = Site.objects.first()
    
    # If there's no site, create one
    if not site:
        site = Site.objects.create(
            hostname='localhost',
            root_page=root_page,
            is_default_site=True
        )
    
    # Get the rendered HTML directly from the page
    from django.test import RequestFactory
    
    request = RequestFactory().get('/')
    request.site = site
    
    # Get the rendered HTML
    from django.template.response import SimpleTemplateResponse
    
    # Use the page's specific method to get the correct template
    response = landing_page.serve(request)
    
    # If the response is a SimpleTemplateResponse, we need to render it
    if isinstance(response, SimpleTemplateResponse):
        response.render()
    
    # Get the content
    content = response.content.decode('utf-8')
    
    # Check for SEO tags in the HTML
    assert "Custom SEO Title for Testing" in content
    assert "Custom SEO description for testing" in content
