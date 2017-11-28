from django.conf.urls import url
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from .views import home


urlpatterns = [
    url(r'^$', home),
    url(r'^admin/', admin.site.urls),
]

urlpatterns.extend(staticfiles_urlpatterns())
