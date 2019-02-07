from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.generic import View
from rest_framework.parsers import JSONParser

from joberia.apps.common import REQUEST_KEY_USER, REQUEST_KEY_PLATFORM
from joberia.apps.common.auth import jwt_required
from joberia.apps.common.responses import create_failed_message
from joberia.apps.job.models import OfferedItem, Job, Bonus, Tag, DesiredProfileItem
from joberia.apps.job.serializers import JobSerializer


class CreateJobView(View):
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

            print('Platform: {}'.format(str(platform)))

            job = Job(title=title, status='off', description=description, short_description=short_description,
                      created_by=created_by, platform_id=platform.pk)
            job.save()

            for o in offers:
                OfferedItem(label=o, job=job, platform_id=platform.pk).save()
            for k, v in bonuses:
                Bonus(name=k, value=v, job=job, platform_id=platform.pk).save()
            for skill in skill_tags:
                Tag(type='skill', name=skill, job=job, platform_id=platform.pk).save()
            for loca in location_tags:
                Tag(type='loc', name=loca, job=job, platform_id=platform.pk).save()
            for dp in desired_profile:
                DesiredProfileItem(name=dp, job=job, platform_id=platform.pk).save()
            serializer = JobSerializer(instance=job)

            return JsonResponse(serializer.data)


        except Exception as e:
            return JsonResponse(create_failed_message(str(e)))
