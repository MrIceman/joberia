# Create your views here.
from django.views import View
from rest_framework.renderers import JSONRenderer

from .models import Platform
from .serializers import PlatformSerializer


class PortalListView(View):

    def get(self, platform_id):
        platform = Platform.objects.filter(id=platform_id).first()

        serializer = PlatformSerializer(data=platform)
        if serializer.is_valid(raise_exception=True):
            return JSONRenderer().render(serializer.data)


class PortalDetailView(View):

    def get(self):
        pass
