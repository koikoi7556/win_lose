import logging

from django.contrib import messages
from django.shortcuts import render, get_object_or_404
from django.views.generic import View

logeer = logging.getLogger(__name__)


class IndexView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'janken/index.html')


index = IndexView.as_view()


class ResultView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'janken/result.html')

    
result = ResultView.as_view()


class ProfileView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'janken/profile.html')


profile = ProfileView.as_view()