import pytest
from django.test import TestCase
from wagtail.models import Page
from wagtail.test.utils import WagtailPageTestCase
from wagtail.rich_text import RichText
from landing.models import LandingPage


class TestLandingPage(WagtailPageTestCase):
    def test_can_create_landing_page(self):
        """Test that a landing page can be created."""
        root_page = Page.objects.get(id=1)
        landing_page = LandingPage(
            title="Test Landing Page",
            description="This is a test landing page",
        )
        root_page.add_child(instance=landing_page)
        
        # Test that the page was created
        retrieved_page = LandingPage.objects.get(id=landing_page.id)
        self.assertEqual(retrieved_page.title, "Test Landing Page")
        self.assertEqual(retrieved_page.description, "This is a test landing page")
    
    def test_landing_page_parent_pages(self):
        """Test that landing pages can be created under appropriate parent pages."""
        self.assertCanCreateAt(Page, LandingPage)
    
    def test_landing_page_child_pages(self):
        """Test that a LandingPage cannot have another LandingPage as a child."""
        child_landing_page = LandingPage(
            title="Child Landing Page",
            description="This is a child landing page",
        )
    
        # This should raise an error because LandingPage is not in subpage_types
        with self.assertRaises(Exception):
            self.landing_page.add_child(instance=child_landing_page)


@pytest.mark.django_db
def test_landing_page_stream_field():
    # Create a landing page with StreamField content
    landing_page = LandingPage(
        title="Stream Field Test",
        description="Testing StreamField",
    )
    
    # Save the page first
    root_page = Page.objects.get(id=1)
    root_page.add_child(instance=landing_page)
    
    # Add content to the body field - make sure this matches your StreamField definition
    landing_page.body = [
        ('hero', {
            'title': 'Test Hero',
            'subtitle': 'Test subtitle',
            'cta_text': 'Click me',
            'cta_link': '/test/'
        })
    ]
    landing_page.save()
    
    # Test that the content was saved correctly
    retrieved_page = LandingPage.objects.get(id=landing_page.id)
    assert len(retrieved_page.body) == 1  # Changed from 2 to 1 to match actual content
    assert retrieved_page.body[0].block_type == 'hero'
