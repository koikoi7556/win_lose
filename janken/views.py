import logging
import random

from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.views.generic import View, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http.response import JsonResponse
from .models import Match, Response, Like
from .forms import ResponseForm

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
        # そのレスポンスをLikeしているか, ゲストのときError回避のため分岐
        if request.user.is_active:        
            is_like = Like.objects.filter(user=request.user, response=match.response).exists()
        else: 
            is_like = False
        return render(request, 'janken/result.html',context={'match': match, 'opponent_hand': opponent_hand, 'is_like': is_like})


result = ResultView.as_view()


class MatchView(View):
    """
    LoginUserならばPOSTメソッドで処理し、DB保存リダリレクト。GuestUserならばGETメソッドで処理し、DB不保存レンダリング。
    """

    def post(self, request, *args, **kwargs):
        user_hand = int(request.POST.get('user_hand'))
        result, opponent_hand = janken(user_hand)
        # レスポンスを結果からランダム選択
        response_list = Response.objects.filter(result=result)
        response = random.choice(response_list)
        match = Match(
            user=request.user,
            response = response,
            user_hand = user_hand,
            opponent_hand = opponent_hand,
            result = result
        )
        match.save()
        return redirect('janken:result', pk=match.pk, )

    def get(self, request, *args, **kwargs):
        user_hand = int(request.GET.get('user_hand'))
        result, opponent_hand = janken(user_hand)
        response_list = Response.objects.filter(result=result)
        response = random.choice(response_list)
        if opponent_hand == 0:
            opponent_hand = 'rock'
        elif opponent_hand == 1:
            opponent_hand = 'peace'
        elif opponent_hand == 2:
            opponent_hand = 'paper'
        else:
            opponent_hand == ''
        context = {
            'user_hand': user_hand,
            'result': result, 
            'opponent_hand': opponent_hand,
            'response': response,
        }
        return render(request, 'janken/result.html', context=context)




match = MatchView.as_view()


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


class ResponseLikeAjaxView(LoginRequiredMixin, View):
    """
    いいねが押されたときデータをAjaxで返す
    """
    def post(self, request, response_id, *args, **kwargs):
        response = get_object_or_404(Response, pk=response_id)
        is_like = Like.objects.filter(user=request.user, response=response).exists()
        # unlike
        if is_like:
            liking = Like.objects.get(user=request.user, response=response)
            liking.delete()
            response.like_num -= 1
            response.save()
            data = {
                'is_like': is_like,
                'like_num': response.like_num
            }
            return JsonResponse(data)
        # like
        response.like_num += 1
        response.save()
        like = Like()
        like.user = request.user
        like.response = response
        like.save()
        data = {
            'is_like': is_like,
            'like_num': response.like_num
        }
        return JsonResponse(data) 


responseLikeAjax = ResponseLikeAjaxView.as_view()


class ResponseNewView(LoginRequiredMixin, View):
    """
    Responseデータを作成
    """
    def get(self, request, *args, **kwargs):
        return render(request, 'janken/response_edit.html', {'form': ResponseForm()})

    def post(self, request, *args, **kwargs):
        form = ResponseForm(request.POST)
        if not form.is_valid():
            return render(request, 'janken/response_edit.html', {'form': form})
        
        response = form.save(commit=False)
        response.author = request.user
        response.save()
        return redirect('janken:response_detail', response_id=response.pk)


responseNew = ResponseNewView.as_view()


class ResponseEditView(LoginRequiredMixin, View):
    """
    Responseデータを編集
    """
    def get(self, request, response_id, *args, **kwargs):
        response = get_object_or_404(Response, pk=response_id, author=request.user)
        form = ResponseForm(instance=response)    
        return render(request, 'janken/response_edit.html', {'form': form})

    def post(self, request, response_id, *args, **kwargs):
        response = get_object_or_404(Response, pk=response_id, author=request.user)
        form = ResponseForm(request.POST, instance=response)
        if not form.is_valid():
            render(request, 'janken/response_edit.html', {'form': form})
        
        response.save()
        return redirect('janken:response_detail', response_id=response.pk)


responseEdit = ResponseEditView.as_view()


class ResponseRemoveView(LoginRequiredMixin, View):
    """
    Responseデータを削除
    """
    def get(self, request, response_id, *args, **kwargs):
        response = get_object_or_404(Response, pk=response_id, author=request.user)
        return render(request, 'janken/response_confirm_delete.html', {'response': response})

    def post(self, request, response_id, *args, **kwargs):
        response = get_object_or_404(Response, pk=response_id, author=request.user)
        response.delete()
        return redirect('janken:response_list')
        

responseRemove = ResponseRemoveView.as_view()


class ResponseListView(LoginRequiredMixin, View):
    """
    Responseのリスト表示
    """
    def get(self, request, *args, **kwargs):
        response_list = Response.objects.filter(author=request.user).order_by('-created_at')
        return render(request, 'janken/response_list.html', {'response_list': response_list})


responseList = ResponseListView.as_view()


class ResponseDetailView(LoginRequiredMixin, View):
    """
    Responseの詳細表示
    """
    def get(self, request, response_id, *args, **kwargs):
        response = get_object_or_404(Response, pk=response_id)
        is_like = Like.objects.filter(user=request.user, response=response).exists()        
        return render(request, 'janken/response_detail.html', {'response': response, 'is_like': is_like})


responseDetail = ResponseDetailView.as_view()


class MatchListView(LoginRequiredMixin, View):
    """
    Matchのリスト表示
    """
    def get(self, request, *args, **kwargs):
        match_list = Match.objects.filter(user=request.user).order_by('-match_time')
        return render(request, 'janken/match_list.html', {'match_list': match_list})


matchList = MatchListView.as_view()


class MatchDetailView(LoginRequiredMixin, View):
    """
    Matchの詳細表示
    """
    def get(self, request, match_id, *args, **kwargs):
        match = get_object_or_404(Match, pk=match_id)
        # match.opponent_handを文字へ変換
        if match.opponent_hand == 0:
            opponent_hand = 'rock'
        elif match.opponent_hand == 1:
            opponent_hand = 'peace'
        elif match.opponent_hand == 2:
            opponent_hand = 'paper'
        else:
            opponent_hand == ''
        is_like = Like.objects.filter(user=request.user, response=match.response).exists()
        return render(request, 'janken/match_detail.html', {'match': match, 'is_like': is_like, 'opponent_hand': opponent_hand})


matchDetail = MatchDetailView.as_view()


class MatchLikeListView(LoginRequiredMixin, View):
    """
    MatchのLikeリスト表示
    """
    def get(self, request, *args, **kwargs):
        responseLikeList = Response.objects.filter(like__user=request.user)
        matchLike_list = []
        for responseLike in responseLikeList:
            matchLike = Match.objects.filter(user=request.user, response=responseLike)[0]
            matchLike_list.append(matchLike)
        # matchLike_list = Match.objects.filter(response__like__user=request.user, user=request.user)
        return render(request, 'janken/matchLike_list.html', {'matchLike_list': matchLike_list})


matchList = MatchListView.as_view()