import logging
import random

from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.views.generic import View
from .models import Match, Response, Like

logeer = logging.getLogger(__name__)


class IndexView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'janken/index.html')


index = IndexView.as_view()


class ResultView(View):
    def get(self, request, pk, *args, **kwargs):
        match = get_object_or_404(Match, pk=pk)
        # match.opponent_handを文字へ変換
        if match.opponent_hand == 0:
            opponent_hand = 'rock'
        elif match.opponent_hand == 1:
            opponent_hand = 'peace'
        elif match.opponent_hand == 2:
            opponent_hand = 'paper'
        else:
            opponent_hand == ''
        return render(request, 'janken/result.html',context={'match': match, 'opponent_hand': opponent_hand})


result = ResultView.as_view()


class MatchView(View):
    def post(self, request, *args, **kwargs):
        user_hand = int(request.POST.get('user_hand'))
        result, opponent_hand = janken(user_hand)
        # レスポンスを結果からランダム選択
        response_list = Response.objects.filter(result=result)
        response = random.choice(response_list)
        try:
            match = Match(user=request.user)
        except ValueError:
            match = Match()
        match.response = response
        match.user_hand = user_hand
        match.opponent_hand = opponent_hand
        match.result = result
        match.save()
        return redirect('janken:result', pk=match.pk, )


def janken(user_hand):
    """user_handを引数に、(result, opponent_hand)を返す.それぞれの確率は等しい。
    
    Parameters
    ----------
    user_hand : [int]
        [0 or 1 or 2 でそれぞれ グー チョキ パー。]
    
    Return
    ----------
    [result, opponent_hand] : [int, int]
        [-1 or 0 or 1 でそれぞれ 負け あいこ 勝ち。], [0 or 1 or 2]
    """
    # 結果を確率で求める
    result = random.random()
    if result >= 2/3:
        result = 1
    elif result >= 1/3:
        result = 0
    else:
        result = -1
    
    # 結果からopponent_handを求める
    if result == 0:
        opponent_hand = user_hand
    elif user_hand + result == 3:
        opponent_hand = 0
    elif user_hand + result == -1:
        opponent_hand = 2
    else:
        opponent_hand = user_hand + result

    return result, opponent_hand
        


class ProfileView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'janken/profile.html')


profile = ProfileView.as_view()