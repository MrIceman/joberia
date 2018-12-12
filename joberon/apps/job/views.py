from django.views.generic import ListView, DetailView

from joberon.apps.job.models import Job, Comment


class JobListView(ListView):
    model = Job
    template_name = 'job/job_list.html'

    def get_queryset(self):
        return Job.objects.all()


class JobDetailView(DetailView):
    model = Job
    template_name = 'job/job_detail.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        data = super().get_context_data(**kwargs)
        comments = Comment.objects.filter(is_confirmed=True).all()
        data['comments'] = comments
        return data
