from django.views.generic import CreateView

from joberia.apps.job.models import Job


class CreateJobForm(CreateView):
    model = Job


class UpdateJobForm(CreateView):
    model = Job
