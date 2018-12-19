# Create your views here.
from django.views.generic import ListView

from joberia.apps.job.models import Job
from joberia.apps.spawner.models import Theme


class HomeView(ListView):
    model = Job
    template_name = 'index.html'

    def get_queryset(self):
        return Job.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        jobs = Job.objects.filter(status='on').all().order_by('udate').reverse()[:5]
        theme = Theme.objects.filter().all().first()

        context['jobs'] = jobs
        context['theme'] = theme

        return context
