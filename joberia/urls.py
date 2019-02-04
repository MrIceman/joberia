from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('', include('joberia.apps.home.urls')),
    path('alert/', include('joberia.apps.alert.urls')),
    path('user/', include('joberia.apps.user.urls')),
    path('job/', include('joberia.apps.job.urls')),
    path('panel/', include('joberia.apps.panel.urls')),
    path('admin/', admin.site.urls),
    path('spawner/', include('joberia.apps.spawner.urls'))
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
