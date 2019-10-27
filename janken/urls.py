from django.urls import path
from django.views.generic import TemplateView

from . import views

app_name = 'janken'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('match/', views.MatchView.as_view(), name='match'),
    path('result/<int:pk>/', views.ResultView.as_view(), name='result'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('response/new/', views.ResponseNewView.as_view(), name='response_new'),
    path('response/<int:response_id>/like/', views.ResponseLikeView.as_view(), name='response_like'),
    path('response/<int:response_id>/edit/', views.ResponseEditView.as_view(), name='response_edit'),
    path('response/<int:response_id>/remove/', views.ResponseRemoveView.as_view(), name='response_remove'),
]
