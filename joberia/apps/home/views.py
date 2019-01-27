# Create your views here.
from django.utils.decorators import method_decorator
from django.views.generic import ListView

from joberia.apps.core.utils import themed_view
from joberia.apps.job.models import Job


class HomeView(ListView):
    model = Job
    template_name = 'index.html'

    def get_queryset(self):
        return Job.objects.all()

    @method_decorator(themed_view)
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        jobs = Job.objects.filter(status='on').all().order_by('udate').reverse()[:5]

        context['jobs'] = jobs
        context['theme'] = kwargs['theme']

        return context
