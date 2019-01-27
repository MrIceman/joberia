from django.contrib.auth.decorators import login_required
# Create your views here.
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.generic.base import View

from joberia.apps.core.utils import themed_view


class PanelView(View):
    user = None

    @method_decorator(login_required)
    def get(self, request):
        self.user = request.user
        context = self.get_context_data()
        return render(request, 'panel/index.html', context)

    @method_decorator(themed_view)
    def get_context_data(self, **kwargs):
        context = dict()
        context['theme'] = kwargs['theme']
        context['theme'].background_color = context['theme'].primary_color
        profile = self.user
        context['profile'] = profile
        context['disable_footer'] = True
        return context
