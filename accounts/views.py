from django.shortcuts import render
from django.urls import reverse_lazy
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.views.generic import CreateView


class SignupView(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('janken:index')
    template_name = 'registration/signup.html'

    def form_valid(self, form):
        # self.objectにsave()されたユーザーオブジェクトが格納される。
        valid = super().form_valid(form)
        login(self.request, self.object)
        return valid
