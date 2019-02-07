from django.urls import path

from .views import CreateJobView

urlpatterns = [
    path('create/', CreateJobView.as_view(), name='create_job'),

]
