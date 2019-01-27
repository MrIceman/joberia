from django.utils.decorators import method_decorator
from django.views.generic import ListView, DetailView, UpdateView, FormView

from joberia.apps.company.models import Organization
from joberia.apps.core.utils import themed_view
from joberia.apps.job.forms import CreateJobForm
from joberia.apps.job.models import Job, Comment


class JobListView(ListView):
    model = Job
    template_name = 'job/job_list.html'

    def get_queryset(self):
        return Job.objects.all()

    @method_decorator(themed_view)
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['theme'] = kwargs['theme']
        return context


class JobDetailView(DetailView):
    model = Job
    template_name = 'job/job_detail.html'

    @method_decorator(themed_view)
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        comments = Comment.objects.filter(is_confirmed=True).all()
        context['comments'] = comments
        context['theme'] = kwargs['theme']
        return context


class CreateJobView(FormView):
    form_class = CreateJobForm
    template_name = 'job/job_create.html'
    success_url = '/'

    def form_valid(self, form):
        print('FORMITY FORM')

        print(form.cleaned_data)

        if form.is_valid():
            form.instance.created_by = self.request.user
            org = Organization.objects.all().first()
            form.instance.organization = org
            form.save(commit=True)

        return super().form_valid(form)


class UpdateJobForm(UpdateView):
    model = Job
