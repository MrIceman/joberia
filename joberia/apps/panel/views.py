from django.shortcuts import render, redirect

# Create your views here.
from django.views.generic.base import View


class PanelView(View):

    def get(self, request):
        if not request.user.is_authenticated:
            return redirect('/user/login')
