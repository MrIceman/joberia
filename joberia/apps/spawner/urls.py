from django.urls import path

from .views import CreatePlatform

urlpatterns = [
    path('platform/', CreatePlatform.as_view(), name='create_platform'),
]
