from django.views.generic import ListView, DetailView

from joberia.apps.job.models import Job, Comment
from joberia.apps.spawner.models import Theme


class JobListView(ListView):
    model = Job
    template_name = 'job/job_list.html'

    def get_queryset(self):
        return Job.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        theme = Theme.objects.filter().all().first()
        context['theme'] = theme
        return context


class JobDetailView(DetailView):
    model = Job
    template_name = 'job/job_detail.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        comments = Comment.objects.filter(is_confirmed=True).all()
        context['comments'] = comments
        theme = Theme.objects.filter().all().first()
        context['theme'] = theme
        return context
