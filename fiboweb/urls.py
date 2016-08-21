"""fiboweb URL Configuration
"""
from django.conf.urls import include, url
from django.contrib import admin


urlpatterns = [
    url(r'^', include('fiboweb.web.urls')),
    url(r'^admin/', admin.site.urls),
]
