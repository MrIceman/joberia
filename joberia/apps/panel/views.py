from django.contrib.auth.decorators import login_required
# Create your views here.
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.generic.base import View

from joberia.apps.spawner.models import Theme
from joberia.apps.user.models import Profile


class PanelView(View):
    user = None

    @method_decorator(login_required)
    def get(self, request):
        self.user = request.user
        context = self.get_context_data()
        return render(request, 'panel/index.html', context)

    def get_context_data(self):
        context = {}
        theme = Theme.objects.filter().all().first()
        context['theme'] = theme
        theme.background_color = theme.primary_dark_color
        profile = Profile.objects.filter(user_id=self.user.id).first()
        context['profile'] = profile
        context['disable_footer'] = True
        return context
