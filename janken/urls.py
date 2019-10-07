from django.urls import path
from django.views.generic import TemplateView

from . import views

app_name = 'janken'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('result/', views.ResultView.as_view(), name='result'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
]
