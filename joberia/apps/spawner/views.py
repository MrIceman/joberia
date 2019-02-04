# Create your views here.
from django.http import JsonResponse
from django.views import View
from rest_framework.parsers import JSONParser

from .serializers import PlatformSerializer


class CreatePlatform(View):
    def post(self, request, *args, **kwargs):
        data = JSONParser().parse(request)
        serializer = PlatformSerializer(data=data)

        if serializer.is_valid():
            instance = serializer.save()
            instance.hash = hash(instance.platform_name)
            instance.save()
            return JsonResponse(serializer.data, status=200)
        else:
            return JsonResponse({'message': 'Data {} is not valid'.format(data)})
