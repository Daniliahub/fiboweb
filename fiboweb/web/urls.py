from django.conf.urls import url

import fiboweb.web.views


urlpatterns = [
    url(r'^$', fiboweb.web.views.fibonacci, name='fibonacci'),
]
