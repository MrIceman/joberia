import json

from django.http import JsonResponse
from django.views import View

from joberon.apps.alert.models import Alert


def _get_alerts_by_type(type):
    alerts = Alert.objects.filter(type=type).all()
    result = [a.to_dict() for a in alerts]

    return result


class DeveloperAlerts(View):

    def get(self, request):
        param_user_id = request.GET.get('id', None)

        if param_user_id:
            alert = Alert.objects.filter(user_id=param_user_id).first()
            return JsonResponse(alert.to_dict(), safe=False)

        return JsonResponse(_get_alerts_by_type('dev'), safe=False)

    def post(self, request):
        # TODO: Return verbose error message when User already has a Subscription
        data = json.loads(request.body)
        user_id = data['user_id']
        alert_type = data['type']
        is_active = data['is_active']

        values = {
            'user_id': user_id,
            'type': alert_type,
            'is_active': is_active
        }

        alert = Alert.objects.create(**values)
        alert.save()

        return JsonResponse(alert.to_dict(), safe=False)


class OrganizationAlerts(View):

    def get(self, request):
        param_orga_id = request.GET.get('id', None)

        if param_orga_id:
            alert = Alert.objects.filter(organization_id=param_orga_id).first()
            return JsonResponse(alert.to_dict(), safe=False)

        return JsonResponse(_get_alerts_by_type('org'), safe=False)

    def post(self, request):
        # TODO: Return verbose error message when User already has a Subscription
        data = json.loads(request.body)
        user_id = data['user_id']
        alert_type = data['type']
        is_active = data['is_active']
        org_id = data['organization_id']

        values = {
            'user_id': user_id,
            'type': alert_type,
            'is_active': is_active,
            'organization_id': org_id
        }

        alert = Alert.objects.create(**values)
        alert.save()

        return JsonResponse(alert.to_dict(), safe=False)
