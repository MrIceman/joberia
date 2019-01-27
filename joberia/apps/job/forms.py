from django import forms

from joberia.apps.job.models import Job


class CreateJobForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = [
            'title', 'description', 'short_description', 'tags', 'desired_profile', 'offered_items', 'bonuses']
