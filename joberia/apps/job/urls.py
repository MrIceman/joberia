from django.urls import path

from joberia.apps.job.views import (
    JobListView, JobDetailView,
    CreateJobView)

urlpatterns = [
    path('create', CreateJobView.as_view(), name='job_create'),
    path('<int:pk>', JobDetailView.as_view(), name='job_detail'),
    path('', JobListView.as_view(), name='job_list'),

]
