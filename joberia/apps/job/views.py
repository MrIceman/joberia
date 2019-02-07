from django.utils.decorators import method_decorator
from django.views.generic import ListView, DetailView

from joberia.apps.core.utils import themed_view
from joberia.apps.job.models import Job, Comment


