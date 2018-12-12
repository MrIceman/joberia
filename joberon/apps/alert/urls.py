from django.urls import path

from joberon.apps.alert.views import DeveloperAlerts, OrganizationAlerts

urlpatterns = [
    path('dev', DeveloperAlerts.as_view()),
    path('org', OrganizationAlerts.as_view())
]
