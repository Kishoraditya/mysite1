import pytest
from django.test import Client
from wagtail.models import Page, Site

from landing.models import LandingPage


@pytest.mark.django_db
def test_accessibility_features():
    """Test that the landing page includes accessibility features."""
    # Create a landing page
    root_page = Page.objects.get(id=1)
    landing_page = LandingPage(
        title="Accessibility Test Page",
        description="Testing accessibility features",
        body=[
            ('hero', {
                'title': 'Accessible Hero',
                'subtitle': 'Testing accessibility',
                'cta_text': 'Learn More',
                'cta_link': '/about/'
            }),
            ('content', {
                'title': 'Accessible Content',
                'content': '<p>This is accessible content.</p>',
                'image_position': 'right'
            })
        ]
    )
    root_page.add_child(instance=landing_page)
    
    # Create a site with the landing page as the root
    site = Site.objects.first()
    site.root_page = landing_page
    site.save()
    
    # Request the page
    client = Client()
    response = client.get(landing_page.url)
    
    # Check accessibility features
    content = response.content.decode('utf-8')
    
    # Skip to content link
    assert '<a href="#main-content" class="skip-link">Skip to content</a>' in content
    
    # Main content area with proper role and ID
    assert '<main id="main-content" role="main">' in content
    
    # Alt text for images (will be added by the template)
    assert 'alt="' in content
    
    # ARIA attributes
    assert 'aria-label="' in content
    assert 'aria-hidden="' in content
    
    # Semantic HTML
    assert '<header>' in content
    assert '<nav' in content
    assert '<footer>' in content
    assert '<main' in content
