from django.db import models
from django.utils import timezone


class Response(models.Model):
    """
    勝ち負け時の画像と文章を保存するモデル
    """
    result = models.IntegerField(verbose_name='janken結果')
    author = models.ForeignKey('auth.User', on_delete=models.SET_NULL, null=True)
    image_link = models.TextField(verbose_name='画像URL', max_length=2000)
    text = models.TextField(verbose_name='コメント', max_length=1000)
    updated_at = models.DateTimeField(verbose_name='更新日時', auto_now_add=True)
    created_at = models.DateTimeField(verbose_name='作成日時', default=timezone.now)
    like_num = models.IntegerField(default=0)

    def __str__(self):
        return self.text[:40]

        
class Match(models.Model):
    """
    ユーザーの勝ち負けを保存するモデル
    """

    # user・responseが削除されても勝ち負け結果は、基本統計などに用いるため保存。
    user = models.ForeignKey('auth.User', null=True, on_delete=models.SET_NULL)
    response = models.ForeignKey(Response, verbose_name='レスポンス', null=True, on_delete=models.SET_NULL)
    user_hand = models.IntegerField(verbose_name='自分の手')
    opponent_hand = models.IntegerField(verbose_name='相手の手')
    result = models.IntegerField(verbose_name='勝負結果')
    match_time = models.DateTimeField(verbose_name='マッチタイム', default=timezone.now)

    def __str__(self):
        return '{}_{}'.format(self.user, self.match_time)


class Like(models.Model):
    """
    Responseに対する「いいね」
    """
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    response = models.ForeignKey(Response, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)
