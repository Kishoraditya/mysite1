from django.http import HttpResponse
from django.template.loader import render_to_string
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.generic import TemplateView

from wagtail.models import Page, Site
import json

class RobotsView(TemplateView):
    content_type = 'text/plain'
    template_name = 'robots.txt'


@method_decorator(cache_page(60 * 60 * 24), name='dispatch')  # Cache for 24 hours
class SitemapView(TemplateView):
    content_type = 'application/xml'
    template_name = 'sitemap.xml'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Get current site
        site = Site.find_for_request(self.request)
        if not site:
            # Use the first site if none is found for the request
            site = Site.objects.first()
        
        # Get all live pages that are not excluded from sitemap
        pages = Page.objects.live().public().filter(
            depth__gt=1  # Exclude root page
        ).specific().order_by('path')
        
        # Create a list of pages with their URLs
        pages_with_urls = []
        for page in pages:
            # Get the full URL including domain
            full_url = page.get_full_url(request=self.request)
            
            # If full_url is empty, try to construct it
            if not full_url and site:
                full_url = f"{self.request.scheme}://{site.hostname}{page.url}"
            
            # Add to the list
            pages_with_urls.append({
                'page': page,
                'full_url': full_url,
                'last_published_at': page.last_published_at
            })
        
        context['pages_with_urls'] = pages_with_urls
        return context

def manifest_view(request):
    """
    Generate a web app manifest file
    """
    manifest = {
        "name": "Your Site Name",
        "short_name": "YourSite",
        "description": "Your site description",
        "start_url": "/",
        "display": "standalone",
        "background_color": "#ffffff",
        "theme_color": "#2b3990",
        "icons": [
            {
                "src": "/static/images/icon-192x192.png",
                "sizes": "192x192",
                "type": "image/png"
            },
            {
                "src": "/static/images/icon-512x512.png",
                "sizes": "512x512",
                "type": "image/png"
            }
        ]
    }
    
    return HttpResponse(
        content=json.dumps(manifest),
        content_type='application/json'
    )
