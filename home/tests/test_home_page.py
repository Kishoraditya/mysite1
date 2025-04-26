import pytest
import os
from django.conf import settings
from django.core.management import call_command
from wagtail.models import Page
from home.models import HomePage


@pytest.fixture(scope="session")
def django_db_setup(django_db_setup, django_db_blocker):
    """Set up the test database."""
    with django_db_blocker.unblock():
        # Make sure static files are collected
        if not os.path.exists(settings.STATIC_ROOT):
            os.makedirs(settings.STATIC_ROOT)
        call_command('collectstatic', '--noinput')


@pytest.mark.django_db
def test_home_page_exists():
    """Test that the home page exists."""
    # The home page should be created by the initial migrations
    assert HomePage.objects.count() > 0
    
    # Get the home page
    home_page = HomePage.objects.first()
    
    # Check that it's a child of the root page
    assert home_page.get_parent().is_root()


@pytest.mark.django_db
def test_home_page_renders(client):
    """Test that the home page renders correctly."""
    # Get the home page
    home_page = HomePage.objects.first()
    
    # Update the home page with test content
    home_page.banner_title = "Test Banner Title"
    home_page.banner_subtitle = "Test Banner Subtitle"
    home_page.body = "<p>Test body content</p>"
    home_page.save()
    
    # Get the URL for the home page
    url = home_page.url
    
    # Request the URL
    response = client.get(url)
    
    # Check that the response is 200 OK
    assert response.status_code == 200
    
    # Check that our content is in the response
    content = response.content.decode('utf-8')
    assert "Test Banner Title" in content
    assert "Test Banner Subtitle" in content
    assert "Test body content" in content
