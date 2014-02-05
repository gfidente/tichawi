from django.conf.urls import patterns, include, url
from django.views.generic.base import RedirectView

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'tichawi.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),

    url(r'^$', RedirectView.as_view(url='planet/')),
    url(r'^planet/', include('planet.urls')),
    url('', include('social.apps.django_app.urls', namespace='social'))
)
