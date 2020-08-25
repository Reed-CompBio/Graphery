"""graphery URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls import url
from django.conf import settings
from django.contrib.sitemaps.views import sitemap


import backend.views as backend_view
from backend.sitemaps import BackendSitemap

from graphene_django.views import GraphQLView

sitemaps = {
    'whole_site': BackendSitemap
}

urlpatterns = [
    path('admin/', admin.site.urls),
    url('graphql', GraphQLView.as_view(graphiql=settings.DEBUG)),
    path('csrf', backend_view.csrf),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}),
    path(f'{settings.UPLOAD_STATICS_ENTRY}/<path:url>', backend_view.media_request)
]
