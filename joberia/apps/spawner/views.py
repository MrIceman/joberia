# Create your views here.
from django.http import JsonResponse
from django.views import View
from rest_framework.parsers import JSONParser

from joberia.apps.common.hasher import hash_sha256
from joberia.apps.common.responses import create_data_does_not_exist_response
from joberia.apps.spawner.models import Platform
from .serializers import PlatformSerializer


class CreatePlatform(View):
    def post(self, request):
        data = JSONParser().parse(request)
        serializer = PlatformSerializer(data=data)

        if serializer.is_valid():
            instance = serializer.save()
            name = instance.platform_name
            instance.hash = hash_sha256(name)
            instance.save()
            return JsonResponse(serializer.data, status=200)
        else:
            return JsonResponse({'message': 'Data {} is not valid'.format(data)})

    def get(self, request):
        platform_id = request.GET.get('platform_id')

        if platform_id:
            platform = Platform.objects.filter(pk=platform_id).first()
            if platform is None:
                return JsonResponse(create_data_does_not_exist_response())
            serializer = PlatformSerializer(platform)
            return JsonResponse(serializer.data)
        else:
            all_platforms = Platform.objects.all()
            serializer = PlatformSerializer(all_platforms, many=True)
            return JsonResponse(serializer.data, safe=False)
