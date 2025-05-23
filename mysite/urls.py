from django.conf import settings
from django.urls import include, path
from django.contrib import admin
from django.http import JsonResponse

from wagtail.admin import urls as wagtailadmin_urls
from wagtail import urls as wagtail_urls
from wagtail.documents import urls as wagtaildocs_urls

from search import views as search_views
from landing.views import RobotsView, SitemapView, manifest_view
def health_check(request):
    """Health check endpoint for monitoring."""
    return JsonResponse({"status": "ok"})

urlpatterns = [
    path("django-admin/", admin.site.urls),
    path("admin/", include(wagtailadmin_urls)),
    path("documents/", include(wagtaildocs_urls)),
    path("search/", search_views.search, name="search"),
    path("healthz/", health_check, name="health_check"),
     # SEO URLs
    path('robots.txt', RobotsView.as_view(), name='robots'),
    path('sitemap.xml', SitemapView.as_view(), name='sitemap'),
    path('manifest.json', manifest_view, name='manifest'),
]


if settings.DEBUG:
    from django.conf.urls.static import static
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns

    # Serve static and media files from development server
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns = urlpatterns + [
    # For anything not caught by a more specific rule above, hand over to
    # Wagtail's page serving mechanism. This should be the last pattern in
    # the list:
    path("", include(wagtail_urls)),
    # Alternatively, if you want Wagtail pages to be served from a subpath
    # of your site, rather than the site root:
    #    path("pages/", include(wagtail_urls)),
]
