from django.urls import path

from joberia.apps.panel.views import PanelView

urlpatterns = [
    path('', PanelView.as_view(), name='panel'),
]
