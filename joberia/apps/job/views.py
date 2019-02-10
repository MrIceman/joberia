from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.generic import View
from rest_framework.parsers import JSONParser

from joberia.apps.common import REQUEST_KEY_USER, REQUEST_KEY_PLATFORM
from joberia.apps.common.auth import jwt_required
from joberia.apps.common.responses import create_failed_message, create_data_does_not_exist_response, \
    create_not_authorized_response, create_action_successful_response
from joberia.apps.job.models import OfferedItem, Job, Bonus, Tag, DesiredProfileItem
from joberia.apps.job.serializers import JobSerializer


class JobView(View):
    """
        data = {
            'title': 'Joberia AI Engineer',
            'created_by': '1',
            'description': 'Hello',
            'short_description': 'asdfaf',
            'desired_profile': ['4 years experience', 'aws', 'docker skills', 'self reliant'],
            'offers': ['home office', 'high salary', 'budget', 'vacations'],
            'bonuses': ['13 salary'],
            'location_tags': ['munich'],
            'skill_tags': ['postgres', 'docker', 'nodejs', 'react'],
            'expires_at': time.time(),
        }

        """

    @method_decorator(jwt_required)
    def delete(self, request, *args, **kwargs):
        try:
            user = kwargs[REQUEST_KEY_USER]
            platform = kwargs[REQUEST_KEY_PLATFORM]
            job_id = request.GET.get('id')

            jobs = Job.objects.all()

            serializer = JobSerializer(instance=jobs, many=True)

            if user and job_id is not None:
                job = Job.objects.filter(pk=job_id, platform=platform.pk).first()
                if job is None:
                    return JsonResponse(create_data_does_not_exist_response())
                if job.created_by.pk != user.pk:
                    return JsonResponse(create_not_authorized_response())
                else:
                    job.delete()
                    return JsonResponse(
                        create_action_successful_response('{id} was deleted successfully.'.format(id=job_id)))
        except Exception as e:
            return JsonResponse(create_failed_message(str(e)))

    def get(self, request):
        job_id = request.GET.get('id')
        if job_id is None:
            jobs = Job.objects.all()
            serializer = JobSerializer(instance=jobs, many=True)
            return JsonResponse(serializer.data, safe=False)

        job = Job.objects.filter(pk=job_id).first()
        serializer = JobSerializer(instance=job)
        return JsonResponse(serializer.data)

    @method_decorator(jwt_required)
    def post(self, request, *args, **kwargs):
        data = JSONParser().parse(request)
        try:
            offers = data['offers']
            bonuses = data['bonuses']
            skill_tags = data['skill_tags']
            location_tags = data['location_tags']
            description = data['description']
            desired_profile = data['desired_profile']
            title = data['title']
            short_description = data['short_description']
            created_by = kwargs[REQUEST_KEY_USER]
            platform = kwargs[REQUEST_KEY_PLATFORM]
            job = Job(title=title, status='off', description=description, short_description=short_description,
                      created_by=created_by, platform_id=platform.pk)
            job.save()

            for o in offers:
                OfferedItem(label=o, used_in_job=job, platform_id=platform.pk).save()
            for k, v in bonuses:
                Bonus(name=k, value=v, used_in_job=job, platform_id=platform.pk).save()
            for skill in skill_tags:
                Tag(type='skill', name=skill, used_in_job=job, platform_id=platform.pk).save()
            for loca in location_tags:
                Tag(type='loc', name=loca, used_in_job=job, platform_id=platform.pk).save()
            for dp in desired_profile:
                DesiredProfileItem(name=dp, used_in_job=job, platform_id=platform.pk).save()
            serializer = JobSerializer(instance=job)

            return JsonResponse(serializer.data)

        except Exception as e:
            return JsonResponse(create_failed_message(str(e)))
