from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import ListView, DetailView, CreateView, UpdateView

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


class CreateJobView(CreateView):
    model = Job
    template_name = 'job/job_create.html'
    fields = ['title', 'description', 'short_description', 'tags', 'desired_profile', 'offered_items', 'bonuses']
    """
     title = models.CharField(max_length=200)
    description = models.TextField()
    short_description = models.TextField(default='')
    status = models.CharField(choices=STATUS, default='off', max_length=5)
    tags = models.ManyToManyField(Tag, related_name='job_tags', default=None)
    desired_profile = models.ManyToManyField(DesiredProfileItem, related_name='job_desired_profile_items', default=None)
    offered_items = models.ManyToManyField(OfferedItem, related_name='job_offered_items', default=None)
    bonuses = models.ManyToManyField(BonusEntry, related_name='job_bonuses', default=None)

    # set only if payment is done
    expires_at = models.DateTimeField(null=True)

    # fks
    organization = models.ForeignKey(Organization, related_name='org_jobs', on_delete=models.CASCADE)
    created_by = models.ForeignKey(User, related_name='created_jobs', on_delete=models.DO_NOTHING)

    picture = models.FileField(verbose_name='job_picture', default=None)

"""

    @method_decorator(login_required)
    def form_valid(self, form):
        print('# # # # {}'.format('Forn is valid') * 10)
        obj = form.save(commit=False)
        obj.created_by = self.request.user
        obj.save()
        print('Forn is valid')
        return super().form_valid(form)


class UpdateJobForm(UpdateView):
    model = Job
