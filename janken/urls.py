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
    path('response/<int:response_id>/like/', views.ResponseLikeAjaxView.as_view(), name='response_like'),
    path('response/<int:response_id>/edit/', views.ResponseEditView.as_view(), name='response_edit'),
    path('response/<int:response_id>/remove/', views.ResponseRemoveView.as_view(), name='response_remove'),
    path('response/list/', views.ResponseListView.as_view(), name='response_list'),
    path('response/<int:response_id>/detail/', views.ResponseDetailView.as_view(), name='response_detail'),
    path('match/list/', views.MatchListView.as_view(), name='match_list'),
    path('match/<int:match_id>/detail/', views.MatchDetailView.as_view(), name='match_detail'),
]
