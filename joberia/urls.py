from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from joberia.apps.core.views import letsencrypt1, letsencrypt2

urlpatterns = [
    path('', include('joberon.apps.job.urls')),
    path('alert/', include('joberon.apps.alert.urls')),
    path('user/', include('joberon.apps.user.urls')),
    path('job/', include('joberon.apps.job.urls')),
    path('admin/', admin.site.urls),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
