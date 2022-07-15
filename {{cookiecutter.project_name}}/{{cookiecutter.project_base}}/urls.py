from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.contrib.sitemaps.views import sitemap
from django.views import defaults as default_views
from django.views.generic.base import TemplateView

sitemaps = {}

urlpatterns = [
    # core
    path(settings.ADMIN_URL, admin.site.urls),
    path(
        "robots.txt",
        TemplateView.as_view(template_name="robots.txt",
                             content_type="text/plain"),
    ),
    path(
        "sitemap.xml",
        sitemap,
        {"sitemaps": sitemaps},
        name="django.contrib.sitemaps.views.sitemap",
    ),
    # 3rd parties
    path("accounts/", include("allauth.urls")),
    # User management
    path(
        "users/",
        include("{{ cookiecutter.project_name }}.apps.users.urls",
                namespace="users")),
    # local: custom urls
    path("",
         TemplateView.as_view(template_name="pages/home.html"),
         name="home"),
]

if settings.DEBUG:
    urlpatterns += [
        static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT),
        static(settings.STATIC_URL, document_root=settings.STATIC_ROOT),

        # This allows the error pages to be debugged during development.
        path(
            "400/",
            default_views.bad_request,
            kwargs={"exception": Exception("Bad Request!")},
        ),
        path(
            "403/",
            default_views.permission_denied,
            kwargs={"exception": Exception("Permission Denied")},
        ),
        path(
            "404/",
            default_views.page_not_found,
            kwargs={"exception": Exception("Page not Found")},
        ),
        path("500/", default_views.server_error),
    ]

    if "debug_toolbar" in settings.INSTALLED_APPS:
        urlpatterns += [
            path("__debug__/", include("debug_toolbar.urls")),
        ]
