import pytest
from django.test import Client, TestCase
from wagtail.models import Page, Site

from landing.models import LandingPage


from django.test.utils import override_settings

@override_settings(WAGTAILSEARCH_BACKENDS={
    'default': {
        'BACKEND': 'wagtail.search.backends.database',
        'AUTO_UPDATE': False,
    }
})
class TestLandingPageView(TestCase):
    def setUp(self):
        # Use default test host so Wagtail Site routing matches
        self.client = Client(HTTP_HOST='testserver')

        # Get the root page (ID 1)
        self.root_page = Page.objects.get(id=1)

        # Ensure a Site exists for testserver pointing at root_page
        self.site = Site.objects.filter(hostname='testserver').first()
        if not self.site:
            self.site = Site.objects.create(
                hostname='testserver',
                root_page=self.root_page,
                is_default_site=True
            )
        else:
            self.site.root_page = self.root_page
            self.site.is_default_site = True
            self.site.save()

        # Create and publish a LandingPage under root
        self.landing_page = LandingPage(
            title="Test Landing Page",
            slug="test-landing-page",
            description="This is a test landing page",
        )
        self.root_page.add_child(instance=self.landing_page)

        # Populate the StreamField body
        self.landing_page.body = [
            ('hero', {
                'title': 'Welcome to our site',
                'subtitle': 'This is a test hero section',
                'cta_text': 'Learn More',
                'cta_link': '/about/',
            }),
            ('features', {
                'title': 'Our Features',
                'features': [
                    {
                        'icon': 'fa-star',
                        'title': 'Feature 1',
                        'description': 'Description of feature 1',
                    }
                ],
            }),
        ]

        # Create a revision but avoid search-index push errors
        _rev = self.landing_page.save_revision()
        # Mark the page live without invoking the full publish machinery
        self.landing_page.live = True
        self.landing_page.save()


    def test_landing_page_200(self):
        """Landing page should return HTTP 200"""
        url = self.landing_page.url
        response = self.client.get(url)
        assert response.status_code == 200

    def test_landing_page_content(self):
        """Landing page displays hero and feature content"""
        url = self.landing_page.url
        response = self.client.get(url)
        assert response.status_code == 200

        self.assertContains(response, 'Welcome to our site')
        self.assertContains(response, 'This is a test hero section')
        self.assertContains(response, 'Learn More')
        self.assertContains(response, 'Our Features')
        self.assertContains(response, 'Feature 1')
        self.assertContains(response, 'Description of feature 1')

    def test_landing_page_meta_tags(self):
        """Landing page includes correct meta description tag"""
        url = self.landing_page.url
        response = self.client.get(url)
        assert response.status_code == 200

        # The template may render multiple meta description tags; we just need the correct content value
        self.assertIn(
            'content="This is a test landing page"',
            response.content.decode('utf-8')
        )




@pytest.mark.django_db
def test_robots_txt_view():
    client = Client()
    response = client.get('/robots.txt')

    assert response.status_code == 200
    assert response['Content-Type'] == 'text/plain'
    assert 'User-agent: *' in response.content.decode('utf-8')


from django.test.utils import override_settings

@override_settings(WAGTAILSEARCH_BACKENDS={
    'default': {
        'BACKEND': 'wagtail.search.backends.database',
        'AUTO_UPDATE': False,
    }
})
@pytest.mark.django_db
def test_sitemap_xml_view():
    root_page = Page.objects.get(id=1)

    # Create and publish a landing page for sitemap
    landing_page = LandingPage(
        title="Sitemap Test Page",
        slug="sitemap-test-page",
        description="Testing sitemap generation",
    )
    root_page.add_child(instance=landing_page)
    revision = landing_page.save_revision()
    revision.publish()
    landing_page.refresh_from_db()

    client = Client(HTTP_HOST='testserver')
    response = client.get('/sitemap.xml')

    assert response.status_code == 200
    assert response['Content-Type'] == 'application/xml'

    content = response.content.decode('utf-8')
    assert '<?xml version="1.0" encoding="UTF-8"?>' in content
    assert '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">' in content
    assert 'sitemap-test-page' in content or 'Sitemap Test Page' in content
