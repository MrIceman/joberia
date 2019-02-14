from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.generic import View
from rest_framework.parsers import JSONParser

from joberia.apps.common import REQUEST_KEY_USER, REQUEST_KEY_PLATFORM
from joberia.apps.common.auth import jwt_required
from joberia.apps.common.responses import create_failed_message, create_data_does_not_exist_response, \
    create_not_authorized_response, create_action_successful_response
from joberia.apps.job.models import OfferedItem, Job, Bonus, Tag, DesiredProfileItem, Comment
from joberia.apps.job.serializers import JobSerializer, CommentSerializer
from joberia.apps.spawner.models import Platform


class JobView(View):
    @method_decorator(jwt_required)
    def put(self, request, *args, **kwargs):
        try:
            user = kwargs[REQUEST_KEY_USER]
            platform = kwargs[REQUEST_KEY_PLATFORM]
            data = JSONParser().parse(request)

            job_id = data['id']

            del data['id']
            if user and job_id is not None:
                job = Job.objects.filter(pk=job_id, platform=platform.pk).first()
                if job is None:
                    return JsonResponse(create_data_does_not_exist_response())
                if job.created_by.pk != user.pk:
                    return JsonResponse(create_not_authorized_response())
                else:
                    serializer = JobSerializer(job, data=data, partial=True)
                    if serializer.is_valid():
                        serializer.save()
                        return JsonResponse(serializer.data)
                    else:
                        return JsonResponse(create_failed_message(serializer.errors))
        except Exception as e:
            return JsonResponse(create_failed_message(str(e)))

    @method_decorator(jwt_required)
    def delete(self, request, *args, **kwargs):
        try:
            user = kwargs[REQUEST_KEY_USER]
            platform = kwargs[REQUEST_KEY_PLATFORM]
            job_id = request.GET.get('id')

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
        platform_id = request.GET.get('platform')
        if job_id is None:
            if platform_id is not None:
                platform = Platform.objects.filter(pk=platform_id).first()
                if platform is None:
                    return JsonResponse(create_data_does_not_exist_response('Platform does not exist.'))
                jobs = Job.objects.filter(platform_id=platform_id).all()
                serializer = JobSerializer(instance=jobs, many=True)
                return JsonResponse(serializer.data, safe=False)
            else:
                return JsonResponse(create_data_does_not_exist_response('Platform ID required'))
        job = Job.objects.filter(pk=job_id, platform_id=platform_id).first()
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


class CommentView(View):

    @method_decorator(jwt_required)
    def delete(self, request, *args, **kwargs):
        job_id = request.GET.get('job_id')
        comment_id = request.GET.get('id')
        user = kwargs.get(REQUEST_KEY_USER)
        platform = kwargs.get(REQUEST_KEY_PLATFORM)
        job = Job.objects.filter(pk=job_id, created_by=user.pk, platform=platform.pk).first()
        if job is None:
            return JsonResponse(create_data_does_not_exist_response('Job does not exist.'))
        else:
            comment = job.comments.filter(pk=comment_id).first()
            if comment is None:
                return JsonResponse(
                    create_data_does_not_exist_response('Comment {} does not exist.'.format(comment_id)))
            comment.delete()
            return JsonResponse(
                create_action_successful_response('Comment {id} was deleted successfully.'.format(id=comment_id)))

    @method_decorator(jwt_required)
    def post(self, request, *args, **kwargs):
        comment_data = JSONParser().parse(request)
        user = kwargs.get(REQUEST_KEY_USER)
        platform = kwargs.get(REQUEST_KEY_PLATFORM)
        job = Job.objects.filter(pk=comment_data['job_id'], created_by=user.pk, platform=platform.pk).first()
        if job is None:
            return JsonResponse(create_data_does_not_exist_response())
        comment_data.update({'job': comment_data['job_id']})
        comment_data.update({'platform': platform.pk})
        comment_data.update({'author': user.pk})
        serializer = CommentSerializer(data=comment_data)
        if serializer.is_valid():
            instance = serializer.save()
            return JsonResponse(serializer.data)
        else:
            return JsonResponse(create_failed_message(serializer.errors))

    @method_decorator(jwt_required)
    def put(self, request, *args, **kwargs):
        comment_data = JSONParser().parse(request)
        comment = Comment.objects.filter(pk=comment_data['id'], job=comment_data['job'],
                                         platform=kwargs.get(REQUEST_KEY_PLATFORM),
                                         author=kwargs.get(REQUEST_KEY_USER)).first()
        serializer = CommentSerializer(instance=comment, data=comment_data, partial=True)
        if serializer.is_valid():
            instance = serializer.save()
            return JsonResponse(serializer.data)
        else:
            return JsonResponse(create_failed_message(serializer.errors))
